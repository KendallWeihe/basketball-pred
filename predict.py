import tensorflow as tf
import numpy as np
import pdb
import os
import sys

import data
import network

config = {
    "seasons_path": "/Users/kendallweihe/Google Drive/Development/basketball-db/seasons/",
    "data_path": "/Users/kendallweihe/Google Drive/Development/2017/",
    "game_number": int(float(sys.argv[1])),
    "teams_file": "/Users/kendallweihe/Google Drive/Development/basketball-db/teams.txt",
    "training_percentage": 1.0,
    "n_input": 94,
    "n_hidden": 256,
    "n_classes": 1,
    "dropout": 1.0,
    "n_steps": int(float(sys.argv[1]))-1,
    "retore_model_path": "./models/"+sys.argv[1]+"/",
    "training": False
}

team1_name = sys.argv[2]
team2_name = sys.argv[3]
date = int(float(sys.argv[4]))
vegas_spread = int(float(sys.argv[5]))

try:
    team1 = np.genfromtxt(config["data_path"]+team1_name+".csv", delimiter=",")
    team2 = np.genfromtxt(config["data_path"]+team2_name+".csv", delimiter=",")
    team1 = team1[::-1,:]
    team2 = team2[::-1,:]

    ground_truth = team1[config["game_number"],46]
    team2_game_number = np.where(team2[:,0] == date)[0][0]
except:
    exit()

team1 = team1[0:config["game_number"],:]
if team2_game_number > config["game_number"]:
    team2 = team2[team2_game_number-config["game_number"]:team2_game_number,:]
    aggregate_data = np.concatenate((team1, team2), axis=1)
elif team2_game_number < config["game_number"]:
    temp = np.zeros((config["game_number"], team1.shape[1]))
    temp[config["game_number"]-team2_game_number:config["game_number"],:] = team2[0:team2_game_number,:]
    aggregate_data = np.concatenate((team1, temp), axis=1)
else:
    aggregate_data = np.concatenate((team1, team2[0:config["game_number"],:]), axis=1)

predict_data = aggregate_data[0:aggregate_data.shape[0]-1,:]
d = data.Data(config)

raw_data = d.get_raw_data()
for i in range(predict_data.shape[1]):
    predict_data[:,i] = (predict_data[:,i] - np.min(raw_data[:,:,i])) / (np.amax(raw_data[:,:,i]) - np.min(raw_data[:,:,i]))
predict_data = np.expand_dims(predict_data, axis=0)

# -------------------------------------------------------------------

x = tf.placeholder("float", [None, config["n_steps"], config["n_input"]])
keep_prob = tf.placeholder("float")

weights = {
    'out' : tf.get_variable("weights_1", shape=[config["n_hidden"], config["n_classes"]],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),
}

biases = {
    'out': tf.Variable(tf.zeros([config["n_classes"]]))
}

pred = network.RNN(x, keep_prob, weights, biases, config)

# Launch the graph
with tf.Session() as sess:
    saver = tf.train.Saver()
    saver.restore(sess, config["retore_model_path"]+"20000.ckpt")

    pred = sess.run(pred, feed_dict={x: predict_data, keep_prob: 1.0})[0]
    # print("Prediction: {:.3f}\tVegas: {:.3f}\tGround truth: {:.3f}".format(pred, vegas_spread, ground_truth))
    print("{},{},{}".format(pred, ground_truth, vegas_spread))
