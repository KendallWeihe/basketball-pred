# TODO:
    # find columns
    # include date
    # start new program to compare to vegas
    #     for each game
    #         find spread from date
    #         include spread in norm data

# TODO:
    # read in team names
    # read in spreads
    # read in norm data
    # for game in norm data:
    #     compute norm
    #     find vegas spread based on date
    #     [norm_pred, actual, vegas]

import os
import pdb
import numpy as np
import math

teamsFile = open("/home/kendall/Development/basketball-db/teams.txt", "r")
teams = teamsFile.read().splitlines()

spread_path = "/home/kendall/Development/basketball-db/spreads/"
spread_files = os.listdir(spread_path)
spreads = []
for f in spread_files:
    spread_data = np.genfromtxt(spread_path + f, delimiter=",")
    if spreads != []:
        spreads = np.concatenate((spreads, spread_data), axis=0)
    else:
        spreads = spread_data

data = np.genfromtxt("/home/kendall/Development/basketball-db/accumulated-selected.csv", delimiter=",")
for i in range(data.shape[1]-3):
    data[:,i] = (data[:,i] - np.min(data[:,i])) / (np.amax(data[:,i]) - np.min(data[:,i]))

difference = []
vegas_difference = []
correct = 0
count = 0
for i in range(data.shape[0]):
    if data[i,17] > 20121100:
        index = np.where(np.logical_and(spreads[:,0] == data[i,17], spreads[:,1] == data[i,18]))[0]

        if index != []:
            # print("Data date:{}\tSpread1 date: {}".format(data[i,17], spreads[index[0],0]))
            # print("Data date:{}\tSpread2 date: {}".format(data[i,17], spreads[index[1],0]))
            # print("Data spread: {}\tSpread1 spread: {}".format(data[i,18], spreads[index[0],1]))
            # print("Data spread: {}\tSpread2 spread: {}".format(data[i,18], spreads[index[1],1]))
            # print("Spread1: {}".format(spreads[index[0],7]))
            # print("Spread1: {}\n".format(spreads[index[1],7]))

            vegas_spread = spreads[index[1],7]

            norms = []
            for j in range(data.shape[0]):
                if i != j:
                    norm = np.linalg.norm(data[i,0:16]-data[j,0:16])
                    norms.append([norm, data[j,16]])

            idx = np.argpartition(np.array(norms)[:,0], 30)

            norm_spreads = []
            for j in range(30):
                norm_spreads.append(norms[idx[j]][1])

            spread1 = data[i,16]
            spread2 = -1*(np.mean(norm_spreads) * 0.93953094110278479 + 0.94037147947698618)
            difference.append(math.fabs(spread1-spread2))
            vegas_difference.append(math.fabs(spread1-vegas_spread))

            if not spread1 <= vegas_spread <= spread2 and not spread1 >= vegas_spread >= spread2:
                correct = correct + 1
            count = count + 1

            print("Spread1: {}\tSpread2: {}\tVegas spread: {}".format(spread1, spread2, vegas_spread))
            print("Percent correct: {}".format(float(correct)/float(count)))
            print("My mean difference: {}".format(np.mean(difference)))
            print("Vegas mean difference: {}".format(np.mean(vegas_difference)))
            print("Game number: {}\n".format(count))
