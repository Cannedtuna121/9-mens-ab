# Nine Men's Morris Game

import numpy as np

class NineMensMorris:
    # Constructor for the game: creates a new game with an empty board and 9 pieces for each player
    def __init__(self):
        # The game board: first array is outer square, second is middle square, third is inner square
        # 0 represents an empty space, 1 represents a white piece, 2 represents a black piece
        self.board = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0], # Outer square: first entry is top left, last entry is middle left (CW)
            [0, 0, 0, 0, 0, 0, 0, 0], # Middle square: first entry is top left, last entry is middle left (CW)
            [0, 0, 0, 0, 0, 0, 0, 0], # Inner square: first entry is top left, last entry is middle left (CW)
        ])
        # The number of pieces currently on the board for each player
        self.white_pieces_on_board = 0
        self.black_pieces_on_board = 0
        # The number of pieces available to be placed by each player
        self.white_pieces_avail = 9
        self.black_pieces_avail = 9
        # The phase of the game we are on for each player
        # 1 = placing phase, 2 = sliding phase, 3 = flying phase
        self.white_phase = 1
        self.black_phase = 1

    def isMill(self, prev, new):
            return True
    
    def move(self, prev, new, remove):
            return self

    def getValidMoves(self, current_player):
            # Find out what phase the current player is in
            if (current_player == 1):
                phase = self.white_phase
            else:
                phase = self.black_phase

            # Finding all possible moves
            valid_moves = [] # Array of valid states
            if (phase == 1): # Placing One
                for i in range(3):
                    for j in range(8):
                        if (self.board[i][j] == 0): # Empty space
                            if (self.isMill(None, (i, j))): # Check if placing will cause a mill
                                self.expandMillMove(None, (i, j), current_player, valid_moves)              
                            else:
                                valid_moves.append(self.move(None, (i, j), None)) # Add non-mill state
            elif(phase == 2): # Sliding Phase
                print("Unimplemented")
            else: # Jumpinh phase
                for i in range(3):
                    for j in range(8):
                        if (self.board[i][j] == current_player): # Previously filled space
                            for ii in range(3):
                                for jj in range(8):
                                    if (self.board[ii][jj] == 0): # Empty space
                                        if (self.isMill((i, j), (ii, jj))): # Check if moving there creates a mill
                                            self.expandMillMove((i, j), (ii, jj), current_player, valid_moves)
                                        else:
                                            valid_moves.append(self.move((i, j), (ii, jj), None)) # Add non-mill state
                                            
            return valid_moves # Return the possible moves
   
    # Helper function that expands moves that require a player to remove an enemy peice 
    def expandMillMove(self, prev, new, current_player, valid_moves):
        opponent_peices_in_mill = []
        found_non_mill = False
        for i in range(3):
            for j in range(8):
                if (self.board[i][j] == current_player % 2 + 1):
                    if (not self.isMill(None, (i, j))):
                        # If the peice is the other players and not part of a mill remove it
                        valid_moves.append(self.move(prev, new, (i, j)))
                        found_non_mill = True
                    elif (not found_non_mill):
                        opponent_peices_in_mill.append((i, j))
        if (not found_non_mill):
            for m in opponent_peices_in_mill:
                valid_moves.append(self.move(prev, new, (m[0], m[1])))


