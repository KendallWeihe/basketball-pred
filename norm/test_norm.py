import numpy as np
import pdb
import math

data = np.genfromtxt("/home/kendall/Development/nba-basketball-db/advanced-accumulated-selected.csv", delimiter=",")
for i in range(data.shape[1]-1):
    data[:,i] = (data[:,i] - np.min(data[:,i])) / (np.amax(data[:,i]) - np.min(data[:,i]))

pdb.set_trace()

# data[:,[0,4,8,12]] = 0.40 * data[:,[0,4,8,12]]
# data[:,[1,5,9,13]] = 0.15 * data[:,[1,5,9,13]]
# data[:,[2,6,10,14]] = 0.20 * data[:,[2,6,10,14]]
# data[:,[3,7,11,15]] = 0.25 * data[:,[3,7,11,15]]

difference = []
plot = []
for i in range(500,5000):
    norms = []
    for j in range(data.shape[0]):
        if i != j:
            norm = np.linalg.norm(data[i,0:16]-data[j,0:16])
            norms.append([norm, data[j,16]])

    # pdb.set_trace()
    idx = np.argpartition(np.array(norms)[:,0], 30)

    spreads = []
    weights = []
    for j in range(30):
        spreads.append(norms[idx[j]][1])
        # print norms[idx[j]][1]
        # weights.append(norms[idx[j]][0])

    # pdb.set_trace()
    spread1 = data[i,16]
    spread2 = np.mean(spreads) * 0.93953094110278479 + 0.94037147947698618

    # numer = np.dot([np.mean(spreads), spread2], [40,40])
    # denom = np.dot([40,40], [40,40])
    # frac = numer / denom
    # spread2 = frac * 40

    # spread2 = np.average(spreads, weights=weights)
    difference.append(math.fabs(spread1-spread2))

    print("Spread1: {}\tSpread2: {}".format(spread1, spread2))
    print("Game number: {}\tMean: {}".format(i,np.mean(difference)))

    plot.append([spread1, spread2])

    # print("{},{}".format(spread1, spread2))

    # indices = np.array(norms)[:,0].argsort()
    # avg = []
    # for j in range(30):
    #     # print norms[indices[j]][1]
    #     avg.append(norms[indices[j]][1])
    # print("Spread: {}".format(np.mean(avg)))

pdb.set_trace()
print

# (Pdb) from scipy import stats
# (Pdb) slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(plot)[:,1], np.array(plot)[:,0])
# (Pdb) p slope
# 0.93953094110278479
# (Pdb) p intercept
# 0.94037147947698618
# (Pdb) p r_value
# 0.37530648258501698


# (Pdb) from scipy import stats
# (Pdb) slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(plot)[:,1], np.array(plot)[:,0])
# (Pdb) p r_value
# 0.41323743775650795
