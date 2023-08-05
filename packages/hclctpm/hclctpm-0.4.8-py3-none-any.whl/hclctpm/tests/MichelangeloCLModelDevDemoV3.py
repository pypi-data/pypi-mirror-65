#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### Michelangelo Causal Learning Infra. 
### -- Model development Environment, constructed using UserCustomFunctions and ModelDev-API's 

## leveverage user-customizable models and Michelangelo CL's 
## ModelDev-API's to develop causal learning models, compare and benchmark them 


# In[2]:


#!sh ../../testpy3/bin/activate
#!install_package_python3.sh scikit-learn=0.20
#!install_package_python3.sh hclctpm=0.4.0
#!install_package_python3.sh scipy=1.4.1
import tensorflow as tf
print(tf.__version__)


# In[3]:


#!/usr/bin/env python 
# coding: utf-8 

import pandas as pd, numpy as np, pickle as pkl, sys, os, tensorflow as tf, matplotlib.pyplot as plt 
#from queryrunner_client import Client 

### ------ import models, functions from Heterogeneous Causal Learning CTPM package ------- 
from hclctpm.models.pyMLModelDefinitions import * 
from hclctpm.dataprep.DataProcFunctions import * 
from hclctpm.exp.Experimentation import * 
from hclctpm.models.PromotionModels import * 

## User customizable ModelingUtils module 
sys.path.append('..')
from ModelingUtils import * 
from QueryFunctions import * 

experiment_prefix = 'test_r2e_data_presto_macl_demo_v3_r1'

### - definitions for models to use 
dpcm_params = dict ({
 'model_name':'STC', \
 'quantile':0.3, ## quantile constraint at a top percentage \
 'use_schedule':True, ## use constraint annealing schedule \
 'temp':2.0, ##initial temperature of the DPCM \
 'inc_temp':0.1, ##incremental temperature per 100 iterations\
 'num_optimize_iterations':30,\
 'num_inits':2, \
 'save_model_filename_for_deploy':'cl_model/weights_deploy.h5', \
})

### R-learner Quasi-oracle estimation model 
rlearner_params = dict({ 'model_name':'rlearner', })

### S-learner Quasi-oracle estimation model 
slearner_params = dict({ 'model_name':'slearner', })

### - data and metric/loss specs
dataspecs = dict({  'use_query': True,   'saved_csv': '../../data/r2e_gb_test_data.csv',   'data_query': r2e_marketing_data_presto(),   'cohort_column_name': 'cohort',   'treatment_indicator_value': 'treatment',   'control_indicator_value': 'control',   'prefix': experiment_prefix, ##the prefix to store model and save names \
  'data_filename': '../data/' + experiment_prefix + '.pkl', ## path and filename to data\
  'sample_frac': 0.2, ##random sample fraction of the dataset\
  'use_intensity': False, \
  'use_matching_data': False, \
  'save_meanstd_filename_for_deploy':'cl_model/meanstd_deploy.pkl',\
  'feature_list': [ 
        'rating_2driver_min_avg_84d'
        , 'trip_incomplete_total_84d'
        , 'days_active_84d'
        , 'days_since_trip_first_lifetime'
        , 'days_since_last_hard_churn_lifetime'
        , 'days_since_last_soft_churn_lifetime'
        , 'fare_max_sd_84d'
        , 'churns_hard_lifetime'
        , 'trips_lifetime'
        , 'fare_max_p50_84d'
        , 'duration_session_pre_request_max_p50_84d'
        , 'trip_pool_per_x_84d'
        , 'fare_total_win7d_sd_84d'
        , 'trip_complete_win7d_sd_84d'
        , 'session_per_days_active_84d'
        , 'churns_soft_lifetime'
        , 'trip_complete_per_days_active_84d'
        , 'trip_pool_prc_84d'
        , 'session_background_pre_request_prc_84d'
        , 'session_lt_1m_prc_84d'
        , 'session_request_prc_84d'
        , 'duration_session_outside_total_prc_84d'
        , 'trip_x_prc_84d'
        , 'days_since_trip_last_lifetime'
        , 'has_session_request_84d'
        , 'has_session_without_request_84d'
        , 'promo_used_84d' 
        , 'fare_promo_total_avg_84d', 
        'fare_total_avg_84d', 
        'surge_trip_avg_84d', 
        'fare_total_win7d_potential_84d', 
        'fare_total_win28d_potential_84d', 
        'fare_lifetime', 
        'time_to_first_message_minutes_mean_lifetime', 
        'ata_trip_max_avg_84d', 
        'eta_trip_max_avg_84d', 
        'trip_pool_matched_avg_84d', 
        'payment_cash_trip_total_84d', 
        'duration_trip_total_p50_84d' 
    ], \
    'label_list':[ 
        'manual_apply_gb', 
        'manual_apply_ni' 
    ] \
})

metricspecs = dict({  'type':'divplus', ##divplus:M1/M2+lambda*M3, timesminus:M3*(M1-lambda*M2)\
  'lambdaweight':0.0 ##lambda in the metric definitions\
})


# In[4]:


#### query data using Presto 
#QueryDataSaveFile(dataspecs, verbose=True)


# In[5]:


#### one simple function to benchmark multiple causal learning models 

BenchmarkModels([rlearner_params, slearner_params], dataspecs, metricspecs) 


# In[ ]:





# In[6]:


#### One function to benchmark multiple models and algorithms 

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
    
    ### load training data using library modules 
    Dtrain, Dval, Dtest = CLDataPreparation(dataspecs) 
    
    ### store results and best models 
    val_results = dict(); dict_best_models = dict(); dict_model_testset_scores = dict() 
    
    ### Model Development for Causal Learning: 
    ### train multiple methodologies in causal learning 
    for mi in range(len(list_model_params)): 
        dict_best_models[list_model_params[mi]['model_name']] = TrainModelWithValidation(list_model_params[mi], Dtrain, Dval) 
    
    ### predict and plot out results from multiple methodologies in causal learning 
    for mi in range(len(list_model_params)): 
        dict_model_testset_scores[list_model_params[mi]['model_name']] = PredictTestSetScores(list_model_params[mi], Dtest,                                                                                               dict_best_models[list_model_params[mi]['model_name']]) 
    
    ### plot experiment results 
    GenerateExperimentResults(list_model_params, dict_model_testset_scores, Dtest) 


# In[7]:


### user custom defined hyper-parameter selection functions 

def HPSelectMultiRandomInitializeTrainModel(model_params, Dtrain, Dval):
    ### for-loop multiple random initializations of the same model                                                                                                                                                                                             
    ### Input:                                                                                                                                                                                                                                                 
    ### model_params - dictionary of model parameters                                                                                                                                                                                                          
    ### Dtrain - dict containing all data for training                                                                                                                                                                                                         
    ### Dval - dict containing all data for validation                                                                                                                                                                                                         
    ### Return:                                                                                                                                                                                                                                                
    ### list of models from each random initialization                                                                                                                                                                                                         

    print('------> Training ' + model_params['model_name'] + ' models with multiple random initializations .... ')
    list_raninit_models = []
    list_val_results = []
    for i in range(model_params['num_inits']):
        print('--> random initialization iteration: '+str(i))
        ## re-implemented deep learning models in Keras and TF 2.0                                                                                                                                                                                             
        trained_model, history = TrainCLModel(model_params, Dtrain) 
        list_raninit_models.append(trained_model) 
        print('->training finished')
        list_val_results.append(history.history['val_loss'][-1]) ## get the most recent validation result                                                                                                                                                      

    best_index = min(enumerate(list_val_results), key=itemgetter(1))[0]
    print('--> best performing model: iteration ' + str(best_index) +' with val result:'+str(list_val_results[best_index])+' out of:')
    print(list_val_results)
    best_model = list_raninit_models[best_index]

    return best_model


# In[8]:


#### Define experimentation, plotting, and cohort level metric predictions 

def GenerateExperimentResults(list_model_params, dict_model_testset_scores, Dtest): 
    ### generate experiment results through matplotlob 
    ### multiple calls of curve-plotting routines  from Experimention Module 
    exp = Experimentation() 
    ci = 0 
    colors = ['r', 'b', 'c', 'g', 'k', 'y', 'm'] 
    dict_auccs = dict() 
    list_legends = [] 
    plt.figure(figsize=(18, 12)) 
    exp.AUC_cost_curve_plot_random() 
    for key in dict_model_testset_scores: 
        scores = dict_model_testset_scores[key] 
        if scores is not None: 
            dict_auccs[key], series_c, series_o = exp.AUC_cpit_cost_curve_deciles_cohort(scores, Dtest['ot'], Dtest['wt'], (-1.0) * Dtest['ct'], colors[ci])
            if ci == len(colors):
                ci = 0
            else:
                ci = ci + 1
    
    list_legends.append('Random') 
    for key in dict_model_testset_scores:
        list_legends.append(key)
        print(key + ' model AUC: ' + str(dict_auccs[key]))
    plt.legend(list_legends)
    plt.show()


# In[ ]:




