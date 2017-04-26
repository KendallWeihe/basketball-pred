# TODO:
    # allow user to enter todays games as teams indices

import pdb
import numpy as np

teamsFile = open("/home/kendall/Development/nba-basketball-db/teams.txt", "r")
teams = teamsFile.read().splitlines()

for i in range(0, len(teams), 3):
    try:
        print("{}. {}\t\t{}. {}\t\t{}. {}".format(i, teams[i], i+1, teams[i+1], i+2, teams[i+2]))
    except:
        print("{}. {}".format(i, teams[i]))        

print("Enter -1 to quit")
team1_index = 1
data = []
while 1:
    team1_index = input("Enter team 1: ")
    if team1_index < 0:
        break
    team2_index = input("Enter team 2: ")

    team1_name = teams[team1_index]
    team2_name = teams[team2_index]

    team1 = np.genfromtxt("/home/kendall/Development/nba-basketball-db/accumulated/2017/"+team1_name+".csv", delimiter=",")[:,[3,12,13,16, 21,30,31,34]]
    team2 = np.genfromtxt("/home/kendall/Development/nba-basketball-db/accumulated/2017/"+team2_name+".csv", delimiter=",")[:,[3,12,13,16, 21,30,31,34]]

    aggregate_data = np.concatenate((team1[0,:], team2[0,:]), axis=0)

    pdb.set_trace()
    data.append(aggregate_data)

pdb.set_trace()
np.savetxt("/home/kendall/Development/nba-basketball-db/tmp/today.csv", data, delimiter=",")
