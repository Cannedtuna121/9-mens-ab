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

    def isMill(self, prev, new, player):
        result = False
        # Create a copy of the board with the piece in location 'prev' removed (if 'prev' is not null)
        temp_board = np.copy(self.board)
        if prev != None:
            temp_board[prev[0]][prev[1]] = 0

        # cases where 'new' piece is in a corner
        if new[1] == 0:
            if temp_board[new[0]][1] == player and temp_board[new[0]][2] == player:
                result = True
            elif temp_board[new[0]][7] == player and temp_board[new[0]][6] == player:
                result = True
        elif new[1] == 2:
            if temp_board[new[0]][1] == player and temp_board[new[0]][0] == player:
                result = True
            elif temp_board[new[0]][3] == player and temp_board[new[0]][4] == player:
                result = True
        elif new[1] == 4:
            if temp_board[new[0]][5] == player and temp_board[new[0]][6] == player:
                result = True
            elif temp_board[new[0]][3] == player and temp_board[new[0]][2] == player:
                result = True
        elif new[1] == 6:
            if temp_board[new[0]][5] == player and temp_board[new[0]][4] == player:
                result = True
            elif temp_board[new[0]][7] == player and temp_board[new[0]][0] == player:
                result = True
        # cases where 'new' piece is not in a corner
        elif new[1] == 1:
            if temp_board[new[0]][0] == player and temp_board[new[0]][2] == player:
                result = True
            elif self.checkInwardLines(temp_board, new, player):
                result = True
        elif new[1] == 3:
            if temp_board[new[0]][2] == player and temp_board[new[0]][4] == player:
                result = True
            elif self.checkInwardLines(temp_board, new, player):
                result = True
        elif new[1] == 5:
            if temp_board[new[0]][4] == player and temp_board[new[0]][6] == player:
                result = True
            elif self.checkInwardLines(temp_board, new, player):
                result = True
        elif new[1] == 7:
            if temp_board[new[0]][6] == player and temp_board[new[0]][0] == player:
                result = True
            elif self.checkInwardLines(temp_board, new, player):
                result = True

        return result
    
    # Helper function for isMill: checks if a mill is present on the appropriate inward line
    def checkInwardLines(self, temp_board, new, player):
        result = False

        if new[0] == 0: # outer square
            if temp_board[1][new[1]] == player and temp_board[2][new[1]] == player:
                result = True
        elif new[0] == 1: # middle square
            if temp_board[0][new[1]] == player and temp_board[2][new[1]] == player:
                result = True
        else: # inner square
            if temp_board[0][new[1]] == player and temp_board[1][new[1]] == player:
                result = True
        
        return result
    
    def newState(self):
            temp = NineMensMorris()
            temp.board = np.copy(self.board)
            temp.white_pieces_on_board = self.white_pieces_on_board
            temp.black_pieces_on_board = self.black_pieces_on_board
            temp.white_pieces_avail = self.white_pieces_avail
            temp.black_pieces_avail = self.black_pieces_avail
            temp.white_phase = self.white_phase
            temp.black_phase = self.black_phase
            return temp
    
    def move(self, prev, new, remove, player):
            temp = self.newState()
            #player is placing down a piece removing 1 from available pieces
            if prev == None:
                if player == 1:
                    temp.board[new[0]][new[1]] = 1
                    temp.white_pieces_avail = self.white_pieces_avail - 1
                    #If there are no more available pieces set phase to sliding
                    if temp.white_pieces_avail == 0:
                        temp.white_phase = self.white_phase + 1
                    #remove piece if remove isn't none
                    if remove != None:
                        temp.board[remove[0]][remove[1]] = 0
                        temp.black_pieces_on_board = temp.black_pieces_on_board - 1
                        #if black only has 3 pieces left set it to jump phase
                        if temp.black_pieces_on_board == 3 and temp.black_pieces_avail == 0:
                            temp.black_phase = 3
                else:
                    temp.board[new[0]][new[1]] = 2
                    temp.black_pieces_avail = self.black_pieces_avail - 1
                    if temp.black_pieces_avail == 0:
                        temp.black_phase = self.black_phase + 1
                    #remove piece if remove isn't none
                    if remove != None:
                        temp.board[remove[0]][remove[1]] = 0
                        temp.white_pieces_on_board = temp.white_pieces_on_board - 1
                        #if white only has 3 pieces left set it to jump phase
                        if temp.white_pieces_on_board == 3 and temp.white_pieces_avail == 0:
                            temp.white_phase = 3
            else:
                #either a slide or a jump, both cases set prev position to 0 and new 
                #to 1 or 2 depending on which player is making the move
                temp.board[prev[0]][prev[1]] = 0
                if player == 1:
                    temp.board[new[0]][new[1]] = 1
                    #remove piece if remove isn't none
                    if remove != None:
                        temp.board[remove[0]][remove[1]] = 0
                        temp.black_pieces_on_board = temp.black_pieces_on_board - 1
                        #if black only has 3 pieces left set it to jump phase
                        if temp.black_pieces_on_board == 3:
                            temp.black_phase = 3
                else:
                    temp.board[new[0]][new[1]] = 1
                    #remove piece if remove isn't none
                    if remove != None:
                        temp.board[remove[0]][remove[1]] = 0
                        temp.white_pieces_on_board = temp.white_pieces_on_board - 1
                        #if white only has 3 pieces left set it to jump phase
                        if temp.white_pieces_on_board == 3:
                            temp.white_phase = 3
            return temp

    def getValidMoves(self, current_player):
            # Find out what phase the current player is in
            if (current_player == 1):
                phase = self.white_phase
            else:
                phase = self.black_phase

            # Finding all possible moves
            valid_moves = [] # Array of valid states
            if (phase == 1): # Placing Phase
                for i in range(3):
                    for j in range(8):
                        if (self.board[i][j] == 0): # Empty space
                            if (self.isMill(None, (i, j), current_player)): # Check if placing will cause a mill
                                self.expandMillMove(None, (i, j), current_player, valid_moves)              
                            else:
                                valid_moves.append(self.move(None, (i, j), None, current_player)) # Add non-mill state
            elif(phase == 2): # Sliding Phase
                for i in range(3):
                    for j in range(8):
                        if (self.board[i][j] == current_player): # Previously filled space
                            for direction in ['u', 'd', 'l', 'r']:
                                new = self.newSlidePosition((i, j), direction)
                                if (new == None or self.board[new[0]][new[1]] != 0): # Make sure move is valid and has an empty space
                                    continue

                                if (self.isMill((i, j), new, current_player)): # check if moving there creates a mill
                                    self.expandMillMove((i, j), new, current_player, valid_moves)
                                else:
                                    valid_moves.append(self.move((i, j), new, None, current_player)) # Add non-mill state
            else: # Jumping phase
                for i in range(3):
                    for j in range(8):
                        if (self.board[i][j] == current_player): # Previously filled space
                            for ii in range(3):
                                for jj in range(8):
                                    if (self.board[ii][jj] == 0): # Empty space
                                        if (self.isMill((i, j), (ii, jj), current_player)): # Check if moving there creates a mill
                                            self.expandMillMove((i, j), (ii, jj), current_player, valid_moves)
                                        else:
                                            valid_moves.append(self.move((i, j), (ii, jj), None, current_player)) # Add non-mill state
                                            
            return valid_moves # Return the possible moves

    # Helper function that determins the new position of a peice after a slide in a direction
    def newSlidePosition(self, prev, slide):
        if (prev == None):
            return None

        pb = prev[0]
        pl = prev[1]

        # Possible up moves
        if (slide == 'u'):
           if (pl == 3 or pl == 4):
              return (pb, pl -1)
           elif (pl == 6):
               return (pb, 7)
           elif (pl == 7):
               return (pb, 0)
           elif (pl == 1):
               if (pb != 0):
                   return (pb - 1, pl)
           elif (pl == 5):
               if (pb != 2):
                   return (pb + 1, pl)

        # Possible down moves
        elif (slide == 'd'):
            if (pl == 2 or pl == 3):
                return (pb, pl + 1)
            elif (pl == 0):
                return (pb, 7)
            elif (pl == 7):
                return (pb, 6)
            elif (pl == 1):
                if (pb != 2):
                    return (pb + 1, pl)
            elif (pl == 5):
                if (pb != 0):
                    return (pb - 1, pl)

        # Possible left moves
        elif (slide == 'l'):
            if (pl == 1 or pl == 2):
                return (pb, pl - 1)
            elif (pl == 4 or pl == 5):
                return (pb, pl + 1)
            elif (pl == 3):
                if (pb != 2):
                    return (pb + 1, pl)
            elif (pl == 7):
                if (pb != 0):
                    return (pb - 1, pl)

        # Possible right moves
        elif (slide == 'r'):
            if (pl == 0 or pl == 1):
                return (pb, pl + 1)
            elif (pl == 5 or pl == 6):
                return (pb, pl - 1)
            elif (pl == 3):
                if (pb != 0):
                    return (pb - 1, pl)
            elif (pl == 7):
                if (pb != 2):
                    return (pb + 1, pl)

        return None

    # Helper function that expands moves that require a player to remove an enemy peice 
    def expandMillMove(self, prev, new, current_player, valid_moves):
        opponent_peices_in_mill = []
        found_non_mill = False
        for i in range(3):
            for j in range(8):
                if (self.board[i][j] == current_player % 2 + 1):
                    if (not self.isMill(None, (i, j), current_player)):
                        # If the peice is the other players and not part of a mill remove it
                        valid_moves.append(self.move(prev, new, (i, j), current_player))
                        found_non_mill = True
                    elif (not found_non_mill):
                        # If we have not found a peice outside of a mill, put keep track of peices in mills
                        opponent_peices_in_mill.append((i, j))
        if (not found_non_mill):
            for m in opponent_peices_in_mill:
                # If there are only peices that are part of a mill, make moves that remove them
                valid_moves.append(self.move(prev, new, (m[0], m[1]), current_player))


