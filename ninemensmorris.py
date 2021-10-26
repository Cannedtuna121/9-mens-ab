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
        # The phase of the game we are on
        self.phase1 = True  # Placing phase
        self.phase2 = False # Shifting phase
        self.phase3 = False # Flying phase

    def isMill(self, prev, new):
            return False
    
    def move(self, prev, new, remove):
            return self

    def getValidMoves(self, current_player):
            # Find out what phase the current player is in
            if (current_player == 1):
                if (self.white_pieces_avail > 0):
                    phase = 1
                elif (self.white_pieces_on_board == 3):
                    phase = 3
                else:
                    phase = 2
            else:
                if (self.black_pieces_avail > 0):
                    phase = 1
                elif (self.black_pieces_on_board == 3):
                    phase = 3
                else:
                    phase = 2

            # Finding all possible moves
            valid_moves = np.empty(0, type(self)) # Array of valid states
            if (phase == 1): # Placing One
                for i in range(3):
                    for j in range(8):
                        if (self.board[i][j] == 0): # Empty space
                            if (self.isMill(None, (i, j))): # Check if placing will cause a mill
                                for ii in range(3):
                                    for jj in range(8):
                                        if (current_player % 2 + 1 == self.board[ii][jj] and not self.ismill(None, (ii, jj))):
                                            # If the peice is the other players and not part of a mill remove it
                                            valid_moves = np.append(valid_moves, self.move((None, (i, j), (ii, jj))))
                            else:
                                valid_moves = np.append(valid_moves, self.move(None, (i, j), None)) # Add non-mill state
            elif(phase == 2): # Sliding Phase
                print("Unimplemented")
            else: # Jumpinh phase
                for i in range(3):
                    for j in range(8):
                        if (self.board[i][j] == current_player): # Previously filled space
                            for ii in range(3):
                                for jj in range(8):
                                    if (self.board[ii][jj] == 0): # Empty space
                                        if (self.isMill((i, j), (i, j))): # Check if moving there creates a mill
                                            for iii in range(3):
                                                for jjj in range(8):
                                                    if (current_player % 2 + 1 == self.board[iii][jjj] and not self.ismill(None, (iii, jjj))): # Move and renove peice if it isnt part of a mill
                                                        valid_moves = np.append(valid_moves, self.move(((i, j), (ii, jj), (iii, jjj))))
                                        else:
                                            valid_moves = np.append(valid_moves, self.move((i, j), (ii, jj), None)) # Add non-mill state
                                            
            return valid_moves # Return the possible moves

