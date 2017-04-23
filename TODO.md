# Developing experiments:

- for seasons 2010 through 2017:
  - fixed number of games for game numbers between 4 and 26
  - fixed number of games for game numbers between 4 and 26 **with accumulated data**

**pseudocode:**
```
for game number in game numbers:
  for season in seasons:
    move season into tmp/
    for training session in range(5):
      train and save model
    predict
      save to it's own CSV file -- one CSV file for each season & game number
```

# TODO:

- collect spreads over last 7 years
- all games LSTM with zero padding
- all games MLP -- accumulated stats
