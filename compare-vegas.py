import numpy as np
import pdb
import math
import os

# predictions = np.genfromtxt("./compare-vegas.csv", delimiter=",")
predictions = None
files = os.listdir("./predictions/")
for f in files:
    # if "-8.csv" in f:
    # if "2017" in f:
    if predictions is None:
        predictions = np.genfromtxt("./predictions/"+f, delimiter=",")
    else:
        predictions = np.concatenate((predictions, np.genfromtxt("./predictions/"+f, delimiter=",")), axis=0)

for i in range(1,15):
    total_count = 0
    spread_correct = 0
    confident_scale = i
    confident_correct = 0
    confident_count = 0
    winning_team = 0
    confident_winning_team = 0
    avg_diff = 0
    avg_vegas_diff = 0
    for p in predictions:
        # pdb.set_trace()
        # p[0] = (p[0] + p[2]) / 2

        if not (p[0] < p[2] < p[1]) and not (p[0] > p[2] > p[1]):
            spread_correct = spread_correct + 1
        if (p[0] < 0 and p[1] < 0) or (p[0] > 0 and p[1] > 0):
            winning_team = winning_team + 1

        if math.fabs(p[0] - p[2]) >= confident_scale:
            if not (p[0] < p[2] < p[1]) and not (p[0] > p[2] > p[1]):
                confident_correct = confident_correct + 1
            if (p[0] < 0 and p[1] < 0) or (p[0] > 0 and p[1] > 0):
                confident_winning_team = confident_winning_team + 1

            confident_count = confident_count + 1

        if (p[1] != p[2]):
            total_count = total_count + 1

        avg_diff = avg_diff + math.fabs(p[0]-p[1])
        avg_vegas_diff = avg_vegas_diff + math.fabs(p[1]-p[2])

        # print("{},{},{}".format(p[0],p[1],p[2]))

    try:
        print("Overall spread winning percentage: {}".format(float(spread_correct)/float(total_count)))
        print("Confident spread winning percentage (>= {}): {}".format(confident_scale, float(confident_correct)/float(confident_count)))
        print("Number of spread confident games: {}\tNumber of total games: {}\tProportion: {}".format(confident_count, total_count, float(confident_count)/float(total_count)))
        print("Overall outright winning percentage: {}".format(float(winning_team)/float(total_count)))
        print("Confident outright winning percentage (>= {}): {}".format(confident_scale, float(confident_winning_team)/float(confident_count)))
        print("Average score difference: {}".format(float(avg_diff)/float(predictions.shape[0])))
        print("Average Vegas score difference: {}\n".format(float(avg_vegas_diff)/float(predictions.shape[0])))
    except:
        pass

#for p in predictions:
#    print("{},{},{}".format(p[0],p[1],p[2]))
