from agents import AlphaBetaAgent, RandomAgent
from ninemensmorris import NineMensMorris
from tqdm import trange
import numpy as np
from geneal.genetic_algorithms import ContinuousGenAlgSolver
from geneal.applications.fitness_functions.continuous import fitness_functions_continuous

def nine_mens_morris_fitness_function(strategy, weights, opp_strategy='random', opp_weights=[], episodes=6):
    weights = [weights[:4], weights[4:12], weights[12:]]
    wins = 0
    max_steps = 100

    for i in trange(episodes):

        game = NineMensMorris()
        # i = 0 or 1 -> play the evolving agent against the 1st set of fixed weights (2 games, both take their turn going 1st)
        if (i == 0):
            smartAgent = 1
            agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights) # evolving agent
            agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=opp_strategy, weights=opp_weights[0]) # fixed agent
        elif (i == 1):
            smartAgent = -1
            agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=opp_strategy, weights=opp_weights[0]) # fixed agent
            agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights) # evolving agent
        # i = 2 or 3 -> play the evolving agent against the 2nd set of fixed weights (2 games, both take their turn going 1st)
        elif (i == 2):
            smartAgent = 1
            agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights) # evolving agent
            agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=opp_strategy, weights=opp_weights[1]) # fixed agent
        elif (i == 3):
            smartAgent = -1
            agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=opp_strategy, weights=opp_weights[1]) # fixed agent
            agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights) # evolving agent
        # i = 4 or 5 -> play the evolving agent against the 3rd set of fixed weights (2 games, both take their turn going 1st)
        elif (i == 4):
            smartAgent = 1
            agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights) # evolving agent
            agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=opp_strategy, weights=opp_weights[2]) # fixed agent
        elif (i == 5):
            smartAgent = -1
            agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=opp_strategy, weights=opp_weights[2]) # fixed agent
            agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights) # evolving agent



        done = False
        a1_turn = True
        step = 0
        while not (game.isWin(1) or game.isWin(2)) and step < max_steps:
            game, reward = agent1.find_opt_move(game, 1) if a1_turn else agent2.find_opt_move(game, 2)
            a1_turn = not a1_turn
            step += 1

        wins += 1 if smartAgent*game.eval(1, 1) == 1_000_000_000 else 0

    return wins/episodes

def run_genetic_algorithm(num_genes, strategy, opp_strategy, opp_weights, episodes):
    solver = ContinuousGenAlgSolver(
        n_genes=num_genes, 
        fitness_function=lambda weights: nine_mens_morris_fitness_function(
            strategy, weights, opp_strategy, opp_weights, episodes),
        pop_size=10,
        max_gen=60,
        mutation_rate=0.1,
        selection_rate=0.6,
        selection_strategy="roulette_wheel",
        problem_type=float, # Defines the possible values as float numbers
        variables_limits=(-10, 10) # Defines the limits of all variables between -10 and 10. 
                                   # Alternatively one can pass an array of tuples defining the limits
                                   # for each variable: [(-10, 10), (0, 5), (0, 5), (-20, 20)]
    )

    solver.solve()
