# TODO TEST:
#
#   test.py
#     games = np.genfromtxt()
#     for game in games:
#       team1_index = game[]
#       team2_index = game[]
#       team1_name = teams[]
#       team2_name = teams[]
#       vegas_spread = game[]
#
#       os.system("mv file into tmp/")
#
#       find_num_games(team2_index):
#         open team1
#         game_number = team1.where(team2_index == team2_index)
#
#       os.system("python predict.py " + team1_name + team2_name + team1_index + team2_index + + game_number +    vegas_spread)
#
#       os.system("mv file back into data dir/")

import numpy as np
import os
import pdb

teamsFile = open("/Users/kendallweihe/Google Drive/Development/basketball-db/teams.txt", "r")
teams = teamsFile.read().splitlines()

games = np.genfromtxt("/Users/kendallweihe/Google Drive/Development/basketball-db/spreads/2017-feb-0-18.csv", delimiter=",")

data_path = "/Users/kendallweihe/Google\ Drive/Development/basketball-db/seasons/2017/"
tmp_path = "/Users/kendallweihe/Google\ Drive/Development/basketball-pred/tmp/"
tmp_path_np = "/Users/kendallweihe/Google Drive/Development/basketball-pred/tmp/"

count = 0
avg_game_number = []
for game in games:
    team1_index = game[1]
    team2_index = game[2]
    team1_name_np = teams[int(team1_index)]
    team2_name_np = teams[int(team2_index)]
    team1_name = team1_name_np.replace("(", "\(").replace(")", "\)")
    team2_name = team2_name_np.replace("(", "\(").replace(")", "\)")
    vegas_spread = game[3] - game[4]

    try:
        # os.system("cp " + data_path + team1_name + ".csv " + tmp_path)
        # os.system("cp " + data_path + team2_name + ".csv " + tmp_path)
        team1 = np.genfromtxt(tmp_path_np + team1_name_np + ".csv", delimiter=",")
        team1 = team1[::-1,:]
        game_number = np.where(team1[:,0] == game[0])[0][0]

        # TODO: call the predict.py program
    except:
        continue

    # try:
    #     os.system("rm " + tmp_path + team1_name + ".csv ")
    #     os.system("rm " + tmp_path + team2_name + ".csv ")
    # except:
    #     continue

    count = count + 1
    avg_game_number.append(game_number)

print("Percent functional: {}".format(float(count)/float(len(games))))
print("Average game number: {}".format(float(np.mean(avg_game_number))))
