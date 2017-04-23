import numpy as np
import os
import pdb

teamsFile = open("/home/kendall/Development/basketball-db/teams.txt", "r")
teams = teamsFile.read().splitlines()

games = np.genfromtxt("/home/kendall/Development/basketball-db/spreads/2017-feb-0-18.csv", delimiter=",")

data_path = "/home/kendall/Development/2017/"

count = 0
avg_game_number = []
game_number_count = 0
for game in games:
    team1_index = game[1]
    team2_index = game[2]
    team1_name = teams[int(team1_index)].replace("(", "\(").replace(")", "\)")
    team2_name = teams[int(team2_index)].replace("(", "\(").replace(")", "\)")
    vegas_spread = game[3] - game[4]

    try:
        team1 = np.genfromtxt(data_path + team1_name + ".csv", delimiter=",")
        team1 = team1[::-1,:]
        game_number = np.where(team1[:,0] == game[0])[0][0]

        if game_number == 23:
            game_number_count = game_number_count + 1
            os.system("python predict.py {} {} {} {} {}".format(game_number, team1_name, team2_name, game[0], vegas_spread))

    except:
        continue

    count = count + 1
    avg_game_number.append(game_number)

print("Percent functional: {}".format(float(count)/float(len(games))))
print("Average game number: {}".format(float(np.mean(avg_game_number))))
print("Number of games equal to 23: {}".format(game_number_count))
