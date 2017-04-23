import tensorflow as tf
from tensorflow.contrib import slim

def MLP(x, keep_prob, config):
    l1 = slim.batch_norm(slim.fully_connected(x, 50, activation_fn=tf.nn.relu))
    l2 = slim.batch_norm(slim.fully_connected(l1, 50, activation_fn=tf.nn.relu))
    l3 = slim.fully_connected(l2, 1, activation_fn=None)
    output = tf.reshape(l3, [-1])
    return tf.nn.dropout(output, keep_prob)
