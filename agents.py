import numpy as np

class AlphaBetaAgent:

    def __init__(self, eval, upper_lim=100, lower_lim=-100, max_depth=3, max_player=1):
        """
        Create an agent with an AlphaBeta Strategy.

        :param eval: The evaluation function used to evaluate a NMM board state in alpha_beta
        :type eval: function
        :param upper_lim: The maximum value possible in a given game
        :type upper_lim: float
        :param lower_lim: The minimum value possible in a given game
        :type lower_lim: float
        :param max_depth: The maximum depth to search to
        :type max_depth: int
        :return: None
        """

        self.eval = eval
        self.max = upper_lim
        self.min = lower_lim
        self.max_depth = max_depth
        self.max_player = max_player
    
    def alpha_beta(self, depth, game, p, alpha, beta):
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
            return self.eval(p, 1)
        
        # Get the valid states we can go to from our current state
        valid_moves = game.getValidMoves(p)
        if len(valid_moves) == 0:
            # If we have none and we haven't moved past the root
            # return the current state and it's value
            if depth == 0: return game, self.eval(p, 1)
            # Otherwise return the value of the current state
            return self.eval(p, 1)
        
        # Randomly set an initial best move
        best_move = np.random.choice(valid_moves)

        if p == self.max_player:
            # the best move for max has the lowest initial value
            best = self.min
            
            # go through each valid move
            for state in valid_moves:
                # get the value of that move
                v = self.alpha_beta(depth+1, state, game.get_opp(p), 
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
                v = self.alpha_beta(depth+1, state, game.get_opp(p),
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

        
    def find_opt_move(self, game, player):
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
        return self.alpha_beta(0, game, player, self.min, self.max)


class HumanAgent:

    def __init__(self):
        # Nothing has to be done on init currently
        return

    def find_opt_move(self, game, player):
        # print the board
        game.printBoard()

        # determine the phase
        if (player == 1):
            phase = game.white_phase
        elif (player == 2):
            phase = game.black_phase

        while (True):
            if (phase == 1):
                print("Place piece at: ")
                pos = self.read_position()
                if game.board[pos[0]][pos[1]] == 0:
                    if (game.isMill(None, pos, player)):
                        # Note: Piece removal is not validated
                        print("Enter piece to remove: ")
                        rem_pos = self.read_position()
                        return game.move(None, pos, rem_pos, player) , 0
                    else:
                        return game.move(None, pos, None, player), 0
                print("Invalid Move, Try Again")
            elif (phase == 2):
                print("Slide piece at: ")
                pos = self.read_position()
                if (game.board[pos[0]][pos[1]] == player):
                    slide_dir = input("Enter slide direction (u, d, l , r)")
                    new_pos = game.newSlidePosition(pos, slide_dir)
                    if (new_pos != None and game.board[new_pos[0]][new_pos[1]] == 0):
                        if (game.isMill(pos, new_pos, player)):
                            # Note: Piece removal is not validated
                            print("Enter piece to remove: ")
                            rem_pos = self.read_position()
                            return game.move(pos, new_pos, rem_pos, player), 0
                        else:
                            return game.move(pos, new_pos, None, player), 0
                print("Invalid Move, Try Again")
            else:
                print("Jump piece at: ")
                pos = self.read_position()
                if (game.board[pos[0]][pos[1]] == player):
                    print("Enter jump location: ")
                    new_pos = self.read_position()
                    if (game.board[new_pos[0]][new_pos[1]] == 0):
                        if (game.isMill(pos, new_pos, player)):
                            # Note: Piece removal is not validated
                            print("Enter piece to remove: ")
                            rem_pos = self.read_position()
                            return game.move(pos, new_pos, rem_pos, player), 0
                        else:
                            return game.move(pos, new_pos, None, player), 0
                print("Invalid Move, Try Again")


    def read_position(self):
        while (True):
            playerInput = input().split()
            if (len(playerInput) != 2):
                print("Invalid Input")
            try:
                playerInput[0] = int(playerInput[0])
                playerInput[1] = int(playerInput[1])
                if (playerInput[0] >= 0 and playerInput[0] <= 2 and
                        playerInput[1] >= 0 and playerInput[1] <= 7):
                    return (playerInput[0], playerInput[1])
                else:
                    print("Out of bounds")
            except TypeError:
                print("Input must be integers")


class RandomAgent:

    def __init__(self):
        """
        Create an agent with a Random Strategy.

        :param game: A game object that we can use to get and execute moves
        :type game: Game (TicTacToe, NineMensMorris)
        :return: None
        """
#         self.game = game

    def find_opt_move(self, game, player):
        """
        Find the optimal move using alpha beta.

        :param player: player that is making the move in the current game state
        :type player: string (flexible)
        :return: best move and its predicted value
        :rtype: string, float
        """
        # Get the agent's valid moves
        valid_moves = game.getValidMoves(player)
        if len(valid_moves) == 0: 
            # If we have no valid moves, use the current state
            new_game = game
        else: 
            # Otherwise randomly choose the next state 
            new_game = np.random.choice(valid_moves)

        # Return the next state and its value
        return new_game, game.eval(player, 1)
