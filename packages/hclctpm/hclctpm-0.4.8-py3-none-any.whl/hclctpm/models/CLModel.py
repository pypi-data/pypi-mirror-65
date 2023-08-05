import numpy as np, tensorflow as tf, pandas as pd, h5py, pickle as pkl

class CLModel(): 
    ## CLModel class as a versatile module for Michelangelo 
    """
    Object oriented programming of models as versatile modules. We customize hclctpm.models.clmodel class with custom written model utilities, including model meta-data, weights, methods to train and predict. CL model classes can be abstract models with flexibility of inheritance to  specific R&D models. Overridden methods can be highly efficient cpython routines for  serving,  instantiated through HCL model development environment, pyML (e.g import hclctpm.models.clmodel in model.py), lambdaDL, OPS. This enables the Michelangelo eco-system to utilize the OOP modules in a highly versatile manner. 
    """ 
    def __init__(self, model_params, dataspecs): 
        pass 
    def predict(self, df, datatype = 'dataframe'): 
        pass 

class CLModel_DL(CLModel): 
    ### [TODO]: separate __init__ to definition of TF model
    ### then use  load_model function to perform meanstd loading and weights loading
    ### into the instance, the TF 1.14 solution for DSW stability is temporary 
    
    def __init__(self, model_params, dataspecs): 
        #super(CLDemoModel, self).__init__()  # Don't forget this line 
        
        # All paths should be relative to the root of your model folder.
        print('---> starting to initialize CLModel')
        
        print('---> loading mean and standard deviation')
        filename = dataspecs['hcl_dev_dir'] + '/cl_model/meanstd_deploy_' + dataspecs['prefix']+'.pkl' 
        Dms = pkl.load(open(filename, 'rb')) 
        self.mean_list = Dms['mean_list']
        self.std_list = Dms['std_list']
        
        print('---> loading model weights to deploy')
        filename = dataspecs['hcl_dev_dir'] + '/cl_model/weights_deploy_' + model_params['model_name'] + '_' + dataspecs['prefix']+'.h5'
        
        f = h5py.File(filename, 'r')
        
        prefix = model_params['model_name'] 
        second_key = prefix+'_score_output'
        i = 1 
        while second_key not in f[prefix+'_score_output'].keys():
            second_key = prefix + '_score_output' + '_' + str(i)
            if i > model_params['num_inits']:
                print('Error: could not find the desired output from Keras model, tried all intialization indices') 
                break
            i = i + 1
        
        k1 = f[prefix+'_score_output'][second_key].get('kernel:0')            
        self.model_kernel = np.array(k1)
        
        b1 = f[prefix+'_score_output'][second_key].get('bias:0')
        self.model_bias = np.array(b1)
        
        self.feature_columns = dataspecs['feature_list'] 
    
    def train(self): 
        """Training function 
        """ 
        pass 
    
    def predict(self, df, datatype='dataframe'): 
        """Predict receives data from a query as a pandas dataframe and returns 
        results as a pandas dataframe. 
        """ 
        
        if datatype == 'dataframe': 
            data = df[self.feature_columns].apply(pd.to_numeric, errors='coerce').as_matrix() 
        elif datatype == 'numpyarray': 
            data = df 
        else: 
            print('model predict for datatype : ' + datatype + ' not implemented') 
        
        data = data - np.reshape(self.mean_list, (1, -1))
        data = data / np.reshape(self.std_list, (1, -1))
        data[pd.isnull(data)] = 0.0
        score = np.matmul(data, self.model_kernel) + self.model_bias
        
        if datatype == 'dataframe': 
            df['score'] = score 
        elif datatype == 'numpyarray':
            df = score
        else:
            print('model predict for datatype : ' + datatype + ' not implemented') 
        
        print(' finished clmodel predict, returning ...  ')
        
        return df 
