from games import TTT as TicTacToe
from ninemensmorris import NineMensMorris

from agents import AlphaBetaAgent, RandomAgent

from tqdm import trange, tqdm
import numpy as np

from multiprocessing import Process, Array

def ttt_terminal(game):
    return game.is_terminal()

def nmm_terminal(game):
    return game.isWin(1) or game.isWin(2)

def run_game(game_class, max_player, win_score, terminal,
             wins, index, strategy, weights, 
             opp_strategy='random', opp_weights=[], 
             max_steps=10):
    game = game_class()
    smartAgent = np.random.choice([-1, 1])
    if smartAgent == 1:
        agent1 = AlphaBetaAgent(upper_lim=win_score, lower_lim=-win_score, max_depth=3,
                                max_player=max_player, strategy=strategy, weights=weights)
        if opp_strategy == 'random':
            agent2 = RandomAgent()
        else:
            agent2 = AlphaBetaAgent(upper_lim=win_score, lower_lim=-win_score, max_depth=3,
                                    max_player=max_player, strategy=opp_strategy, weights=opp_weights)
    else:
        if opp_strategy == 'random':
            agent1 = RandomAgent()
        else:
            agent1 = AlphaBetaAgent(upper_lim=win_score, lower_lim=-win_score, max_depth=3,
                                    max_player=max_player, strategy=opp_strategy, weights=opp_weights)
        agent2 = AlphaBetaAgent(upper_lim=win_score, lower_lim=-win_score, max_depth=3,
                                max_player=max_player, strategy=strategy, weights=weights)

    done = False
    a1_turn = True
    for step in range(max_steps):
        game, reward = agent1.find_opt_move(game, game.p1) if a1_turn else agent2.find_opt_move(game, game.p2)
        a1_turn = not a1_turn
        if terminal(game): break

    wins[index] = 1 if smartAgent*game.eval(game.p1, game.p1) == win_score else 0

def ttt_fitness_function(strategy, weights, opp_strategy='random', opp_weights=[], episodes=10):
    max_steps = 10
    
    wins = Array('i', range(episodes))
    cores = []
    for i in range(episodes):
        p = Process(target=run_game, args=(TicTacToe, 'x', 100, ttt_terminal,
                                           wins, i, strategy, weights, 
                                           opp_strategy, opp_weights, max_steps))
        p.start()
        cores.append(p)
        
    for core in cores:
        core.join()
    return np.sum(wins)/episodes

def nmm_fitness_function(strategy, weights, opp_strategy='random', opp_weights=[], episodes=10):
    weights = [weights[:4], weights[4:12], weights[12:]]
    max_steps = 100
    
    wins = Array('i', range(episodes))
    cores = []
    for i in range(episodes):
        p = Process(target=run_game, args=(NineMensMorris, 1, 1_000_000_000, nmm_terminal,
                                                       wins, i, strategy, weights, 
                                                       opp_strategy, opp_weights, max_steps))
        p.start()
        cores.append(p)
        
    for core in cores:
        core.join()
    return np.sum(wins)/episodes

from geneal.genetic_algorithms import ContinuousGenAlgSolver
from geneal.applications.fitness_functions.continuous import fitness_functions_continuous

def run_genetic_algorithm(fitness_function, num_genes, strategy, opp_strategy, opp_weights, episodes):
    solver = ContinuousGenAlgSolver(
        n_genes=num_genes, 
        fitness_function=lambda weights: fitness_function(
            strategy, weights, opp_strategy, opp_weights, episodes),
        pop_size=10,
        max_gen=100,
        mutation_rate=0.1,
        selection_rate=0.6,
        selection_strategy="roulette_wheel",
        problem_type=float, # Defines the possible values as float numbers
        variables_limits=(-1, 1) # Defines the limits of all variables between -10 and 10. 
                                   # Alternatively one can pass an array of tuples defining the limits
                                   # for each variable: [(-10, 10), (0, 5), (0, 5), (-20, 20)]
    )

    solver.solve() 