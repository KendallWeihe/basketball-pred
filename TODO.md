BACKUP DATA!!!

scrape data from teamrankings that includes vegas spread
  TODO: will need to generate lookup of sorts for team names across datasets

  file_columns: date | team1_index, team2_index | team1_vegas_score, team2_vegas_score, team1_score, team2_score, spread
    NOTE: each game will have two rows, one for team1 and one for team2
      TODO: when predicting, average the spread difference
        NOTE: before doing this, just do straight up predictions

TODO:
  train and save models for each game number 10-25

TODO TEST:

  test.py
    games = np.genfromtxt()
    for game in games:
      team1_index = game[]
      team2_index = game[]
      team1_name = teams[]
      team2_name = teams[]
      vegas_spread = game[]

      os.system("mv file into tmp/")

      find_num_games(team2_index):
        open team1
        game_number = team1.where(team2_index == team2_index)

      os.system("python predict.py " + team1_name + team2_name + team1_index + team2_index + + game_number +    vegas_spread)

      os.system("mv file back into data dir/")

  predict.py
    place argv into config
    read in prediction file from argv
    open saved model based on game_number
    make prediction
    open test.csv
    if win, then append
      [1, team1_index, game_number]
    else append
      [0, team1_index, game_number]
    save back to file



TODO TEST v2:
  save models across thousands of iterations
  make multiple predictions from different models
  average prediction spread value

TODO: identify home or away game in scrape.py
