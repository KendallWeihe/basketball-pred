import tensorflow as tf
import numpy as np
import pdb

import data
import network

config = {
    "seasons_path": "/home/kendall/Development/basketball-db/seasons/",
    "game_number": 15,
    "teams_file": "/home/kendall/Development/basketball-db/teams.txt",
    "training_percentage": 0.85,
    "n_input": 94,
    "n_hidden": 256,
    "n_classes": 1,
    "n_steps": 14,
    "learning_rate": 0.01,
    "batch_size": 60,
    "save_model_path": "./models/15/",
    "save_step": 1000
}

x = tf.placeholder("float", [None, config["n_steps"], config["n_input"]])
y = tf.placeholder("float", [None])

weights = {
    'out' : tf.get_variable("weights_1", shape=[config["n_hidden"], config["n_classes"]],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),
}

biases = {
    'out': tf.Variable(tf.zeros([config["n_classes"]]))
}

pred = network.RNN(x, weights, biases, config)
n_samples = tf.cast(tf.shape(x)[0], tf.float32)
cost = tf.reduce_sum(tf.pow(pred-y, 2))/(2*n_samples)
optimizer = tf.train.AdamOptimizer(learning_rate=config["learning_rate"]).minimize(cost)
accuracy = tf.reduce_mean(tf.abs(tf.sub(pred, y)))

d = data.Data(config)

# Launch the graph
with tf.Session() as sess:
    saver = tf.train.Saver()
    init = tf.global_variables_initializer()
    sess.run(init)
    training_data, ground_truth = d.get_training_data()
    testing_data, testing_ground_truth = d.get_testing_data()

    for iteration in range(100000):
        start_pos = np.random.randint(len(training_data) - config["batch_size"])
        batch_x = training_data[start_pos:start_pos+config["batch_size"],:,:]
        batch_y = ground_truth[start_pos:start_pos+config["batch_size"]]
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
        train_acc, train_loss = sess.run([accuracy, cost], feed_dict={x: batch_x, y: batch_y})

        # start_pos = np.random.randint(len(testing_data) - config["batch_size"])
        # batch_x = testing_data[start_pos:start_pos+config["batch_size"],:,:]
        # batch_y = testing_ground_truth[start_pos:start_pos+config["batch_size"]]
        batch_x = testing_data
        batch_y = testing_ground_truth
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
        test_acc, test_loss = sess.run([accuracy, cost], feed_dict={x: batch_x, y: batch_y})
        samples = sess.run(pred, feed_dict={x: batch_x})
        # print samples
        data.compute_acc(samples, batch_y)

        print("Training\tAcc: {}\tLoss: {}".format(train_acc, train_loss))
        print("Testing\t\tAcc: {}\tLoss: {}".format(test_acc, test_loss))

        if iteration % config["save_step"] == 0:
            saver.save(sess, config["save_model_path"])
