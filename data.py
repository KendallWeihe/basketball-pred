import os
import numpy as np
import pdb
import math

def compute_acc(samples, ground_truth):
    difference = 0
    for s, d in zip(samples, ground_truth):
        difference = difference + math.fabs(s - d)

    print("Custom accuracy: {}\n".format(float(difference) / float(len(samples))))

class Data:
    def __init__(self, config):
        self.teams = self.read_teams(config)
        self.read_data(config)
        np.random.shuffle(self.raw_data)
        self.num_training_examples = float(self.raw_data.shape[0]) * config["training_percentage"]
        self.generate_training_data(config)
        self.generate_testing_data(config)
        self.normalize_data()

    def read_teams(self, config):
        teamsFile = open(config["teams_file"], "r")
        return teamsFile.read().splitlines()

    def read_data(self, config):
        seasons = os.listdir(config["seasons_path"])
        raw_data = []
        for s in seasons:
            files = os.listdir(config["seasons_path"]+s)
            for f in files:
                team1 = np.genfromtxt(config["seasons_path"]+s+"/"+f, delimiter=",")

                if team1.shape[0] < config["game_number"]:
                    continue

                try:
                    team1 = team1[::-1,:]

                    team2_index = team1[config["game_number"],43]
                    team2_file = self.teams[int(team2_index)]

                    team2 = np.genfromtxt(config["seasons_path"]+s+"/"+team2_file+".csv", delimiter=",")
                    team2 = team2[::-1,:]

                    team1_index = self.teams.index(f[:f.index(".")])
                    for i in range(team2.shape[0]):
                        if team2[i,43] == team1_index:
                            team2_game_number = i
                            break

                    team1 = team1[0:config["game_number"],]
                    if team2_game_number > config["game_number"]:
                        team2 = team2[team2_game_number-config["game_number"]:team2_game_number,:]
                        aggregate_data = np.concatenate((team1, team2), axis=1)
                    elif team2_game_number < config["game_number"]:
                        temp = np.zeros((config["game_number"], team1.shape[1]))
                        temp[config["game_number"]-team2_game_number:config["game_number"],:] = team2[0:team2_game_number,:]
                        aggregate_data = np.concatenate((team1, temp), axis=1)
                    else:
                        aggregate_data = np.concatenate((team1, team2[0:config["game_number"],:]), axis=1)

                    raw_data.append(aggregate_data)

                except:
                    continue

        self.raw_data = np.array(raw_data)

    def generate_training_data(self, config):
        ground_truth = []
        training_data = []
        for i in range(int(self.num_training_examples)):
            spread = self.raw_data[i,config["game_number"]-1,46]
            ground_truth.append(spread)
            training_data.append(self.raw_data[i,0:config["game_number"]-1,:])

        self.training_data = np.array(training_data)
        self.ground_truth = np.array(ground_truth)

    def generate_testing_data(self, config):
        ground_truth = []
        testing_data = []
        for i in range(int(self.num_training_examples), self.raw_data.shape[0]):
            spread = self.raw_data[i,config["game_number"]-1,46]
            ground_truth.append(spread)
            testing_data.append(self.raw_data[i,0:config["game_number"]-1,:])

        self.testing_data = np.array(testing_data)
        self.testing_ground_truth = np.array(ground_truth)

    def normalize_data(self):
        for i in range(self.raw_data.shape[2]):
            self.training_data[:,:,i] = (self.training_data[:,:,i] - np.min(self.raw_data[:,:,i])) / (np.amax(self.raw_data[:,:,i]) - np.min(self.raw_data[:,:,i]))
            self.testing_data[:,:,i] = (self.testing_data[:,:,i] - np.min(self.raw_data[:,:,i])) / (np.amax(self.raw_data[:,:,i]) - np.min(self.raw_data[:,:,i]))

    def get_training_data(self):
        return self.training_data, self.ground_truth

    def get_testing_data(self):
        return self.testing_data, self.testing_ground_truth
