import numpy as np
import pdb
import math

data = np.genfromtxt("/Users/kendallweihe/Google Drive/Development/basketball-db/single-games/mlp-data.csv", delimiter=",")

for i in range(data.shape[1]-1):
    data[:,i] = (data[:,i] - np.min(data[:,i])) / (np.amax(data[:,i]) - np.min(data[:,i]))

difference = []
for i in range(data.shape[0]):
    norms = []
    for j in range(data.shape[0]):
        if i != j:
            norm = np.linalg.norm(data[i,:]-data[j,:])
            norms.append([norm, data[j,22]])

    idx = np.argpartition(np.array(norms)[:,0], 10)

    spreads = []
    for j in range(10):
        spreads.append(norms[idx[j]][1])

    # min_index = np.where(np.array(norms)[:,0] == np.min(np.array(norms)[:,0]))[0][0]
    spread1 = data[i,22]
    # spread2 = norms[min_index][1]
    spread2 = np.mean(spreads)
    difference.append(math.fabs(spread1-spread2))

    # print("Minimum index: {}".format(min_index))
    print("Spread1: {}\tSpread2: {}".format(spread1, spread2))
    print("Game number: {}\tMean: {}".format(i,np.mean(difference)))
