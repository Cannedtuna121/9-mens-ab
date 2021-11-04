import numpy as np

class AlphaBetaAgent:

    def __init__(self, game, upper_lim=100, lower_lim=-100, max_depth=3):
        """
        Create an agent with an AlphaBeta Strategy.

        :param game: A game object that we can use to get and execute moves
        :type game: Game (TicTacToe, NineMensMorris)
        :param upper_lim: The maximum value possible in a given game
        :type upper_lim: float
        :param lower_lim: The minimum value possible in a given game
        :type lower_lim: float
        :param max_depth: The maximum depth to search to
        :type max_depth: int
        :return: None
        """
        self.game = game
        self.max = upper_lim
        self.min = lower_lim
        self.max_depth = max_depth
    
    def alpha_beta(self, depth, s, p, alpha, beta):
        """
        Run alpha beta strategy at the current state.

        :param depth: current depth
        :type depth: int
        :param s: current state
        :type s: string (flexible)
        :param p: current player
        :type p: string (flexible)
        :param alpha: current value of alpha
        :type alpha: float
        :param beta: current value of beta
        :type beta: float
        :return: either the best move and its value at depth max_depth
                 or just the value at max_depth if an interior or leaf node
        :rtype: (string, float) or float
        """
        # If we are at the depth we want to search to, 
        # evaluate the current state
        if depth == self.max_depth:
            return self.game.eval(s)
        
        # Get the valid states we can go to from our current state
        valid_moves = self.game.get_valid_moves(s, p)
        if len(valid_moves) == 0:
            # If we have none and we haven't moved past the root
            # return the current state and it's value
            if depth == 0: return s, self.game.eval(s)
            # Otherwise return the value of the current state
            return self.game.eval(s)
        
        # Randomly set an initial best move
        best_move = np.random.choice(valid_moves)

        if p == self.game.p1:
            # the best move for max has the lowest initial value
            best = self.min
            
            # go through each valid move
            for state in valid_moves:
                # get the value of that move
                v = self.alpha_beta(depth+1, state, self.game.get_opp(p), 
                                    alpha, beta)
                # best move maximizes value
                best = max(best, v)

                # alpha and best move are updated - alpha maximizes value
                if best > alpha:
                    best_move = state
                    alpha = best
                
                # alpha cutoff
                if beta <= alpha:
                    break
        else:
            # the best move for min has the highest initial value
            best = self.max

            # go through each valid move
            for state in valid_moves:
                # get the value of that move
                v = self.alpha_beta(depth+1, state, self.game.get_opp(p),
                                    alpha, beta)  
                # best move minimizes value
                best = min(best, v)

                # beta and best move are updated - alpha maximizes value
                if best < beta:
                    best_move = state
                    beta = best

                # beta cutoff
                if beta <= alpha:
                    break

        # find_opt_move should get both the best move and its value        
        if depth == 0:
            return best_move, best
        else:
            # alpha beta only needs the best value
            return best

        
    def find_opt_move(self, player):
        """
        Find the optimal move using alpha beta.

        :param player: player that is making the move in the current game state
        :type player: string (flexible)
        :return: best move and its predicted value
        :rtype: string, float
        """
        # start at depth 0 with the current state
        # with the given player's turn to move
        # initially set alpha to be min and beta to be max
        return self.alpha_beta(0, self.game.state, player, self.min, self.max)

class RandomAgent:

    def __init__(self, game):
        """
        Create an agent with a Random Strategy.

        :param game: A game object that we can use to get and execute moves
        :type game: Game (TicTacToe, NineMensMorris)
        :return: None
        """
        self.game = game

    def find_opt_move(self, player):
        """
        Find the optimal move using alpha beta.

        :param player: player that is making the move in the current game state
        :type player: string (flexible)
        :return: best move and its predicted value
        :rtype: string, float
        """
        # Get the agent's valid moves
        valid_moves = self.game.get_valid_moves(self.game.state, player)
        if len(valid_moves) == 0: 
            # If we have no valid moves, use the current state
            state = game.state
        else: 
            # Otherwise randomly choose the next state 
            state = np.random.choice(valid_moves)

        # Return the next state and its value
        return state, self.game.eval(state)
