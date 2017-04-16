import numpy as np
import pdb
import math

predictions = np.genfromtxt("./compare-vegas.csv", delimiter=",")

total_count = 0
spread_correct = 0
confident_scale = 6
confident_correct = 0
confident_count = 0
winning_team = 0
confident_winning_team = 0
for p in predictions:
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

print("Overall spread winning percentage: {}".format(float(spread_correct)/float(total_count)))
print("Confident spread winning percentage (>= {}): {}".format(confident_scale, float(confident_correct)/float(confident_count)))
print("Number of spread confident games: {}\tNumber of total games: {}\tProportion: {}".format(confident_count, total_count, float(confident_count)/float(total_count)))
print("Overall outright winning percentage: {}".format(float(winning_team)/float(total_count)))
print("Confident outright winning percentage (>= {}): {}".format(confident_scale, float(confident_winning_team)/float(confident_count)))
