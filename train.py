import tensorflow as tf
import numpy as np
import pdb

import data
import network

config = {
    "seasons_path": "/home/kendall/Development/basketball-db/seasons/",
    "verification_path": "/home/kendall/Development/2017/",
    "game_number": 23,
    "teams_file": "/home/kendall/Development/basketball-db/teams.txt",
    "training_percentage": 0.95,
    "n_input": 94,
    "n_hidden": 64,
    "n_classes": 1,
    "n_steps": 22,
    "learning_rate": 0.01,
    "batch_size": 60,
    "save_model_path": "./models/23/",
    "save_step": 1000,
    "training_iterations": 1000001,
    "training": True,
    "dropout": 0.75
}

x = tf.placeholder("float", [None, config["n_steps"], config["n_input"]])
y = tf.placeholder("float", [None])
keep_prob = tf.placeholder("float")

weights = {
    'out' : tf.get_variable("weights_1", shape=[config["n_hidden"], config["n_classes"]],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),
}

biases = {
    'out': tf.Variable(tf.zeros([config["n_classes"]]))
}

pred = network.RNN(x, keep_prob, weights, biases, config)
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
    verification_data, verification_ground_truth = d.get_verification_data()

    for iteration in range(config["training_iterations"]):
        start_pos = np.random.randint(len(training_data) - config["batch_size"])
        batch_x = training_data[start_pos:start_pos+config["batch_size"],:,:]
        batch_y = ground_truth[start_pos:start_pos+config["batch_size"]]
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, keep_prob: config["dropout"]})
        train_acc, train_loss = sess.run([accuracy, cost], feed_dict={x: batch_x, y: batch_y, keep_prob: 1.0})

        # samples = sess.run(pred, feed_dict={x: testing_data, keep_prob: 1.0})
        # data.compute_acc(samples, testing_ground_truth, "testing")
        # test_acc, test_loss = sess.run([accuracy, cost], feed_dict={x: testing_data, y: testing_ground_truth, keep_prob: 1.0})

        samples = sess.run(pred, feed_dict={x: verification_data, keep_prob: 1.0})
        data.compute_acc(samples, verification_ground_truth, "verification")
        # verification_acc, verification_loss = sess.run([accuracy, cost], feed_dict={x: verification_data, y: verification_ground_truth, keep_prob: 1.0})

        print("Training\tAcc: {}\tLoss: {}".format(train_acc, train_loss))
        # print("Testing\t\tAcc: {}\tLoss: {}".format(test_acc, test_loss))
        # print("Verification\t\tAcc: {}\tLoss: {}".format(verification_acc, verification_loss))
        print("Iteration: {}\n".format(iteration))

        if iteration % config["save_step"] == 0:
            saver.save(sess, config["save_model_path"]+str(iteration)+".ckpt")
