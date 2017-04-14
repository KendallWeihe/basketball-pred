import tensorflow as tf
import numpy as np
import pdb
import sys

import data
import network

config = {
    "data_path": "/home/kendall/Development/basketball-db/seasons/2017/",
    "game_number": int(sys.argv[1]),
    "teams_file": "/home/kendall/Development/basketball-db/teams.txt",
    "training_percentage": 1.0,
    "n_input": 94,
    "n_hidden": 256,
    "n_classes": 1,
    "n_steps": int(sys.argv[1])-1,
    "retore_model_path": "./models/"+sys.argv[1]+"/",
}

team1_name = sys.argv[2]
team2_name = sys.argv[3]
team1_index = int(sys.argv[4])
team2_index = int(sys.argv[5])

team1 = np.genfromtxt(config["data_path"]+team1_name+".csv", delimiter=",")
team2 = np.genfromtxt(config["data_path"]+team2_name+".csv", delimiter=",")

ground_truth = team1[config["game_number"],46]

for i in range(team2.shape[0]):
    if team2[i,43] == team1_index:
        team2_game_number = i
        break

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

# -------------------------------------------------------------------

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

# Launch the graph
with tf.Session() as sess:
    saver = tf.train.Saver()
    init = tf.global_variables_initializer()
    sess.run(init)
    saver.restore(sess, "/tmp/model.ckpt")
    # TODO:
        # make prediction
        # compare with ground truth
        # append to prediction.csv file
