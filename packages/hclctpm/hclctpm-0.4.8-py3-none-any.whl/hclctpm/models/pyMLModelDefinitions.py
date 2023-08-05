import tensorflow as tf, numpy as np 
from hclctpm.models.CLModel import * 

### consider having functions below in models.AuxiliaryFunctions 
def custom_metric(y_true, y_pred): 
    return tf.keras.backend.mean(y_pred, axis=1) 
def custom_loss(y_true, y_pred): 
    return tf.math.reduce_sum(y_pred, axis=0) 
def dummy_loss(y_true, y_pred): 
    return float(0) 

def TrainCLModel(model_params, Dtrain, Dval, i, graph, sess): 
    ### train CL model depending on the type given in model_params 
    ### support models: 'DPCM' - Dynamic Pooling Constrained Model
    ###                 'STC' - Simple Treatment Control (DL) Model
    
    ### Input: 
    ###   model_params - dictionary of model parameters 
    ###   Dtrain - dict() containing training data 
    ###         used in this function:
    ###             model_params['model_name'],
    ###             model_params['num_optimize_iterations'], 
    ###             if model_params['model_name'] == 'DPCM', access model_params['quantile']
    ###             if model_params['model_name'] == 'DPCM', access model_params['temp']
    ###   i - integer, ith itheration of random initialization (for fix keras naming issue) 
    
    ### Return:
    ###   trained_model - the trained model data structure (keras/sklearn)
    ###   val_loss - validation loss of this model on validation set
    
    model_name = model_params['model_name']
    
    if model_name == 'DPCM': 
        obj, opt, dumh, dumhu, temp, p_quantile = TunableTQRankingModelDNN(graph, \
                                                                           Dtrain['D_tre'], \
                                                                           Dtrain['D_unt'], \
                                                                           Dtrain['o_tre'], \
                                                                           Dtrain['o_unt'], \
                                                                           Dtrain['c_tre'], \
                                                                           Dtrain['c_unt'], \
                                                                           'train-first', \
                                                                           model_params['temp'], \
                                                                           model_params['quantile'], \
                                                                           model_params['num_hidden'], \
                                                                           model_params['use_schedule'])
    else:
        obj, opt, dumh, dumhu, saver = SimpleTCModelDNN(graph, \
                                                 Dtrain['D_tre'], \
                                                 Dtrain['D_unt'], \
                                                 Dtrain['o_tre'], \
                                                 Dtrain['o_unt'], \
                                                 Dtrain['c_tre'], \
                                                 Dtrain['c_unt'], \
                                                 'train-first', \
                                                 model_params['num_hidden']) 
    
    print('->fitting ' + model_name + ' model for '+str(model_params['num_optimize_iterations'])+' iterations')
    
    ### initialize variables and run optimization
    with graph.as_default() as g:
        init = tf.compat.v1.global_variables_initializer()
    sess.run(init)
    
    if model_name == 'DPCM': 
        cur_temp = model_params['temp']
        
    for step in range(model_params['num_optimize_iterations']):
        _, objres = sess.run([opt, obj])
        if step % 300 == 0 and step is not 0:
            print('')
        if step % 100 == 0:
            print('step :' + str(step) + ' obj:%.2f'%objres, end = ' -- ')
            if model_name == 'DPCM': 
                cur_temp = cur_temp + model_params['inc_temp']
                if model_params['use_schedule']:
                    sess.run(temp.assign(cur_temp))
                    print('[temp to :%2f]'%sess.run(temp), end = '--')
    
    if model_name == 'DPCM': 
        objv, optv, dumhv, dumhuv, tempv, p_quantilev = TunableTQRankingModelDNN(graph, \
                                                                                 Dval['D_tre'], \
                                                                                 Dval['D_unt'], \
                                                                                 Dval['o_tre'], \
                                                                                 Dval['o_unt'], \
                                                                                 Dval['c_tre'], \
                                                                                 Dval['c_unt'], \
                                                                                 'validate', \
                                                                                 model_params['temp'], \
                                                                                 model_params['quantile'], \
                                                                                 model_params['num_hidden'],
                                                                                 model_params['use_schedule'])
    else:
        objv, optv, dumhv, dumhuv, saver = SimpleTCModelDNN(graph, \
                                                            Dval['D_tre'], \
                                                            Dval['D_unt'], \
                                                            Dval['o_tre'], \
                                                            Dval['o_unt'], \
                                                            Dval['c_tre'], \
                                                            Dval['c_unt'], \
                                                            'validate', \
                                                            model_params['num_hidden']) 
    
    val_loss = sess.run(objv) 
    return val_loss 

def TrainCLModelTF2(model_params, Dtrain, Dval, i): 
    ### train CL model depending on the type given in model_params 
    ### support models: 'DPCM' - Dynamic Pooling Constrained Model
    ###                 'STC' - Simple Treatment Control (DL) Model
    
    ### Input: 
    ###   model_params - dictionary of model parameters 
    ###   Dtrain - dict() containing training data 
    ###         used in this function:
    ###             model_params['model_name'],
    ###             model_params['num_optimize_iterations'], 
    ###             if model_params['model_name'] == 'DPCM', access model_params['quantile']
    ###             if model_params['model_name'] == 'DPCM', access model_params['temp']
    ###   i - integer, ith itheration of random initialization (for fix keras naming issue) 
    
    ### Return:
    ###   trained_model - the trained model data structure (keras/sklearn)
    ###   val_loss - validation loss of this model on validation set
    
    my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    tf.config.experimental.set_visible_devices(devices= my_devices, device_type='CPU')
    
    intraT = tf.config.threading.get_intra_op_parallelism_threads() 
    interT = tf.config.threading.get_inter_op_parallelism_threads()
    #print('TF threading: intra (' + str(intraT) + '), inter (' + str(interT) + ')')
    if intraT is not 1: 
        tf.config.threading.set_intra_op_parallelism_threads(1)
    if interT is not 1: 
        tf.config.threading.set_inter_op_parallelism_threads(1) 
    
    intraT = tf.config.threading.get_intra_op_parallelism_threads() 
    interT = tf.config.threading.get_inter_op_parallelism_threads() 
    print('   (after set) TF threads: ra (' + str(intraT) + '), er (' + str(interT) + ')')
    
    if model_params['model_name'] == 'DPCM':
        trained_model = DefineKerasDPCMModel(Dtrain['D_tre'].shape[1], 1, Dtrain['D_tre'].shape[0], \
                             activation=tf.nn.tanh, quantile=model_params['quantile'], temp=model_params['temp'])
    elif model_params['model_name'] == 'STC':
        trained_model = DefineKerasSimpleTCModel(Dtrain['D_tre'].shape[1], 1, Dtrain['D_tre'].shape[0], activation=tf.nn.tanh)
    output_prefix = model_params['model_name'] + '_' 
    opt = tf.keras.optimizers.Adam(learning_rate=0.01) 
    
    ### this part is a temporary solution for the naming of output node in Keras 
    if i == 0: 
        main_output_str = 'tf_op_layer_' + output_prefix + 'main_output' 
    else: 
        main_output_str = 'tf_op_layer_' + output_prefix + 'main_output_'+str(i) 
    
    trained_model.compile(loss={main_output_str:custom_loss, output_prefix + 'score_output':dummy_loss}, 
                                   loss_weights={main_output_str:1.0, output_prefix + 'score_output':0.0}, 
                                   optimizer=opt) 
    
    y_train_zeros = np.zeros((Dtrain['D_tre'].shape[0], 1)) ## used to create absolute difference to zero and minimize 
    y_val_zeros = np.zeros((Dval['D_tre'].shape[0], 1)) ## used to create absolute difference to zero and minimize
    print('->fitting model for '+str(model_params['num_optimize_iterations'])+' iterations')
    
    history = trained_model.fit([\
                                 Dtrain['D_tre'], Dtrain['D_unt'], \
                                 Dtrain['c_tre'], Dtrain['c_unt'], \
                                 Dtrain['o_tre'], Dtrain['o_unt'] \
                                ],\
                                [y_train_zeros, y_train_zeros], \
                                validation_data=[[Dval['D_tre'], Dval['D_unt'], \
                                                  Dval['c_tre'], Dval['c_unt'], \
                                                  Dval['o_tre'], Dval['o_unt']], \
                                                 [y_val_zeros, y_val_zeros]\
                                ], \
                                batch_size=Dtrain['D_tre'].shape[0], \
                                epochs=model_params['num_optimize_iterations'], \
                                validation_freq=model_params['num_optimize_iterations'], ## not much need to be customized \
                                verbose=0)
    
    return trained_model, history.history['val_loss'][-1]

def DefineKerasSimpleTCModel(input_dim, num_hidden, sample_size, activation=tf.nn.tanh): 
    ## define the simple TC model from scratch
    
    inputs_tr = tf.keras.Input(shape=(input_dim,)) 
    inputs_co = tf.keras.Input(shape=(input_dim,)) 
    #print('inputs_tr :' + str(inputs_tr.shape)) 
    
    c_tr = tf.keras.Input(shape=(1,)) 
    c_co = tf.keras.Input(shape=(1,)) 
    g_tr = tf.keras.Input(shape=(1,)) 
    g_co = tf.keras.Input(shape=(1,)) 
    
    weight_layer = tf.keras.layers.Dense(num_hidden,  input_shape=(input_dim,), activation=activation, name='STC_score_output') 
    x_tr = weight_layer(inputs_tr) 
    x_co = weight_layer(inputs_co) 
    #print('x_tr :' + str(x_tr.shape))
    
    scores = x_tr
    
    sm_layer_batchaxis = tf.keras.layers.Softmax(axis=0) 
    
    s_tr = sm_layer_batchaxis(x_tr) 
    s_co = sm_layer_batchaxis(x_co) 
    #print('s_tr :' + str(s_tr.shape))
    
    dc_tr = tf.reduce_sum(tf.multiply(s_tr, c_tr), axis=0) 
    dc_co = tf.reduce_sum(tf.multiply(s_co, c_co), axis=0) 
    
    dg_tr = tf.reduce_sum(tf.multiply(s_tr, g_tr), axis=0) 
    dg_co = tf.reduce_sum(tf.multiply(s_co, g_co), axis=0) 
    
    #print('dc_tr :' + str(dc_tr.shape))
    #print('dg_tr :' + str(dg_tr.shape))
    
    outputs = tf.divide(dc_tr - dc_co, dg_tr - dg_co, name='STC_main_output') 
    
    #print('outputs :')
    #print(outputs)
    
    #print('outputs size : ' + str(outputs.shape))
    
    model = tf.keras.Model(inputs=[inputs_tr, inputs_co, c_tr, c_co, g_tr, g_co], outputs=[outputs, scores]) 
    return model 

def DefineKerasDPCMModel(input_dim, num_hidden, sample_size, activation=tf.nn.tanh, quantile=0.3, temp=2.0): 
    ## define the simple TC model from scratch 
    
    inputs_tr = tf.keras.Input(shape=(input_dim,)) 
    inputs_co = tf.keras.Input(shape=(input_dim,)) 
    #print('inputs_tr :' + str(inputs_tr.shape))
    
    c_tr = tf.keras.Input(shape=(1,)) 
    c_co = tf.keras.Input(shape=(1,)) 
    g_tr = tf.keras.Input(shape=(1,)) 
    g_co = tf.keras.Input(shape=(1,)) 
    
    weight_layer = tf.keras.layers.Dense(num_hidden, input_shape=(input_dim,), activation=activation, name='DPCM_score_output') 
    x_tr = weight_layer(inputs_tr) 
    x_co = weight_layer(inputs_co) 
    #print('x_tr :' + str(x_tr.shape))
    
    scores = x_tr
    
    ### adopt a sorting operator that's also differentiable 
    ### for application of back-propagation and gradient optimization 
    h_tre_sorted = tf.sort(x_tr, axis=0, direction='DESCENDING') 
    h_unt_sorted = tf.sort(x_co, axis=0, direction='DESCENDING') 
    
    top_k_tre = tf.cast(tf.math.ceil(sample_size * quantile), tf.int32) 
    top_k_unt = tf.cast(tf.math.ceil(sample_size * quantile), tf.int32) 
    
    intercept_tre = tf.slice(h_tre_sorted, [top_k_tre - 1, 0], [1, 1]) 
    intercept_unt = tf.slice(h_unt_sorted, [top_k_unt - 1, 0], [1, 1]) 
    
    ### stop gradients at the tunable intercept for sigmoid 
    ### to stabilize gradient-based optimization 
    intercept_tre = tf.stop_gradient(intercept_tre) 
    intercept_unt = tf.stop_gradient(intercept_unt) 
    
    ### use sigmoid to threshold top-k candidates 
    h_tr = tf.math.sigmoid(temp * (x_tr - intercept_tre)) 
    h_co = tf.math.sigmoid(temp * (x_co - intercept_unt)) 
    
    sm_layer_batchaxis = tf.keras.layers.Softmax(axis=0) 
    
    s_tr = sm_layer_batchaxis(h_tr) 
    s_co = sm_layer_batchaxis(h_co) 
    #print('s_tr :' + str(s_tr.shape)) 
    
    dc_tr = tf.reduce_sum(tf.multiply(s_tr, c_tr), axis=0) 
    dc_co = tf.reduce_sum(tf.multiply(s_co, c_co), axis=0) 
    
    dg_tr = tf.reduce_sum(tf.multiply(s_tr, g_tr), axis=0) 
    dg_co = tf.reduce_sum(tf.multiply(s_co, g_co), axis=0) 
    
    #print('dc_tr :' + str(dc_tr.shape))
    #print('dg_tr :' + str(dg_tr.shape))
    
    outputs = tf.divide(dc_tr - dc_co, dg_tr - dg_co, name='DPCM_main_output') 
    
    #print('outputs :') 
    #print(outputs) 
    
    #print('outputs size : ' + str(outputs.shape)) 
    
    model = tf.keras.Model(inputs=[inputs_tr, inputs_co, c_tr, c_co, g_tr, g_co], outputs=[outputs, scores]) 
    return model 

def forwardSimpleTCModelDNN(Dt, num_hidden): 
    if num_hidden > 0: 
        with tf.compat.v1.variable_scope("drmhidden") as scope: 
            h1_test = tf.contrib.layers.fully_connected(Dt, num_hidden, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
        with tf.compat.v1.variable_scope("drmranker") as scope: 
            h_test = tf.contrib.layers.fully_connected(h1_test, 1, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope) 
    else: 
        with tf.compat.v1.variable_scope("drmranker") as scope: 
            h_test = tf.contrib.layers.fully_connected(Dt, 1, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope) 
    return h_test 

def SimpleTCModelDNN(graph, D_tre, D_unt, o_tre, o_unt, c_tre, c_unt, idstr, num_hidden): 
    
    ## implements the Direct Ranking Model based on CPIT 
    ## D_tre: user context features for treatment 
    ## D_unt: user context features for control (untreated) 
    ## o_tre: user next week order labels for treatment 
    ## o_unt: user next week order labels for control (untreated) 
    ## c_tre: user next week cost(negative net-inflow/variable contribution) labels for treatment 
    ## c_unt: user next week cost(negative net-inflow/variable contribution) labels for control (untreated)  
    ## idstr: a string to indicate whether function is used for train/val, avoid tensorflor parameter re-use 
    
    ## returns: 
    ## obj, objective node 
    ## opt, optimizer node 
    ## h_tre_rnkscore, ranker scores for treated users 
    ## h_unt_rnkscore, ranker scores for control users 
    
    ## define size of cohort datasets 
    size_tre = D_tre.shape[0] 
    size_unt = D_unt.shape[0] 
    
    with graph.as_default() as g: 
        ### ------ define model graph of direct ranking ------ 
        
        ### define ranker/scorer with one or more layers 
        if num_hidden > 0: 
            with tf.compat.v1.variable_scope("drmhidden") as scope: 
                h1_tre = tf.contrib.layers.fully_connected(D_tre, num_hidden, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
                h1_unt = tf.contrib.layers.fully_connected(D_unt, num_hidden, activation_fn=tf.nn.tanh, reuse=True, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
            with tf.compat.v1.variable_scope("drmranker") as scope: 
                h_tre_rnkscore = tf.contrib.layers.fully_connected(h1_tre, 1, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope) 
                h_unt_rnkscore = tf.contrib.layers.fully_connected(h1_unt, 1, activation_fn=tf.nn.tanh, reuse=True, scope=scope) 
        else: 
            with tf.compat.v1.variable_scope("drmranker") as scope: 
                h_tre_rnkscore = tf.contrib.layers.fully_connected(D_tre, 1, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope) 
                h_unt_rnkscore = tf.contrib.layers.fully_connected(D_unt, 1, activation_fn=tf.nn.tanh, reuse=True, scope=scope) 
        
        ### use softmax normalization and weighted reduce-sum for 
        ### compute of expected value of treatment effects 
        s_tre = tf.nn.softmax(h_tre_rnkscore, axis=0) 
        s_unt = tf.nn.softmax(h_unt_rnkscore, axis=0) 
        
        s_tre = tf.reshape(s_tre, (size_tre, )) 
        s_unt = tf.reshape(s_unt, (size_unt, )) 
        
        dc_tre = tf.reduce_sum(tf.multiply(s_tre, c_tre)) 
        dc_unt = tf.reduce_sum(tf.multiply(s_unt, c_unt)) 
        
        do_mult_tre = tf.multiply(s_tre, o_tre) 
        do_mult_unt = tf.multiply(s_unt, o_unt) 
        
        do_tre = tf.reduce_sum(do_mult_tre) 
        do_unt = tf.reduce_sum(do_mult_unt) 
        
        ### implement the cost-gain effectiveness objective 
        obj = tf.divide(dc_tre - dc_unt, do_tre - do_unt)         
        
        ### for application/production purposes, the above equation is more interpretable 
        ### and works well for most datasets, below is 
        ### an option to use relu, and math.log to ensure the objective is differentiable         
        #obj = tf.divide(tf.nn.leaky_relu(dc_tre - dc_unt), tf.nn.leaky_relu(do_tre - do_unt)) 
        #obj = tf.subtract(tf.math.log(tf.nn.leaky_relu(dc_tre - dc_unt)), tf.math.log(tf.nn.leaky_relu(do_tre - do_unt)))
        
        with tf.compat.v1.variable_scope("optimizer" + idstr) as scope: 
            opt = tf.compat.v1.train.AdamOptimizer().minimize(obj) 
        saver = tf.compat.v1.train.Saver()         
        return obj, opt, h_tre_rnkscore, h_unt_rnkscore, saver 

def forwardTunableTQRankingModelDNN(Dtest, num_hidden):
    if num_hidden > 0: 
        with tf.compat.v1.variable_scope("tqrhidden") as scope: 
            h1 = tf.contrib.layers.fully_connected(Dtest, num_hidden, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
        with tf.compat.v1.variable_scope("tqranker") as scope: 
            htest = tf.contrib.layers.fully_connected(h1, 1, activation_fn=None, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
    else: 
        with tf.compat.v1.variable_scope("tqranker") as scope: 
            htest = tf.contrib.layers.fully_connected(Dtest, 1, activation_fn=None, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer())
    return htest 

def TunableTQRankingModelDNN(graph, D_tre, D_unt, o_tre, o_unt, c_tre, c_unt, idstr, initial_temp, p_quantile, num_hidden, use_schedule=False): 
    ## implements the top-p-quantile operator for Constrained Ranking Model 
    ## with tunable temperature through gradient descent and temperature schedule 
    ## D_tre: user context features for treatment 
    ## D_unt: user context features for control (untreated) 
    ## o_tre: user next week order labels for treatment 
    ## o_unt: user next week order labels for control (untreated) 
    ## c_tre: user next week cost(negative net-inflow/variable contribution) labels for treatment 
    ## c_unt: user next week cost(negative net-inflow/variable contribution) labels for control (untreated)  
    ## p_quantile: the top-p-quantile number between (0, 1) 
    ## idstr: a string to indicate whether function is used for train/val, avoid tensorflor parameter re-use 
    ## initial_temp: initial temperature (this is tunable) of the sigmoid governing p_quantile cut-off 
    
    ## returns: 
    ## obj, objective node 
    ## opt, optimizer node 
    ## h_tre_rnkscore, ranker scores for treated users 
    ## h_unt_rnkscore, ranker scores for control users 
    
    ## Consider the contrast TQRanking Model 
    ## as opposed to improving cpit upon control cohort, 
    ## [E(Ctqr) - E(Cctrl)] / [E(Ttqr) - E(Tctrl)] 
    ## let's think about improving cpit upon treatment cohort 
    ## [E(Ctqr) - E(Ctre)] / [E(Ttqr) - E(Ttre)] 
    ## or, let's think about improving upon DRM 
    ## 
    
    ## temperature of the sigmoid governing p_quantile cut-off 
    with graph.as_default() as g: 
        #if use_schedule == False: 
        init = tf.constant(initial_temp, dtype=tf.float64) 
        with tf.compat.v1.variable_scope("temp", reuse=tf.compat.v1.AUTO_REUSE) as scope: 
            temp = tf.compat.v1.get_variable('temp', initializer=init, dtype=tf.float64) 
        ### ---- the following code makes the temperature tunable ---- 
        ### deleted for use of temperature schedule, but keep for future applications 
        #else: 
        #    temp = tf.constant(initial_temp, dtype=tf.float64) 
            #tf.Variable(2.5, dtype=tf.float64, trainable=True) 
        #init2 = tf.constant(p_quantile, dtype=tf.float64) 
        #with tf.compat.v1.variable_scope("p_quantile", reuse=tf.compat.v1.AUTO_REUSE) as scope: 
        #    p_quantile = tf.get_variable('p_quantile', initializer=init2, dtype=tf.float64)
            #tf.Variable(0.3, dtype=tf.float32, trainable=True, reuse=tf.compat.v1.AUTO_REUSE)
        
        ## define size of cohort datasets 
        size_tre = D_tre.shape[0] 
        size_unt = D_unt.shape[0] 
        
        ### ----- define model graph of Top Quantile Constrained ranking ----- 

        ### we can define either a linear or a multi-layer neural network 
        ### for the ranker or scorer 
        if num_hidden > 0: 
            with tf.compat.v1.variable_scope("tqrhidden") as scope: 
                h1_tre = tf.contrib.layers.fully_connected(D_tre, num_hidden, activation_fn=tf.nn.tanh, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
                h1_unt = tf.contrib.layers.fully_connected(D_unt, num_hidden, activation_fn=tf.nn.tanh, reuse=True, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
            with tf.compat.v1.variable_scope("tqranker") as scope: 
                h_tre_rnkscore = tf.contrib.layers.fully_connected(h1_tre, 1, activation_fn=None, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
                h_unt_rnkscore = tf.contrib.layers.fully_connected(h1_unt, 1, activation_fn=None, reuse=True, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
        else: 
            with tf.compat.v1.variable_scope("tqranker") as scope: 
                h_tre_rnkscore = tf.contrib.layers.fully_connected(D_tre, 1, activation_fn=None, reuse=tf.compat.v1.AUTO_REUSE, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
                h_unt_rnkscore = tf.contrib.layers.fully_connected(D_unt, 1, activation_fn=None, reuse=True, scope=scope, weights_initializer=tf.contrib.layers.xavier_initializer()) 
        
        ### adopt a sorting operator that's also differentiable 
        ### for application of back-propagation and gradient optimization 
        h_tre_sorted = tf.contrib.framework.sort(h_tre_rnkscore, axis=0, direction='DESCENDING') 
        h_unt_sorted = tf.contrib.framework.sort(h_unt_rnkscore, axis=0, direction='DESCENDING') 
        
        top_k_tre = tf.cast(tf.math.ceil(size_tre * p_quantile), tf.int32) 
        top_k_unt = tf.cast(tf.math.ceil(size_unt * p_quantile), tf.int32) 
        
        intercept_tre = tf.slice(h_tre_sorted, [top_k_tre - 1, 0], [1, 1]) 
        intercept_unt = tf.slice(h_unt_sorted, [top_k_unt - 1, 0], [1, 1]) 
        
        ### stop gradients at the tunable intercept for sigmoid 
        ### to stabilize gradient-based optimization 
        intercept_tre = tf.stop_gradient(intercept_tre) 
        intercept_unt = tf.stop_gradient(intercept_unt) 
        
        ### use sigmoid to threshold top-k candidates, or use more sophisticated hinge loss 
        h_tre = tf.sigmoid(temp * (h_tre_rnkscore - intercept_tre)) 
        h_unt = tf.sigmoid(temp * (h_unt_rnkscore - intercept_unt)) 
        
        ### using softmax and weighted reduce-sum to compute the expected value 
        ### of treatment effect functions 
        s_tre = tf.nn.softmax(h_tre, axis=0) 
        s_unt = tf.nn.softmax(h_unt, axis=0) 
        
        s_tre = tf.reshape(s_tre, (size_tre, ))
        s_unt = tf.reshape(s_unt, (size_unt, ))
        
        dc_tre = tf.reduce_sum(tf.multiply(s_tre, c_tre)) 
        dc_unt = tf.reduce_sum(tf.multiply(s_unt, c_unt)) 
        
        do_mult_tre = tf.multiply(s_tre, o_tre) 
        do_mult_unt = tf.multiply(s_unt, o_unt) 
        
        do_tre = tf.reduce_sum(do_mult_tre) 
        do_unt = tf.reduce_sum(do_mult_unt) 
        
        ### implement the cost-gain effectiveness objective 
        obj = tf.divide(dc_tre - dc_unt, do_tre - do_unt) 
        ### for application/production purposes, the above equation is more interpretable 
        ### and works well for most datasets, below is 
        ### an option to use relu, and math.log to ensure the objective is differentiable 
        #obj = tf.divide(tf.nn.leaky_relu(dc_tre - dc_unt), tf.nn.leaky_relu(do_tre - do_unt)) 
        #obj = tf.subtract(tf.math.log(tf.nn.leaky_relu(dc_tre - dc_unt)), tf.math.log(tf.nn.leaky_relu(do_tre - do_unt)))
        
        with tf.compat.v1.variable_scope("optimizer" + idstr) as scope: 
            opt = tf.compat.v1.train.AdamOptimizer().minimize(obj) 
    
    return obj, opt, h_tre_rnkscore, h_unt_rnkscore, temp, p_quantile 
