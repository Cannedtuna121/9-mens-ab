from agents import AlphaBetaAgent, RandomAgent
from ninemensmorris import NineMensMorris
from tqdm import trange
import numpy as np

episodes = 6 # Don't change
wins = 0
max_iter = 100
# our_agent_weights = [[8.47531752,  1.14965636,  8.10564905, -3.49353069],
#                     [-0.34866957, -6.44818734, 8.8221015,   7.67009098,  0.05872871,  0.42747391,  4.62017604, -7.73292282],
#                     [5.91117537,  5.97929156,  2.45572599, -3.95235823]]
# our_agent_weights = [[ 0.25881889,  0.73915422,  5.29516936,  9.57751935 ],
#  [-2.35316248, -1.36067873, 3.14801864, 11.51043482, -3.76819322,  6.7475799,  -2.82267305 ,-5.33653518],
#   [5.68846286, -7.48438148,  6.74884434,  8.8137806 ]]
our_agent_weights =  [[ 9.04963465,  2.41271133,  7.79383726, -7.73246753 ],
 [2.71139758, -3.4810557, 1.56830888,  9.94005156, -0.19213668,  9.67457274, -0.05219354, -6.87482395],
 [1.56343005,  9.81174816,  0.90162486,  3.11871356]] #Best agent
depth = 3

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
