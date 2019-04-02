import random
import numpy as np
from scipy import stats

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

# global variables

reaction_times = []
previous_moves = []
outcomes = []
# means = []
# stds = []


def get_move(state):
    global reaction_times
    global previous_moves
    # global means
    # global stds

    # First round
    if state["previous-move"] == -1:
        # # update means and stds
        # mean = np.mean(reaction_times)
        # std = np.std(reaction_times, ddof=1)  # sample standard deviation
        # if not np.isnan(std):
        #     means.append(mean)
        #     stds.append(std)

        # empty lists
        reaction_times = []
        previous_moves = []

        # return random float between 9 and 10 (unpredictable and conservative)
        return random.uniform(9, 10)

    # All other rounds
    else:
        # update dictionary entry
        reaction_times.append(state["reaction-time"])
        previous_moves.append(state["previous-move"])

        mean = np.mean(reaction_times)
        std = np.std(reaction_times, ddof=1)  # sample standard deviation
        n = len(reaction_times)

        t = stats.t.ppf(.95, df=5000)  # .95 significance level

        result = t * std/(n ** .5) + mean

        if np.isnan(result):
            return (mean + 10) / 2  # average of reaction-time and 10

        if state["outcome"] == 1:
            return max(result, state["previous-move"] - std/(n ** .5))

        # Swerve at 'result' seconds left
        return result


# print(get_move(state))
#
# state2 = {
#     "team-code": "eef8976e",
#     "game": "chicken",
#     "opponent-name": "mighty_ducks",
#     "reaction-time": 4,
#
#     "previous-move": 1,    # -1 if it's the first round, and otherwise will be
#     # your opponent's selection for the previous round
#
#     "outcome": 0            # 0 if there's no previous round, and otherwise represents the utility your bot
#     # received last round (1, -1, 0, or -10)
# }
#
# state3 = {
#     "team-code": "eef8976e",
#     "game": "chicken",
#     "opponent-name": "mighty_ducks",
#     "reaction-time": 3,
#
#     "previous-move": 1,    # -1 if it's the first round, and otherwise will be
#     # your opponent's selection for the previous round
#
#     "outcome": 0            # 0 if there's no previous round, and otherwise represents the utility your bot
#     # received last round (1, -1, 0, or -10)
# }
#
# print(get_move(state2))
# print(get_move(state3))
