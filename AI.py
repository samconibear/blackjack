import tensorflow as tf
import sys, os
import random


import blackjack as bj

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

player_options = ['s', 'h', 'd', 'sp']

# Create Training Data
training_data = []

# per game
game_memory = []

# per turn
while not game_finished:
    prev_observation = (card1, card2, dealers_card)
    action = random.choice(player_options)

    # observation = output from action in game
    game_memory.append(prev_observation, action)
    prev_observation = observation

# after the game is over
if game_score >= 0
    accepted_scores.append(game_score)
    training_data.append(game_memory)




observations.append(observation)
actions.append(action)
training_data.append((observation, action, score))




'''blockPrint()
game = bj.game()
enablePrint()'''
