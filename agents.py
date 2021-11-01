import numpy as np

class AlphaBetaAgent:

    def __init__(self, game, upper_lim=100, lower_lim=-100, max_depth=3):
        self.game = game
        self.max = upper_lim
        self.min = lower_lim
        self.max_depth = max_depth
    
    def alpha_beta(self, depth, s, p, alpha, beta):
        if depth == self.max_depth:
            return self.game.eval(s)
        
        valid_moves = self.game.get_valid_moves(s, p)
        if len(valid_moves) == 0:
            if depth == 0: return s, self.game.eval(s)
            return self.game.eval(s)
        
        best_move = np.random.choice(valid_moves)

        if p == self.game.p1:
            best = self.min

            for state in valid_moves:
                v = self.alpha_beta(depth+1, state, self.game.get_opp(p), 
                                    alpha, beta)
                best = max(best, v)
                if best > alpha:
                    best_move = state
                    alpha = best

                if beta <= alpha:
                    break
        else:
            best = self.max

            for state in valid_moves:
                v = self.alpha_beta(depth+1, state, self.game.get_opp(p),
                                    alpha, beta)  
                best = min(best, v)
                if best < beta:
                    best_move = state
                    beta = best

                if beta <= alpha:
                    break
        
        if depth == 0:
            return best_move, best
        else:
            return best

        
    def find_opt_move(self, player):
        return self.alpha_beta(0, self.game.state, player, self.min, self.max)

class RandomAgent:

    def __init__(self, game):
        self.game = game

    def find_opt_move(self, player):
        valid_moves = self.game.get_valid_moves(self.game.state, player)
        if len(valid_moves) == 0: 
            state = game.state
        else: 
            state = np.random.choice(valid_moves)

        return state, self.game.eval(state)
