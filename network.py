import tensorflow as tf
from tensorflow.contrib import slim
from tensorflow.python.ops import rnn, rnn_cell

def RNN(x, keep_prob, weights, biases, config):
    x = tf.transpose(x, [1, 0, 2])
    x = tf.reshape(x, [-1, config["n_input"]])
    x = tf.split(0, config["n_steps"], x)
    lstm_cell = rnn_cell.BasicLSTMCell(config["n_hidden"], forget_bias=1.0)
    outputs, states = rnn.rnn(lstm_cell, x, dtype=tf.float32)
    # all_lstm_outputs = tf.reshape(tf.stack(outputs, axis=1), [-1, config["n_steps"]*config["n_hidden"]])
    output = tf.matmul(outputs[-1], weights['out']) + biases['out']

    # l1 = slim.batch_norm(slim.fully_connected(outputs[-1], 50))
    # l2 = slim.batch_norm(slim.fully_connected(l1, 50))
    # output = slim.fully_connected(l2, 1, activation_fn=None)

    # output = slim.fully_connected(outputs[-1], 1, activation_fn=None)
    output = tf.reshape(output, [-1])
    return tf.nn.dropout(output, keep_prob)
