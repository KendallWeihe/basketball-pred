import os
import numpy as np
import pdb
import math

def compute_acc(samples, ground_truth, dataset_type):
    difference = 0
    for s, d in zip(samples, ground_truth):
        difference = difference + math.fabs(s - d)
        # print("My prediction: {:.3f}\tActual spread: {}".format(s, d))

    print("Custom {} accuracy: {}".format(dataset_type, float(difference) / float(len(samples))))

class Data:
    def __init__(self, config):
        self.teams = self.read_teams(config)
        self.read_data(config)
        if config["training"]:
            np.random.shuffle(self.raw_data)
            self.num_training_examples = float(self.raw_data.shape[0]) * config["training_percentage"]
            self.generate_training_data(config)
            self.generate_testing_data(config)
            self.generate_verification_data(config)
            self.normalize_data()

    def read_teams(self, config):
        teamsFile = open(config["teams_file"], "r")
        return teamsFile.read().splitlines()

    def read_data(self, config):
        seasons = os.listdir(config["seasons_path"])
        raw_data = []
        count = 0
        for s in seasons:
            files = os.listdir(config["seasons_path"]+s)
            for f in files:
                # team1 = np.genfromtxt(config["seasons_path"]+s+"/"+f, delimiter=",")
                try:
                    team1 = np.genfromtxt(config["seasons_path"]+s+"/"+f, delimiter=",")[:,[0,43,3,15,16,19,21,24,36,37,40,42,46]]

                    if team1.shape[0] < config["game_number"]:
                        continue

                    team1 = team1[::-1,:]
                    team2_index = team1[config["game_number"],1]
                    team2_file = self.teams[int(team2_index)]

                    # team2 = np.genfromtxt(config["seasons_path"]+s+"/"+team2_file+".csv", delimiter=",")
                    team2 = np.genfromtxt(config["seasons_path"]+s+"/"+team2_file+".csv", delimiter=",")[:,[0,3,15,16,19,21,24,36,37,40,42,46]]

                    team2 = team2[::-1,:]
                    team2_game_number = np.where(team2[:,0] == team1[config["game_number"],0])[0][0]
                    team1 = team1[0:config["game_number"]+1,2:]
                    team2 = team2[:,1:]

                    count = count + 1
                    if team2_game_number > config["game_number"]:
                        team2 = team2[team2_game_number-config["game_number"]:team2_game_number+1,:]
                        aggregate_data = np.concatenate((team1, team2), axis=1)
                    elif team2_game_number < config["game_number"]:
                        temp = np.zeros((team1.shape[0], team1.shape[1]))
                        temp[config["game_number"]-team2_game_number:config["game_number"]+1,:] = team2[0:team2_game_number+1,:]
                        aggregate_data = np.concatenate((team1, temp), axis=1)
                    else:
                        aggregate_data = np.concatenate((team1, team2[0:config["game_number"]+1,:]), axis=1)

                    raw_data.append(aggregate_data)

                except:
                    continue

        self.raw_data = np.array(raw_data)

    def generate_training_data(self, config):
        ground_truth = []
        training_data = []
        for i in range(int(self.num_training_examples)):
            spread = self.raw_data[i,config["game_number"],10]
            ground_truth.append(spread)
            training_data.append(self.raw_data[i,0:config["game_number"]-1,:])

        self.training_data = np.array(training_data)
        self.ground_truth = np.array(ground_truth)

    def generate_testing_data(self, config):
        ground_truth = []
        testing_data = []
        for i in range(int(self.num_training_examples), self.raw_data.shape[0]):
            spread = self.raw_data[i,config["game_number"],10]
            ground_truth.append(spread)
            testing_data.append(self.raw_data[i,0:config["game_number"]-1,:])

        self.testing_data = np.array(testing_data)
        self.testing_ground_truth = np.array(ground_truth)

    def generate_verification_data(self, config):
        teams = os.listdir(config["verification_path"])

        raw_data = []
        for team1_file in teams:
            try:
                team1 = np.genfromtxt(config["verification_path"]+team1_file, delimiter=",")[:,[0,43,3,15,16,19,21,24,36,37,40,42,46]]

                if team1.shape[0] < config["game_number"]:
                    continue

                team1 = team1[::-1,:]
                team2_index = team1[config["game_number"],1]
                team2_file = self.teams[int(team2_index)]

                # team2 = np.genfromtxt(config["seasons_path"]+s+"/"+team2_file+".csv", delimiter=",")
                team2 = np.genfromtxt(config["verification_path"]+team2_file+".csv", delimiter=",")[:,[0,3,15,16,19,21,24,36,37,40,42,46]]
                team2 = team2[::-1,:]
                team2_game_number = np.where(team2[:,0] == team1[config["game_number"],0])[0][0]

                team1 = team1[0:config["game_number"]+1,2:]
                team2 = team2[:,1:]

                if team2_game_number > config["game_number"]:
                    team2 = team2[team2_game_number-config["game_number"]:team2_game_number+1,:]
                    aggregate_data = np.concatenate((team1, team2), axis=1)
                elif team2_game_number < config["game_number"]:
                    temp = np.zeros((team1.shape[0], team1.shape[1]))
                    temp[config["game_number"]-team2_game_number:config["game_number"]+1,:] = team2[0:team2_game_number+1,:]
                    aggregate_data = np.concatenate((team1, temp), axis=1)
                else:
                    aggregate_data = np.concatenate((team1, team2[0:config["game_number"]+1,:]), axis=1)

                raw_data.append(aggregate_data)

            except:
                continue

        self.verification_ground_truth = np.array(raw_data)[:,config["game_number"],10]
        self.verification_data = np.array(raw_data)[:,0:config["game_number"]-1,:]

    def normalize_data(self):
        for i in range(self.raw_data.shape[2]):
            self.training_data[:,:,i] = (self.training_data[:,:,i] - np.min(self.raw_data[:,:,i])) / (np.amax(self.raw_data[:,:,i]) - np.min(self.raw_data[:,:,i]))
            self.testing_data[:,:,i] = (self.testing_data[:,:,i] - np.min(self.raw_data[:,:,i])) / (np.amax(self.raw_data[:,:,i]) - np.min(self.raw_data[:,:,i]))
            self.verification_data[:,:,i] = (self.verification_data[:,:,i] - np.min(self.raw_data[:,:,i])) / (np.amax(self.raw_data[:,:,i]) - np.min(self.raw_data[:,:,i]))

    def get_training_data(self):
        return self.training_data, self.ground_truth

    def get_testing_data(self):
        return self.testing_data, self.testing_ground_truth

    def get_verification_data(self):
        return self.verification_data, self.verification_ground_truth

    def get_raw_data(self):
        return self.raw_data
