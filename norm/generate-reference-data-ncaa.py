import numpy as np
import os
import pdb

teamsFile = open("/home/kendall/Development/basketball-db/teams.txt", "r")
teams = teamsFile.read().splitlines()

seasons_path = "/home/kendall/Development/basketball-db/accumulated/"

seasons = os.listdir(seasons_path)
raw_data = []
for s in seasons:
    files = os.listdir(seasons_path+s)
    for f in files:
        try:

            # if s == "2017" and f == "Gonzaga.csv":
            #     pdb.set_trace()
            #     print

            # NOTE: columns 3, 12, 15, 19, 24, 33, 36, 40
            team1_index = teams.index(f[:f.index(".csv")])
            team1 = np.genfromtxt(seasons_path+s+"/"+f, delimiter=",")[:,[0,43, 3,12,15,19, 24,33,36,40, 46]]
            team1 = team1[::-1,:]
            spread = team1[:,10]
            team1_data = team1[:,2:10]

            for i in range(4,team1.shape[0]):
                try:
                    team2_index = team1[i,1]
                    team2_name = teams[int(team2_index)]
                    team2 = np.genfromtxt(seasons_path+s+"/"+team2_name+".csv", delimiter=",")[:,[0, 3,12,15,19, 24,33,36,40]]
                    team2 = team2[::-1,:]
                    team2_game_index = np.where(team2[:,0] == team1[i,0])[0][0]
                    team2 = team2[:,1:]
                    aggregate_data = np.concatenate((team1_data[i-1,:], team2[team2_game_index-1,:]), axis=0)
                    aggregate_data = np.append(aggregate_data, spread[i])
                    aggregate_data = np.append(aggregate_data, team1[i,0])
                    aggregate_data = np.append(aggregate_data, team1_index)
                    raw_data.append(aggregate_data)
                except:
                    pass



        except:
            continue

pdb.set_trace()
np.savetxt("/home/kendall/Development/basketball-db/accumulated-selected.csv", raw_data, delimiter=",")
