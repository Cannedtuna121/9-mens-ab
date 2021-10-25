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
