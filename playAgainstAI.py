import agents
import ninemensmorris
from agents import AlphaBetaAgent, RandomAgent, HumanAgent
from ninemensmorris import NineMensMorris
from tqdm import trange
import numpy as np

episodes = 1
wins = 0

for i in trange(episodes):

    game = NineMensMorris()
    smartAgent = np.random.choice([-1, 1])
    if smartAgent == 1:
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3)
        agent2 = HumanAgent()
    else:
        agent1 = HumanAgent()
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3)

    done = False
    a1_turn = True
    while not (game.isWin(1) or game.isWin(2)):
        game, reward = agent1.find_opt_move(game, 1) if a1_turn else agent2.find_opt_move(game, 2)
        a1_turn = not a1_turn
        wins += 1 if smartAgent*game.eval(1, 1) == 1_000_000_000 else 0
print("Win Rate:", wins/episodes)

