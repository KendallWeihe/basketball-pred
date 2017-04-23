# for game number in game numbers:
#   for season in seasons:
#     move season into tmp/
#     for training session in range(5):
#       train and save model
#     predict
#       save to it's own CSV file -- one CSV file for each season & game number

import os
import pdb

game_numbers = []
for i in range(5,27):
    game_numbers.append(i)

seasons = []
for i in range(2012,2018):
    seasons.append(i)

db_path = "/home/kendall/Development/basketball-db/"
for game_number in game_numbers:
    for season in seasons:
        os.system("mv {}accumulated/{}/ {}tmp/".format(db_path, season, db_path))
        model_paths = []
        for i in range(5):
            model_path = "./models/{}-{}-{}".format(game_number, season, str(i))
            os.mkdir(model_path)
            model_paths.append(model_path)
            os.system("python train.py {} {} {}".format(game_number, model_path, season))
        os.system("python predict_CGI.py {} {} {} {} {} {} {}".format(season, game_number, model_paths[0], model_paths[1],\
                model_paths[2], model_paths[3], model_paths[4]))

        os.system("mv {}tmp/{} {}accumulated/".format(db_path, season, db_path))
