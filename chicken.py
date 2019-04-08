import random
import math
import numpy as np
from scipy import stats

# state = {
#     "team-code": "eef8976e",
#     "game": "chicken",
#     "opponent-name": "mighty_ducks",
#     "reaction-time": 5,
#
#     "previous-move": -1,    # -1 if it's the first round, and otherwise will be
#     # your opponent's selection for the previous round
#
#     "outcome": 0            # 0 if there's no previous round, and otherwise represents the utility your bot
#     # received last round (1, -1, 0, or -10)
#
# }

state = {
   "game": "connect_more",
   "opponent-name": "mighty_ducks",
   "columns": 6,
   "connect_n": 5,
   "your-token": "R",
   "board": [
    [],
    [],
    [],
    ['Y'],
    [],
    [],
] }

# state2 = {
#    "game": "connect_more",
#    "opponent-name": "mighty_ducks",
#    "columns": 6,
#    "connect_n": 5,
#    "your-token": "R",
#    "board": [
#     [],
#     [],
#     ['Y'],
#     ['R'],
#     [],
#     [],
# ] }


# global variables

reaction_times = []
previous_moves = []
outcomes = []
# means = []
# stds = []
board_state = []
scores = []
in_a_row = 0


def score(potential_spot, token):
    v=vertical_score(potential_spot, token)
    h=horizontal_score(potential_spot, token)
    d1=diagonal_upRight(potential_spot, token)
    d2=diagonal_downRight(potential_spot, token)
    return v,h,d1,d2

def vertical_score(position, token):  
    global board_state
    global in_a_row
    enemy_streak = True
    e_count = 0
    our_streak = True
    o_count = 0
    last_index = len(board_state[position])
    i = 1
    while enemy_streak or our_streak:
        if last_index-i < 0:
            break
        if enemy_streak and board_state[position][last_index-i] == token:
            our_streak = False
            e_count += 2 #figure out scoring
        if our_streak and board_state[position][last_index-i] != token:
            enemy_streak = False
            o_count += 1
        i += 1
    if o_count == in_a_row-1:
        return (position, 99999)
    return (position, o_count) if o_count > e_count else (position, e_count)

def horizontal_score(position, token):
    global board_state
    global in_a_row
    left_enemy_streak = True
    e_count_left = 0
    left_our_streak = True
    o_count_left = 0
    last_index = len(board_state[position])
    i = 1
    while left_enemy_streak or left_our_streak:
        if position - i < 0:
            break
        if last_index >= len(board_state[position-i]):
            break
        if left_enemy_streak and board_state[position-i][last_index] == token:
            left_our_streak = False
            e_count_left += 2 #scoring
        if left_our_streak and board_state[position-i][last_index] != token:
            left_our_streak = False
            o_count_left += 1
        i += 1
    if o_count_left == in_a_row-1:
        return (position, 99999)
    right_enemy_streak = True
    e_count_right = 0
    right_our_streak = True
    o_count_right = 0
    j = 1
    while right_enemy_streak or right_our_streak:
        if position + j >= len(board_state):
            break
        if last_index >= len(board_state[position + j]):
            break
        if right_enemy_streak and board_state[position + j][last_index] == token:
            right_our_streak = False
            e_count_right += 2
        if right_our_streak and board_state[position + j][last_index] != token:
            right_enemy_streak = False
            o_count_right += 1
        j += 1
    if o_count_right == in_a_row-1:
        return (position, 99999)
    if o_count_right + o_count_left >= in_a_row-1:
        return (position, 99999)
    return (position, e_count_right + e_count_left + o_count_right + o_count_left)

def diagonal_upRight(position, token):
    global board_state
    global in_a_row
    left_enemy_streak = True
    e_count_left = 0
    left_our_streak = True
    o_count_left = 0
    last_index = len(board_state[position])
    i = 1
    j = 1
    while left_enemy_streak or left_our_streak:
        if position - i < 0:
            break
        if last_index - j < 0:
            break
        if last_index - j >= len(board_state[position-i]):
            break
        if left_enemy_streak and board_state[position-i][last_index-j] == token:
            left_our_streak = False
            e_count_left += 2
        if left_our_streak and board_state[position-i][last_index-j] != token:
            left_enemy_streak = False
            o_count_left += 1
        j += 1
        i += 1
    if o_count_left == in_a_row-1:
        return (position, 99999)
    right_enemy_streak = True
    e_count_right = 0
    right_our_streak = True
    o_count_right = 0
    i = 1
    j = 1
    while right_enemy_streak or right_our_streak:
        if position + i >= len(board_state):
            break
        if last_index + j >= len(board_state[position+i]):
            break
        if right_enemy_streak and board_state[position+i][last_index+j] == token:
            right_our_streak = False
            e_count_right += 2
        if right_our_streak and board_state[position+i][last_index+j] != token:
            right_enemy_streak = False
            o_count_right += 1
        j += 1
        i += 1
    if o_count_right == in_a_row-1:
        return (position, 99999)
    if o_count_right + o_count_left >= in_a_row-1:
        return (position, 99999)
    return (position, e_count_left + e_count_right + o_count_right + o_count_left)

def diagonal_downRight(position, token):
    global board_state
    global in_a_row
    left_enemy_streak = True
    e_count_left = 0
    left_our_streak = True
    o_count_left = 0
    last_index = len(board_state[position])
    i = 1
    j = 1
    while left_enemy_streak or left_our_streak:
        if position - i < 0:
            break
        if last_index + j >= len(board_state[position-i]):
            break
        if left_enemy_streak and board_state[position-i][last_index + j] == token:
            left_our_streak = False
            e_count_left += 2
        if left_our_streak and board_state[position-i][last_index + j] != token:
            left_enemy_streak = False
            o_count_left += 1
        i+=1
        j+=1
    if o_count_left == in_a_row-1:
        return (position, 99999)
    right_enemy_streak = True
    e_count_right = 0
    right_our_streak = True
    o_count_right = 0
    i = 1
    j = 1
    while right_enemy_streak or right_our_streak:
        if position + i >= len(board_state):
            break
        if last_index - j < 0:
            break
        if last_index - j >= len(board_state[position + i]):
            break
        if right_enemy_streak and board_state[position + i][last_index - j] == token:
            right_our_streak = False
            e_count_left += 2
        if right_our_streak and board_state[position + i][last_index -j] != token:
            right_enemy_streak = False
            o_count_right += 1
        i+=1
        j+=1
    if o_count_right == in_a_row-1:
        return (position, 99999)
    if o_count_right + o_count_left >= in_a_row-1:
        return (position, 99999)
    return (position, e_count_left + e_count_right + o_count_right + o_count_left)



def get_move(state):
    if(state["game"] == "chicken"):
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
    else:
        global board_state
        global scores
        global in_a_row
        if len(board_state)==0: # for beginning of the game scenarios
            move_location = -1
            token = ''
            in_a_row = state["connect_n"]
            empty = True
            for i in range(state["columns"]):
                scores.append(0)
            #check to see if you have the first move or not
            for i in range(state["columns"]):
                board_state.append(state["board"][i])
                if len(state["board"][i]) != 0:
                    #board_state[column].append(column[0])
                    empty = False
                    move_location = i
                    token = board_state[i][-1]
                    #calculate_scores(i)
            # you have the first move
            if empty:
                starting_point = math.ceil(state["columns"]/2)
                board_state[starting_point].append(state["your-token"])

                print(board_state)
                return starting_point
            else:
                above = [-1, 0]
                left = [-1, -1]
                right = [-1, -1]
                above_scores = score(move_location, token)
                print(score(move_location, token)) # above
                above[0] = above_scores[0][0]
                for results in above_scores:
                    above[1] += results[1]
                # print(above)
                if move_location - 1 >= 0:
                    left_scores = score(move_location - 1, token)
                    print(score(move_location-1, token)) #left
                    left[0] = left_scores[0][0]
                    left[1] = 0
                    for results in left_scores:
                        left[1] += results[1]
                    # print(left)
                if move_location + 1 < len(board_state):
                    right_scores = score(move_location + 1, token)
                    print(score(move_location+1, token)) #right
                    right[0] = right_scores[0][0]
                    right[1] = 0
                    for results in right_scores:
                        right[1] += results[1]
                    # print(right)
                all_three = [above, left, right]
                all_three.sort(key=lambda x: x[1], reverse=1)
                # print(all_three)
                max = all_three[0][1]
                occurences = 0
                for arr in all_three:
                    if arr[1] == max:
                        occurences += 1
                    else:
                        break
                if occurences > 1:
                    result = all_three[random.randint(0, occurences - 1)][0]
                    # print(result)
                    board_state[result].append(state['your-token'])
                    print(board_state)
                    return result
                else:
                    board_state[all_three[0][0]].append(state['your-token'])
                    return all_three[0][0]



        else:
            token = "R"
            for i in range(0, state['columns']):
                move_location = -1
                if len(state["board"][i]) != len(board_state[i]):
                    token = state["board"][i][-1] # enemy token
                    board_state[i].append(token)
                    move_location = i
                    break

            print(board_state)

            above = [-1,0]
            left = [-1,-1]
            right = [-1,-1]
            above_scores = score(move_location, token)
            #print(score(move_location, token)) # above
            above[0] = above_scores[0][0]
            for results in above_scores:
                above[1] += results[1]
            #print(above)
            if move_location - 1 >= 0:
                left_scores = score(move_location-1, token)
                #print(score(move_location-1, token)) #left
                left[0] = left_scores[0][0]
                left[1] = 0
                for results in left_scores:
                    left[1] += results[1]
                #print(left)
            if move_location + 1 < len(board_state):
                right_scores = score(move_location+1, token)
                #print(score(move_location+1, token)) #right
                right[0] = right_scores[0][0]
                right[1] = 0
                for results in right_scores:
                    right[1] += results[1]
                #print(right)
            all_three = [above, left, right]
            all_three.sort(key=lambda x:x[1], reverse=1)
            #print(all_three)
            max = all_three[0][1]
            occurences = 0
            for arr in all_three:
                if arr[1] == max:
                    occurences += 1
                else:
                    break
            if occurences > 1:
                result = all_three[random.randint(0, occurences-1)][0]
                #print(result)
                board_state[result].append(state['your-token'])
                print(board_state)
                return result
            else:
                board_state[all_three[0][0]].append(state['your-token'])
                return all_three[0][0]



get_move(state)
#get_move(state2)
    
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
