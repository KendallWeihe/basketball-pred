import numpy as np
import pdb

predictions = np.genfromtxt("./compare-vegas.csv", delimiter=",")

num_correct = 0
for p in predictions:
    if not (p[0] < p[2] < p[1]) and not (p[0] > p[2] > p[1]):
        num_correct = num_correct + 1

print("Winning percentage: {}".format(float(num_correct)/float(predictions.shape[0])))
