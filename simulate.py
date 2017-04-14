import numpy as np
import pdb
import math

actual_spreads = np.random.randint(20, size=1000000)

spreads1 = np.random.randint(20, size=1000000)
spreads2 = np.random.randint(20, size=1000000)

vegas_spreads = []
my_spreads = []
for i in range(actual_spreads.shape[0]):
    if 4 <= math.fabs(actual_spreads[i] - spreads1[i]) <= 12:
        vegas_spreads.append([spreads1[i], actual_spreads[i]])

    if 2 <= math.fabs(actual_spreads[i] - spreads2[i]) <= 6:
        my_spreads.append([spreads2[i], actual_spreads[i]])


my_spreads = np.array(my_spreads)
vegas_spreads = np.array(vegas_spreads)[0:my_spreads.shape[0],:]

my_correct_count = 0
my_count = 0
vegas_correct_count = 0
vegas_count = 0
for i in range(my_spreads.shape[0]):
    if my_spreads[i,0] < my_spreads[i,1]:
        my_correct_count = my_correct_count + 1
    if my_spreads[i,0] != my_spreads[i,1]:
        my_count = my_count + 1

    if vegas_spreads[i,0] < vegas_spreads[i,1]:
        vegas_correct_count = vegas_correct_count + 1
    if vegas_spreads[i,0] != vegas_spreads[i,1]:
        vegas_count = vegas_count + 1

print("My winning accuracy: {}".format(float(my_correct_count)/float(my_count)))
print("Vegas winning accuracy: {}".format(float(vegas_correct_count)/float(vegas_count)))
