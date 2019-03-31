import random

state = {
   "team-code": "eef8976e",
   "game": "chicken",
   "opponent-name": "mighty_ducks",
   "reaction-time": 5,

   "previous-move": -1,    # -1 if it's the first round, and otherwise will be
                           # your opponent's selection for the previous round

   "outcome": 0            # 0 if there's no previous round, and otherwise represents the utility your bot
                           # received last round (1, -1, 0, or -10)

}

data = {}



def get_move(state):
   if state["opponent-name"] not in data.keys():
      # initialize new entry in data dictionary
      data[state["opponent-name"]] = {}
      data[state["opponent-name"]]["reaction-times"] = []
      data[state["opponent-name"]]["previous-moves"] = []
      if random.randint(0, 10) == 0:  # 1/10 chance to not swerve
         return 1
      else:
         return 0
   else:
      # update dictionary entry
      data[state["opponent-name"]]["reaction-times"].append(state["reaction-time"])
      data[state["opponent-name"]]["previous-moves"].append(state["previous-moves"])

      sum = 0
      count = 0
      for time in data[state["opponent-name"]]["reaction-times"]:
         sum += time
         count += 1
      average_time = sum / count










   # Any processing you do goes here.



   # return 0.25 # If you were to always swerve at 1/4 seconds left


