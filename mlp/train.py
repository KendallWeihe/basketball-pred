import tensorflow as tf
import numpy as np
import pdb
import sys

import data
import network

config = {
    "seasons_path": "/Users/kendallweihe/Google Drive/Development/basketball-db/accumulated/",
    "data_path": "/Users/kendallweihe/Google Drive/Development/basketball-db/single-games/mlp-data.csv",
    "teams_file": "/Users/kendallweihe/Google Drive/Development/basketball-db/teams.txt",
    "training_percentage": 0.85,
    "n_input": 22,
    "n_classes": 1,
    "learning_rate": 0.01,
    "batch_size": 128,
    "save_step": 60000,
    "training_iterations": 1000000,
    "training": True,
    "dropout": 0.75
}

x = tf.placeholder("float", [None, config["n_input"]])
y = tf.placeholder("float", [None])
keep_prob = tf.placeholder("float")

pred = network.MLP(x, keep_prob, config)
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
    # saver = tf.train.Saver()
    # saver.restore(sess, "models/23/n-hidden-16/660000.ckpt")

    training_data, ground_truth = d.get_training_data()
    testing_data, testing_ground_truth = d.get_testing_data()
    pdb.set_trace()

    for iteration in range(config["training_iterations"]):
        start_pos = np.random.randint(len(training_data) - config["batch_size"])
        batch_x = training_data[start_pos:start_pos+config["batch_size"],:]
        batch_y = ground_truth[start_pos:start_pos+config["batch_size"]]

        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, keep_prob: config["dropout"]})

        if iteration % 1000 == 0:
            train_acc, train_loss = sess.run([accuracy, cost], feed_dict={x: batch_x, y: batch_y, keep_prob: 1.0})

            samples = sess.run(pred, feed_dict={x: testing_data, keep_prob: 1.0})
            test_acc, test_loss = sess.run([accuracy, cost], feed_dict={x: testing_data, y: testing_ground_truth, keep_prob: 1.0})
            print(samples[0:100])

            print("Training size: {}".format(training_data.shape[0]))
            print("Training\tAcc: {}\tLoss: {}".format(train_acc, train_loss))
            print("Testing\t\tAcc: {}\tLoss: {}".format(test_acc, test_loss))
            data.compute_acc(samples, testing_ground_truth, "testing")
            print("Iteration: {}\n".format(iteration))

        # if iteration % config["save_step"] == 0:
        #     saver.save(sess, config["save_model_path"]+str(iteration)+".ckpt")
