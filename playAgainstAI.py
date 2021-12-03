import agents
import ninemensmorris
from agents import AlphaBetaAgent, RandomAgent, HumanAgent
from ninemensmorris import NineMensMorris
from tqdm import trange
import numpy as np

weight = [
[8.18627698, -4.99200251,  4.64841755, -2.15612517],
[-0.62366081, 2.31575263, 6.38517914,  2.56146793, -5.33196369, -0.11217285, -4.02026406, -9.7158145],
[-5.21222128, -0.3849427, -1.20550137, -2.31792131]]

episodes = 1
wins = 0

for i in trange(episodes):

    game = NineMensMorris()
    smartAgent = np.random.choice([-1, 1])
    if smartAgent == 1:
        agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3, weights=weight)
        agent2 = HumanAgent()
    else:
        agent1 = HumanAgent()
        agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3, weights=weight)

    done = False
    a1_turn = True
    while not (game.isWin(1) or game.isWin(2)):
        game, reward = agent1.find_opt_move(game, 1) if a1_turn else agent2.find_opt_move(game, 2)
        if ((smartAgent == 1 and not a1_turn) or (smartAgent == -1 and a1_turn)):
            undoInput = input("Undo turn? y/n")
            if (len(undoInput) >= 1 and undoInput[0] == 'y'):
                game = game.prev_nmm.prev_nmm
                a1_turn = not a1_turn
                continue
        a1_turn = not a1_turn
        wins += 1 if smartAgent*game.eval(1, 1) == 1_000_000_000 else 0
print("Win Rate:", wins/episodes)

