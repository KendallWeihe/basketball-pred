import numpy as np
import pdb
import math

reference_data = np.genfromtxt("/home/kendall/Development/nba-basketball-db/accumulated-selected.csv", delimiter=",")
data = np.genfromtxt("/home/kendall/Development/nba-basketball-db/tmp/today.csv", delimiter=",")
pdb.set_trace()

for i in range(data.shape[1]):
    data[:,i] = (data[:,i] - np.min(reference_data[:,i])) / (np.amax(reference_data[:,i]) - np.min(reference_data[:,i]))
    reference_data[:,i] = (reference_data[:,i] - np.min(reference_data[:,i])) / (np.amax(reference_data[:,i]) - np.min(reference_data[:,i]))

difference = []
for i in range(data.shape[0]):
    norms = []
    for j in range(reference_data.shape[0]):
        norm = np.linalg.norm(data[i,:]-reference_data[j,0:16])
        norms.append([norm, reference_data[j,16]])

    idx = np.argpartition(np.array(norms)[:,0], 50)
    # pdb.set_trace()

    spreads = []
    for j in range(50):
        spreads.append(norms[idx[j]][1])
        # print norms[idx[j]][1]

    print("Spread: {}".format(np.mean(spreads)))

    # indices = np.array(norms)[:,0].argsort()
    # avg = []
    # for j in range(30):
    #     # print norms[indices[j]][1]
    #     avg.append(norms[indices[j]][1])
    # print("Spread: {}".format(np.mean(avg)))
