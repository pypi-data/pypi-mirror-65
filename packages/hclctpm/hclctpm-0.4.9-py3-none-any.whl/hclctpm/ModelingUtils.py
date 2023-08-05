#### Michelangelo Causal Learning Infra. 
### -- UserCustomizableFunctions for model development environment 

## A set of user-modifiable and customizable functions, .e.g hyperparameter selection, 
## e.g. experiment plotting, e.g. query data from production sources 
## user is encouraged to custom to your particular use case. 
## Contribution back to Michelangelo repository is welcome 

import pandas as pd, numpy as np, pickle as pkl, sys, os, tensorflow as tf, matplotlib.pyplot as plt 
from operator import itemgetter 

from hclctpm.exp.Experimentation import * 
from hclctpm.dataprep.DataProcFunctions import * 
from hclctpm.models.pyMLModelDefinitions import * 
from hclctpm.models.PromotionModels import * 

def BenchmarkModels( 
    list_model_params, 
    dataspecs, 
    metricspecs 
    ): 
    ### A function to benchmark multiple models on the same dataset and same metrics 
    
    ### Input: 
    ### -- a list of model parameters 
    ### -- the data-set to benchmark on 
    ### -- the loss function and objective to use 
    ### -- ... 
    
    ### Return: 
    ### data structure containing plottable data to be utilized by MLvis 
    
    ### **CFF 
    
    print('---> starting to benchmark models for heterogeneous causal learning ---> ') 
    
    ### --- load data for CL from the data saved by QueryDataSaveFile 
    Dtrain, Dval, Dtest = CLDataPreparation(dataspecs) 
    ## the returns Dtrain, Dval, Dtest are dictionaries of the same keys 
    ## e.g. Dtrain.keys() = ['D', 'w', 'o', 'c'], each indicating 'data', 'treatment', 'gain', and 'cost', respectively 
    ## also Dtest.keys() = ['Dt', 'wt', 'ot', 'ct'] with slight variation of the naming 
    
    ### start training 
    val_results = dict() 
    dict_best_models = dict() 
    dict_model_testset_scores = dict() 
    
    ### train models across the list of potent models 
    for mi in range(len(list_model_params)): 
        dict_best_models[list_model_params[mi]['model_name']] = TrainModelWithValidation(list_model_params[mi], Dtrain, Dval) 
    
    for mi in range(len(list_model_params)): 
        dict_model_testset_scores[list_model_params[mi]['model_name']] = PredictTestSetScores(list_model_params[mi], Dtest, \
                                                                                              dict_best_models[list_model_params[mi]['model_name']])
    
    ### save models if indicated to deploy and providion of save folder 
    for mi in range(len(list_model_params)):
        if 'save_model_filename_for_deploy' in list_model_params[mi]: 
            dict_best_models[list_model_params[mi]['model_name']].save_weights(list_model_params[mi]['save_model_filename_for_deploy']) 
    GenerateExperimentResults(list_model_params, dict_model_testset_scores, Dtest) 

def QueryDataSaveFile(dataspecs, verbose=False): 
    ### Apply a data query to obtain data from ETL 
    ### and save to disk as pickle file, which is later used for training and validation 
    
    ### Input: 
    ###   dataspec - dict() of specifications for the data, query etc. 
    ###   verbose - bool indicator for print out 
    
    ### Return: 
    ###   None but save data to dataspecs['data_filename'] 
    
    ### **CFF 
    
    if 'saved_csv' in dataspecs:
        predFrame = pd.read_csv(dataspecs['saved_csv'])
    elif 'data_query' in dataspecs: 
        print('\n------> Running Presto to query data ... ') 
        predFrame = dataspecs['qr_client'].execute('presto', \
                                                   dataspecs['data_query']) 
        print('---> loading data into dsw...') 
        predFrame = pd.DataFrame(predFrame.load_data()) 
        print('done')
        if verbose: 
            print(predFrame) 
            print(predFrame.columns) 
    else:
        print('Error: not data query nor CSV specified')
        exit()
    
    cohort_column_name = dataspecs['cohort_column_name'] 
    treatment_indicator_value = dataspecs['treatment_indicator_value']
    control_indicator_value = dataspecs['control_indicator_value'] 
    
    print('\n---> Queried number of data samples: ' + str(len(predFrame)) + '  with '\
           + str(sum(predFrame[cohort_column_name] == control_indicator_value)) \
           + ' Control samples') 
    D = predFrame 
    D = D.sample(frac=1.0) ## mandatory shuffle of the queried dataset 
    
    feature_list = dataspecs['feature_list'] 
    label_list = dataspecs['label_list'] 
    
    mean_list = [] 
    std_list = [] 
    for l in feature_list: 
        print('number of nans: ' + str(sum(D[l] == '\\N'))) 
        D[l] = pd.to_numeric(D[l], errors='coerce') 
        me_v = D[l].mean() 
        st_v = D[l].std() 
        mean_list.append(me_v) 
        std_list.append(st_v) 
        D[l] = D[l] - me_v 
        D[l] = D[l] / st_v 
        D[l][pd.isnull(D[l])] = 0.0 ## at zero mean due to standard normalization 
    
    for l in label_list: 
        D[l] = pd.to_numeric(D[l], errors='coerce') 
        D[l][pd.isnull(D[l])] = 0.0 ## at zero mean due to standard normalization 
    
    #### ---- save the mean and std lists to file for deployment
    if 'save_meanstd_filename_for_deploy' in dataspecs:
        mean_list = np.asarray(mean_list)
        mean_list = np.reshape(mean_list, (len(feature_list), 1))
        std_list = np.asarray(std_list)
        std_list = np.reshape(std_list, (len(feature_list), 1))
        meanstd_save_dict = dict()
        meanstd_save_dict['mean_list'] = mean_list
        meanstd_save_dict['std_list'] = std_list
        pkl.dump(meanstd_save_dict, open(dataspecs['save_meanstd_filename_for_deploy'], 'wb'))
    
    if verbose: 
        ### -- compute simple statistics 
        treated_entries = D[D[cohort_column_name] == treatment_indicator_value] 
        untreated_entries = D[D[cohort_column_name] == control_indicator_value] 
        
        rpu_treated = float(treated_entries[label_list[0]].sum()) / len(treated_entries) 
        nipu_treated = float(treated_entries[label_list[1]].sum()) / len(treated_entries) 
        
        rpu_untreated = float(untreated_entries[label_list[0]].sum()) / len(untreated_entries) 
        nipu_untreated = float(untreated_entries[label_list[1]].sum()) / len(untreated_entries) 
        
        cpit = -1.0 * (nipu_treated - nipu_untreated) / (rpu_treated - rpu_untreated) 
        
        print('rpu_treated : ' + str(rpu_treated)) 
        print('nipu_treated : ' + str(nipu_treated)) 
        print('rpu_untreated : ' + str(rpu_untreated)) 
        print('nipu_untreated : ' + str(nipu_untreated)) 
        print('cpit : ' + str(cpit)) 
    
    ### split the data into 3/1/1 train/val/test 
    len_tr = int(len(D) / 5 * 3) 
    len_va = int(len(D) / 5) 
    
    nX = D[feature_list].as_matrix() 
    w = D[cohort_column_name].apply(lambda x: 1.0 if x == treatment_indicator_value else 0.0) 
    w = w.as_matrix() 
    values = D[label_list[0]] 
    values = values.as_matrix() 
    negcost = D[label_list[1]] 
    negcost = negcost.as_matrix() * 1.0 

    ## split train/val/test sets 

    nX_tr = nX[0:len_tr, :] 
    nX_va = nX[len_tr:len_tr + len_va, :] 
    nX_te = nX[len_tr + len_va:, :] 

    w_tr = w[0:len_tr]
    w_va = w[len_tr:len_tr + len_va] 
    w_te = w[len_tr + len_va:] 

    values_tr = values[0:len_tr] 
    values_va = values[len_tr:len_tr + len_va] 
    values_te = values[len_tr + len_va:] 

    negcost_tr = negcost[0:len_tr] 

    negcost_va = negcost[len_tr:len_tr + len_va] 

    negcost_te = negcost[len_tr + len_va:] 

    ## saving data using cPickel and naming the dictionaries 
    saveD = {'nX_tr':nX_tr, 
             'w_tr':w_tr, 
             'values_tr':values_tr, 
             'nX_va':nX_va, 
             'w_va':w_va, 
             'values_va':values_va, 
             'nX_te':nX_te, 
             'w_te':w_te, 
             'values_te':values_te, 
             'feature_list':feature_list, 
             #'avg_ni_usd_tr':avg_ni_usd_tr, 
             'negcost_tr': negcost_tr, 
             #'avg_ni_usd_va':avg_ni_usd_va, 
             'negcost_va': negcost_va, 
             #'avg_ni_usd_te':avg_ni_usd_te, 
             'negcost_te': negcost_te 
             } 

    pkl.dump(saveD, open(dataspecs['data_filename'], 'wb')) 

def TrainModelWithValidation(model_params, Dtrain, Dval):
    ### genertic function to train a model with validation set
    ### inclusive of hyperparameter selection methods
    ### the routines for model training, hyperparameter selection to call, are 
    ### based on model type and specifications
    
    ## Input: 
    ##   model-params: the model paramters with which to train 
    ##   Dtrain: dict() containing the training data 

    ## Return:
    ##   the model instance according to its trainer (keras, sklearn etc) 
    
    ### **CFF 
    if model_params['model_name'] == 'DPCM': 
        return_model = HPSelectMultiRandomInitializeTrainModel(model_params, Dtrain, Dval)
    elif model_params['model_name'] == 'STC': 
        return_model = HPSelectMultiRandomInitializeTrainModel(model_params, Dtrain, Dval)         
    elif model_params['model_name'] == 'rlearner' or model_params['model_name'] == 'slearner': 
        return_model = HPSelectMultParamsTrainModel(model_params, Dtrain, Dval) 
    elif model_params['model_name'] == 'custom_model_1': 
        print('placeholder for custom modesl to be added by customer ') 
        return_model = None 
    return return_model 

def HPSelectMultParamsTrainModel(model_params, Dtrain, Dval): 
    ### run grid search for parameter selection 
    ### first version implements basic linear models 
    
    pmodels = PromotionModels() 
    
    if model_params['model_name'] == 'rlearner': 
        print('---> Training R-learner model') 
        ## set-up RLearner 
        rl_ridge_model_O, rl_ridge_model_C = pmodels.fit_rlearner(Dtrain['D'], Dtrain['o'], Dtrain['c'], Dtrain['w']) 
        #rl_ridge_model_O, rl_ridge_model_D = pmodels.fit_rlearner(D, o, d2d, w) 
        
        return_model = dict() 
        return_model['O_model'] = rl_ridge_model_O 
        return_model['C_model'] = rl_ridge_model_C 
    elif model_params['model_name'] == 'slearner': 
        print('---> Training S-learner model') 
        slearner_O = pmodels.fit_slearner(Dtrain['D'], Dtrain['o'], Dtrain['w'])
        slearner_C = pmodels.fit_slearner(Dtrain['D'], Dtrain['c'], Dtrain['w'])
        return_model = dict() 
        return_model['O_model'] = slearner_O 
        return_model['C_model'] = slearner_C 
    
    return return_model 

def HPSelectMultiRandomInitializeTrainModel(model_params, Dtrain, Dval): 
    ### for-loop multiple random initializations of the same model
    
    ### Input: 
    ###   model_params - dictionary of model parameters 
    ###   Dtrain - dict containing all data for training 
    ###   Dval - dict containing all data for validation 

    ### Return: 
    ###   list of model instances from each random initialization, note this will be different per model (e.g. keras model from tf, sklearn model) 
    
    print('\n') 
    print('------> Training ' + model_params['model_name'] + ' models with multiple random initializations .... ') 
    list_raninit_models = [] 
    list_val_results = [] 
    for i in range(model_params['num_inits']): 
        print('--> random initialization iteration: '+str(i)) 
        ## re-implemented deep learning models in Keras and TF 2.0 
        trained_model, val_loss = TrainCLModel(model_params, Dtrain, Dval, i) 
        list_raninit_models.append(trained_model)
        print('->training finished')
        list_val_results.append(val_loss) ## get the most recent validation result 
    
    best_index = min(enumerate(list_val_results), key=itemgetter(1))[0] 
    print('--> best performing model: iteration ' + str(best_index) +' with val result:'+str(list_val_results[best_index])+' out of:') 
    print(list_val_results) 
    best_model = list_raninit_models[best_index] 
    
    return best_model 

def PredictTestSetScores(model_params, Dtest, model_struct): 
    ### perform CL model prediction based on model type
    
    ### Input: 
    ###   model_params: dict() of model parameters as provided in model development notebook
    ###   Dtest: dict() of data for the test-set
    ###      Dtest['Dt'] numpy array of data shape = (num_samples, num_features)
    
    ### Output:
    ###   return_scores: numpy array for score one per sample, shape = (num_samples,) 
    
    print('-----> Predicting model:'+model_params['model_name']+' on test set....') 
    
    if model_params['model_name'] == 'DPCM':
        return_scores = model_struct.predict_on_batch([Dtest['Dt'], Dtest['Dt'], \
                                 Dtest['ct'], Dtest['ct'], Dtest['ot'], Dtest['ot']])
        return_scores = np.reshape(return_scores[1], (return_scores[1].shape[0], )) #flatten vector
    elif model_params['model_name'] == 'STC': 
        print('before prediction on batch on STC') 
        print('shape: ')
        print(Dtest['Dt'].shape[0])        
        return_scores = model_struct.predict_on_batch([Dtest['Dt'], Dtest['Dt'], \
                                 Dtest['ct'], Dtest['ct'], Dtest['ot'], Dtest['ot']]) 
        print('after prediction on batch on STC')         
        return_scores = np.reshape(return_scores[1], (return_scores[1].shape[0], )) #flatten vector
    elif model_params['model_name'] == 'rlearner': 
        ## one model for order lift and one model for cost drop 
        pred_values_O = model_struct['O_model'].predict(Dtest['Dt']) 
        pred_values_C = model_struct['C_model'].predict(Dtest['Dt']) 
        # [todo: implement 3-factor cost] pred_values_va_rlearner_D = rl_ridge_model_D.predict(Dt) 
        
        return_scores = np.divide(np.maximum(pred_values_O, 0), pred_values_C + 1e-7) 
        #+ d2dlamb * pred_values_va_rlearner_D #pred_values_va_rlearner_O 
    elif model_params['model_name'] == 'slearner': 
        OP = model_struct['O_model'][0].predict(Dtest['Dt'])
        ON = model_struct['O_model'][1].predict(Dtest['Dt'])
        pred_values_O = (OP - ON) 
        CP = model_struct['C_model'][0].predict(Dtest['Dt'])
        CN = model_struct['C_model'][1].predict(Dtest['Dt'])
        pred_values_C = (CP - ON) 
        
        return_scores = np.divide(np.maximum(pred_values_O, 0), pred_values_C + 1e-7) 
    elif model_params['model_name'] == 'custom_model_1': 
        print('placeholder for custom modesl to be added by customer ') 
        return_scores = None 
        
    return return_scores 

def GenerateExperimentResults(list_model_params, dict_model_testset_scores, Dtest): 
    ### generate experiment results through matplotlob 
    ### multiple calls of curve-plotting routines  from Experimention Module
    
    ### Inputs: 
    ###   list_model_params - list of model_params, one for each model to benchmark 
    ###   dict_model_testset_scores - dict() of scores of the testset predicted by each of the model, \
          #key to dict is model_params['model_name'] 
    ###   Dtest - all the data in the test set stored as a dict()
    
    ### Return: N/A 
    
    exp = Experimentation() 
    ci = 0; dict_auccs = dict(); series_percs = dict(); series_cs = dict(); series_os = dict(); list_legends = [] 
    plt.figure(figsize=(8, 6)) 
    for key in dict_model_testset_scores: 
        scores = dict_model_testset_scores[key] 
        if scores is not None:
            exp_return = exp.AUC_cpit_cost_curve_deciles_cohort(scores, Dtest['ot'], Dtest['wt'], (-1.0) * Dtest['ct']) 
            dict_auccs[key] = exp_return[0] 
            series_percs[key] = exp_return[1] 
            series_cs[key] = exp_return[2] 
            series_os[key] = exp_return[3]     
    
    ## --- generate lift-curves for gain as a plot ---- 
    exp.generate_plot(series_percs, series_os, plot_random='lift-curve') 

    ## --- generate lift-curves for cost as a plot ---- 
    exp.generate_plot(series_percs, series_cs, plot_random='lift-curve') 
    
    ## --- generate cost-curves as a plot ----             
    exp.generate_plot(series_cs, series_os, plot_random='cost-curve')
    
    
