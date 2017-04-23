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
            self.generate_training_data(config)
            self.generate_testing_data(config)
            self.normalize_data()

    def read_teams(self, config):
        teamsFile = open(config["teams_file"], "r")
        return teamsFile.read().splitlines()

    def read_data(self, config):
        # seasons = os.listdir(config["seasons_path"])
        # raw_data = []
        # count = 0
        # for s in seasons:
        #     files = os.listdir(config["seasons_path"]+s)
        #     for f in files:
        #         # team1 = np.genfromtxt(config["seasons_path"]+s+"/"+f, delimiter=",")
        #         try:
        #             team1 = np.genfromtxt(config["seasons_path"]+s+"/"+f, delimiter=",")[:,[0,43,3,15,16,19,21,24,36,37,40,42,46]]
        #             team1 = team1[::-1,:]
        #             team1_data = team1[:,2:]
        #
        #             for i in range(4,team1.shape[0]):
        #                 try:
        #                     team2_index = team1[i,1]
        #                     team2_name = self.teams[int(team2_index)]
        #                     team2 = np.genfromtxt(config["seasons_path"]+s+"/"+team2_name+".csv", delimiter=",")[:,[0,3,15,16,19,21,24,36,37,40,42,46]]
        #                     team2_game_index = np.where(team2[:,0] == team1[i,0])[0][0]
        #                     team2 = team2[::-1,1:]
        #                     aggregate_data = np.concatenate((team1_data[i-1,:], team2[team2_game_index-1,:]), axis=0)
        #                     aggregate_data = np.append(aggregate_data, team1_data[i,10])
        #                     raw_data.append(aggregate_data)
        #                 except:
        #                     # pdb.set_trace()
        #                     pass
        #
        #         except:
        #             continue
        #
        # pdb.set_trace()
        # self.raw_data = np.array(raw_data)
        self.raw_data = np.genfromtxt(config["data_path"], delimiter=",")

    def generate_training_data(self, config):
        num_training_examples = int(config["training_percentage"] * self.raw_data.shape[0])
        self.training_data = self.raw_data[0:num_training_examples,0:22]
        self.ground_truth = self.raw_data[0:num_training_examples,22]

    def generate_testing_data(self, config):
        num_testing_examples = int(config["training_percentage"] * self.raw_data.shape[0])
        self.testing_data = self.raw_data[num_testing_examples:self.raw_data.shape[0],0:22]
        self.testing_ground_truth = self.raw_data[num_testing_examples:self.raw_data.shape[0],22]

    def normalize_data(self):
        for i in range(self.training_data.shape[1]):
            self.training_data[:,i] = (self.training_data[:,i] - np.min(self.raw_data[:,i])) / (np.amax(self.raw_data[:,i]) - np.min(self.raw_data[:,i]))
            self.testing_data[:,i] = (self.testing_data[:,i] - np.min(self.raw_data[:,i])) / (np.amax(self.raw_data[:,i]) - np.min(self.raw_data[:,i]))

    def get_training_data(self):
        return self.training_data, self.ground_truth

    def get_testing_data(self):
        return self.testing_data, self.testing_ground_truth

    def get_raw_data(self):
        return self.raw_data
