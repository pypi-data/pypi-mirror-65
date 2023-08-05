import tensorflow as tf

def test_tf_ver_f1():
    test = tf.AUTO_REUSE
    print(test) 
    
def test_tf_ver_f2():
    test = tf.compat.v1.AUTO_REUSE
    print(test)
