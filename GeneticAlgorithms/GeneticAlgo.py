from agents import AlphaBetaAgent, RandomAgent
from ninemensmorris import NineMensMorris
from tqdm import trange
import numpy as np
from geneal.genetic_algorithms import ContinuousGenAlgSolver
from geneal.applications.fitness_functions.continuous import fitness_functions_continuous

def nine_mens_morris_fitness_function(strategy, weights, opp_strategy='random', opp_weights=[], episodes=5):
    weights = [weights[:4], weights[4:12], weights[12:]]
    wins = 0
    max_steps = 100
    
    for i in trange(episodes):

        game = NineMensMorris()
        smartAgent = np.random.choice([-1, 1])
        if smartAgent == 1:
            agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights)
            if opp_strategy == 'random':
                agent2 = RandomAgent()
            else:
                agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                        max_player=1, strategy=opp_strategy, weights=opp_weights)
        else:
            if opp_strategy == 'random':
                agent1 = RandomAgent()
            else:
                agent1 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                        max_player=1, strategy=opp_strategy, weights=opp_weights)
            agent2 = AlphaBetaAgent(upper_lim=1_000_000_000, lower_lim=-1_000_000_000, max_depth=3,
                                    max_player=1, strategy=strategy, weights=weights)



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
