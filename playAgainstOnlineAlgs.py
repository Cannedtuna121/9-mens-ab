from agents import AlphaBetaAgent, RandomAgent
from ninemensmorris import NineMensMorris
from tqdm import trange
import numpy as np

episodes = 6 # Don't change
wins = 0
max_iter = 100
our_agent_weights = [[8.47531752,  1.14965636,  8.10564905, -3.49353069],
                    [-0.34866957, -6.44818734, 8.8221015,   7.67009098,  0.05872871,  0.42747391,  4.62017604, -7.73292282],
                    [5.91117537,  5.97929156,  2.45572599, -3.95235823]]
depth = 2

for i in trange(episodes):

    game = NineMensMorris()
    
    if (i == 0): 
        smartAgent = 1
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy=None, weights=our_agent_weights)
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy='online_alg1', weights=None)
    elif (i == 1):
        smartAgent = -1
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy='online_alg1', weights=None)
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy=None, weights=our_agent_weights)
    elif (i == 2):
        smartAgent = 1
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy=None, weights=our_agent_weights)
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy='online_alg2', weights=None)
    elif (i == 3):
        smartAgent = -1
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy='online_alg2', weights=None)
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy=None, weights=our_agent_weights)
    elif (i == 4):
        smartAgent = 1
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy=None, weights=our_agent_weights)
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy='online_alg3', weights=None)
    elif (i == 5):
        smartAgent = -1
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy='online_alg3', weights=None)
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=depth,
                                max_player=1, strategy=None, weights=our_agent_weights)

    done = False
    a1_turn = True
    #iteration = 0
    for _ in trange(max_iter):
        game, reward = agent1.find_opt_move(game, 1) if a1_turn else agent2.find_opt_move(game, 2)
        a1_turn = not a1_turn
        if (game.isWin(1) or game.isWin(2)): break
        # iteration += 1

    wins += 1 if smartAgent*game.eval(1, 1) == 1_000_000_000 else 0

print("\nWin Rate:", wins/episodes)