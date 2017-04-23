import tensorflow as tf
import numpy as np
import pdb
import os
import sys

import data
import network

config = {
    "seasons_path": "/home/kendall/Development/basketball-db/seasons/",
    "data_path": "/home/kendall/Development/2017/",
    "game_number": int(float(sys.argv[1])),
    "teams_file": "/home/kendall/Development/basketball-db/teams.txt",
    "training_percentage": 1.0,
    "n_input": 22,
    "n_hidden": 16,
    "n_classes": 1,
    "dropout": 1.0,
    "n_steps": int(float(sys.argv[1]))-1,
    "retore_model_path": "./models/"+sys.argv[1]+"/n-hidden-16/",
    "training": False
}

team1_name = sys.argv[2]
team2_name = sys.argv[3]
date = int(float(sys.argv[4]))
vegas_spread = int(float(sys.argv[5]))

try:
    team1 = np.genfromtxt(config["data_path"]+team1_name+".csv", delimiter=",")[:,[0,3,15,16,19,21,24,36,37,40,42,46]]
    team2 = np.genfromtxt(config["data_path"]+team2_name+".csv", delimiter=",")[:,[0,3,15,16,19,21,24,36,37,40,42,46]]
    team1 = team1[::-1,:]
    team2 = team2[::-1,:]

    team2_game_number = np.where(team2[:,0] == date)[0][0]

    team1 = team1[:,1:]
    team2 = team2[:,1:]
except:
    exit()

team1 = team1[0:config["game_number"]+1,:]

if team2_game_number > config["game_number"]:
    team2 = team2[team2_game_number-config["game_number"]:team2_game_number+1,:]
    aggregate_data = np.concatenate((team1, team2), axis=1)
elif team2_game_number < config["game_number"]:
    temp = np.zeros((team1.shape[0], team1.shape[1]))
    temp[config["game_number"]-team2_game_number:config["game_number"]+1,:] = team2[0:team2_game_number+1,:]
    aggregate_data = np.concatenate((team1, temp), axis=1)
else:
    aggregate_data = np.concatenate((team1, team2[0:config["game_number"]+1,:]), axis=1)

ground_truth = team1[config["game_number"],10]
predict_data = aggregate_data[0:aggregate_data.shape[0]-2,:]
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

# model_files = ["n_input-22-run-1/60000", "n_input-22-run-2/60000", \
#     "n_input-22-run-3/60000", "n_input-22-run-4/60000", \
#     "n_input-22-run-5/60000", "n_input-22-run-6/60000", \
#     "n_input-22-run-7/60000"]
model_files = ["40000", "45000", "50000", "55000", "60000"]
preds = []
with tf.Session() as sess:
    for f in model_files:
        saver = tf.train.Saver()
        saver.restore(sess, config["retore_model_path"]+f+".ckpt")

        preds.append(sess.run(pred, feed_dict={x: predict_data, keep_prob: 1.0})[0])
    # print("Prediction: {:.3f}\tVegas: {:.3f}\tGround truth: {:.3f}".format(pred, vegas_spread, ground_truth))
    print("{},{},{}".format(np.mean(preds), ground_truth, vegas_spread))
