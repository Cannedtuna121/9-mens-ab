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
        
        self.get_opp = lambda p: (p%2 + 1)

    # Function to help with debugging, prints a visual representation of the board
    def printBoard(self):
        print(str(self.board[0][0]) + "─────────" + str(self.board[0][1]) + "─────────" + str(self.board[0][2]))
        print("┃         ┃         ┃")
        print("┃   " + str(self.board[1][0]) + "─────" + str(self.board[1][1]) + "─────" + str(self.board[1][2]) + "   ┃")
        print("┃   ┃     ┃     ┃   ┃")
        print("┃   ┃  " + str(self.board[2][0]) + "──" + str(self.board[2][1]) + "──" + str(self.board[2][2]) + "  ┃   ┃")
        print("┃   ┃  ┃     ┃  ┃   ┃")
        print(str(self.board[0][7]) + "───" + str(self.board[1][7]) + "──" + str(self.board[2][7]) + "     " + str(self.board[2][3]) + "──" + str(self.board[1][3]) + "───" + str(self.board[0][3]))
        print("┃   ┃  ┃     ┃  ┃   ┃")
        print("┃   ┃  " + str(self.board[2][6]) + "──" + str(self.board[2][5]) + "──" + str(self.board[2][4]) + "  ┃   ┃")
        print("┃   ┃     ┃     ┃   ┃")
        print("┃   " + str(self.board[1][6]) + "─────" + str(self.board[1][5]) + "─────" + str(self.board[1][4]) + "   ┃")
        print("┃         ┃         ┃")
        print(str(self.board[0][6]) + "─────────" + str(self.board[0][5]) + "─────────" + str(self.board[0][4]))

    def isMill(self, prev, new, player):
        result = False
        # Create a copy of the board with the piece in location 'prev' removed (if 'prev' is not None)
        if prev == None:
            temp_board = self.board
        else:
            temp_board = np.copy(self.board)
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
                    temp.white_pieces_on_board += 1
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
                    temp.black_pieces_on_board += 1
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
                    temp.board[new[0]][new[1]] = 2
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
                    if (not self.isMill(None, (i, j), current_player % 2 + 1)):
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


    def isWin(self, player):
        (white, black) = self.blockedInWhiteThenBlack()
        if (self.white_phase > 1 and self.black_phase > 1):
            if (player == 1):
                return self.black_pieces_on_board <= 2 or black == self.black_pieces_on_board
            else: return self.white_pieces_on_board <= 2 or white == self.white_pieces_on_board
        else:
            return False

    def minSlidesToMill(self, current_player):
        seen = {}
        originalLocation = []
        queue = []
        pieceNum = 0
        for i in range(3):
            for j in range(8):
                if (self.board[i][j] == current_player):
                    queue.append((pieceNum, (i, j), 0))
                    seen[(pieceNum, (i, j))] = True
                    originalLocation.append((i, j))
                    pieceNum += 1
        while (len(queue) > 0):
           cur = queue[0]
           del queue[0]
           for direction in ['u', 'd', 'l', 'r']:
               new = self.newSlidePosition(cur[1], direction)
               if (not new == None and self.board[new[0]][new[1]] == 0):
                   if (not (cur[0], new) in seen):
                       if (self.isMill(originalLocation[cur[0]], new, current_player)):
                           return cur[2] + 1
                       else:
                           seen[(cur[0], new)] = True
                           queue.append((cur[0], new, cur[2] + 1))
        return 25

    
    # Returns the given players' number of mills minus the opponents number of mills
    def millDifference(self, player):
        white_mill_count = 0
        black_mill_count = 0

        # Count the number of mills in outer square
        outer_result = self.millCount(0)
        white_mill_count += outer_result[0]
        black_mill_count += outer_result[1]
        # Count the number of mills in middle square
        middle_result = self.millCount(1)
        white_mill_count += middle_result[0]
        black_mill_count += middle_result[1]
        # Count the number of mills in inner square
        inner_result = self.millCount(2)
        white_mill_count += inner_result[0]
        black_mill_count += inner_result[1]
        # Count the number of mills on inward lines
        if (self.board[0][1] == 1 and self.board[1][1] == 1 and self.board[2][1] == 1):
            white_mill_count += 1
        elif (self.board[0][1] == 2 and self.board[1][1] == 2 and self.board[2][1] == 2):
            black_mill_count += 1
        if (self.board[0][3] == 1 and self.board[1][3] == 1 and self.board[2][3] == 1):
            white_mill_count += 1
        elif (self.board[0][3] == 2 and self.board[1][3] == 2 and self.board[2][3] == 2):
            black_mill_count += 1
        if (self.board[0][5] == 1 and self.board[1][5] == 1 and self.board[2][5] == 1):
            white_mill_count += 1
        elif (self.board[0][5] == 2 and self.board[1][5] == 2 and self.board[2][5] == 2):
            black_mill_count += 1
        if (self.board[0][7] == 1 and self.board[1][7] == 1 and self.board[2][7] == 1):
            white_mill_count += 1
        elif (self.board[0][7] == 2 and self.board[1][7] == 2 and self.board[2][7] == 2):
            black_mill_count += 1

        if (player == 1):
            return white_mill_count - black_mill_count
        else:
            return black_mill_count - white_mill_count
    

    # Helper function for millDifference: counts the number of mills in the given part of the
    # board (i.e., outer (0), middle (1), or inner square (2))
    def millCount(self, part_of_board):
        white_mill_count = 0
        black_mill_count = 0

        if (self.board[part_of_board][0] == 1 and self.board[part_of_board][1] == 1 and self.board[part_of_board][2] == 1):
            white_mill_count += 1
        elif (self.board[part_of_board][0] == 2 and self.board[part_of_board][1] == 2 and self.board[part_of_board][2] == 2):
            black_mill_count += 1
        if (self.board[part_of_board][0] == 1 and self.board[part_of_board][7] == 1 and self.board[part_of_board][6] == 1):
            white_mill_count += 1
        elif (self.board[part_of_board][0] == 2 and self.board[part_of_board][7] == 2 and self.board[part_of_board][6] == 2):
            black_mill_count += 1
        if (self.board[part_of_board][4] == 1 and self.board[part_of_board][5] == 1 and self.board[part_of_board][6] == 1):
            white_mill_count += 1
        elif (self.board[part_of_board][4] == 2 and self.board[part_of_board][5] == 2 and self.board[part_of_board][6] == 2):
            black_mill_count += 1
        if (self.board[part_of_board][4] == 1 and self.board[part_of_board][3] == 1 and self.board[part_of_board][2] == 1):
            white_mill_count += 1
        elif (self.board[part_of_board][4] == 2 and self.board[part_of_board][3] == 2 and self.board[part_of_board][2] == 2):
            black_mill_count += 1
        
        return (white_mill_count, black_mill_count)

    # The number of pieces which can't move
    def blockedInWhiteThenBlack(self):
        white_blocked_in = 0
        black_blocked_in = 0
        
        corners_result = self.cornerPiecesBlocked()
        white_blocked_in += corners_result[0]
        black_blocked_in += corners_result[1]

        # i = 1, 3, 5, 7: non-corner spaces
        for i in range(1, 8, 2):
            temp = i + 1
            if (temp == 8): temp = 0

            if (self.board[0][i] == 1 and self.board[0][i - 1] != 0 and self.board[0][temp] != 0 and self.board[1][i] != 0):
                white_blocked_in += 1
            elif (self.board[0][i] == 2 and self.board[0][i - 1] != 0 and self.board[0][temp] != 0 and self.board[1][i] != 0):
                black_blocked_in += 1
            if (self.board[1][i] == 1 and self.board[0][i] != 0 and self.board[2][i] != 0 and self.board[1][i - 1] != 0 and self.board[1][temp] != 0):
                white_blocked_in += 1
            elif (self.board[1][i] == 2 and self.board[0][i] != 0 and self.board[2][i] != 0 and self.board[1][i - 1] != 0 and self.board[1][temp] != 0):
                black_blocked_in += 1
            if (self.board[2][i] == 1 and self.board[1][i] != 0 and self.board[2][i - 1] != 0 and self.board[2][temp] != 0):
                white_blocked_in += 1
            elif (self.board[2][i] == 2 and self.board[1][i] != 0 and self.board[2][i - 1] != 0 and self.board[2][temp] != 0):
                black_blocked_in += 1

        # Do not count any pieces as being blocked in if the player is in the flying phase
        if (self.black_phase == 3): black_blocked_in = 0
        if (self.white_phase == 3): white_blocked_in = 0

        return (white_blocked_in, black_blocked_in)

    # The number of opponents pieces which can't move minus the number of player pieces which can't move
    def blockedInDifference(self, player):
        (white, black) = self.blockedInWhiteThenBlack()
        if player == 1: return black - white
        else: return white - black

    # Helper function for blockedInDifference: returns the number of corner pieces which are blocked in
    # for each player
    def cornerPiecesBlocked(self):
        white_blocked_in = 0
        black_blocked_in = 0

        # Count the number of blocked in pieces for each player in each corner
        for i in range(3):
            if (self.board[i][0] == 1 and self.board[i][1] != 0 and self.board[i][7] != 0):
                white_blocked_in += 1
            elif (self.board[i][0] == 2 and self.board[i][1] != 0 and self.board[i][7] != 0):
                black_blocked_in += 1
            if (self.board[i][2] == 1 and self.board[i][1] != 0 and self.board[i][3] != 0):
                white_blocked_in += 1
            elif (self.board[i][2] == 2 and self.board[i][1] != 0 and self.board[i][3] != 0):
                black_blocked_in += 1
            if (self.board[i][4] == 1 and self.board[i][3] != 0 and self.board[i][5] != 0):
                white_blocked_in += 1
            elif (self.board[i][4] == 2 and self.board[i][3] != 0 and self.board[i][5] != 0):
                black_blocked_in += 1
            if (self.board[i][6] == 1 and self.board[i][5] != 0 and self.board[i][7] != 0):
                white_blocked_in += 1
            elif (self.board[i][6] == 2 and self.board[i][5] != 0 and self.board[i][7] != 0):
                black_blocked_in += 1
        
        return (white_blocked_in, black_blocked_in)

    # spammable mill piece = a piece in a mill which you can continuously move out of the mill
    # and back into the mill without risk of the opponent preventing your mill.
    # Returns: number of spammable mill pieces of given player - number of spammable mill pieces of opponent
    def spammableMillPiecesDifference(self, player):
        white_result = 0
        black_result = 0

        # i = 0, 1, 2
        for i in range(3):
            #### Horizontal mills ####
            if (self.board[i][0] == 1 and self.board[i][1] == 1 and self.board[i][2] == 1):
                # Top left is spammable (i, 0)
                if (self.board[i][7] == 0):
                    white_result += 1
                # Top right is spammable (i, 2)
                if (self.board[i][3] == 0):
                    white_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][1] == 0):
                    white_result += 1
                elif (i == 1):
                    if (self.board[0][1] == 0 and self.board[2][1] == 0):
                        white_result += 1
                    elif (self.board[0][1] == 1 and self.board[2][1] == 0):
                        white_result += 1
                    elif (self.board[0][1] == 0 and self.board[2][1] == 1):
                        white_result += 1
                elif (i == 2 and self.board[1][1] == 0):
                    white_result += 1
            elif (self.board[i][0] == 2 and self.board[i][1] == 2 and self.board[i][2] == 2):
                # Top left is spammable (i, 0)
                if (self.board[i][7] == 0):
                    black_result += 1
                # Top right is spammable (i, 2)
                if (self.board[i][3] == 0):
                    black_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][1] == 0):
                    black_result += 1
                elif (i == 1):
                    if (self.board[0][1] == 0 and self.board[2][1] == 0):
                        black_result += 1
                    elif (self.board[0][1] == 2 and self.board[2][1] == 0):
                        black_result += 1
                    elif (self.board[0][1] == 0 and self.board[2][1] == 2):
                        black_result += 1
                elif (i == 2 and self.board[1][1] == 0):
                    black_result += 1
            if (self.board[i][4] == 1 and self.board[i][5] == 1 and self.board[i][6] == 1):
                # Bottom left is spammable (i, 6)
                if (self.board[i][7] == 0):
                    white_result += 1
                # Bottom right is spammable (i, 4)
                if (self.board[i][3] == 0):
                    white_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][5] == 0):
                    white_result += 1
                elif (i == 1):
                    if (self.board[0][5] == 0 and self.board[2][5] == 0):
                        white_result += 1
                    elif (self.board[0][5] == 1 and self.board[2][5] == 0):
                        white_result += 1
                    elif (self.board[0][5] == 0 and self.board[2][5] == 1):
                        white_result += 1
                elif (i == 2 and self.board[1][5] == 0):
                    white_result += 1
            elif (self.board[i][4] == 2 and self.board[i][5] == 2 and self.board[i][6] == 2):
                # Bottom left is spammable (i, 6)
                if (self.board[i][7] == 0):
                    black_result += 1
                # Bottom right is spammable (i, 4)
                if (self.board[i][3] == 0):
                    black_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][5] == 0):
                    black_result += 1
                elif (i == 1):
                    if (self.board[0][5] == 0 and self.board[2][5] == 0):
                        black_result += 1
                    elif (self.board[0][5] == 2 and self.board[2][5] == 0):
                        black_result += 1
                    elif (self.board[0][5] == 0 and self.board[2][5] == 2):
                        black_result += 1
                elif (i == 2 and self.board[1][5] == 0):
                    black_result += 1
            #### Vertical mills ####
            if (self.board[i][0] == 1 and self.board[i][7] == 1 and self.board[i][6] == 1):
                # Top left is spammable (i, 0)
                if (self.board[i][1] == 0):
                    white_result += 1
                # Bottom left is spammable (i, 6)
                if (self.board[i][5] == 0):
                    white_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][7] == 0):
                    white_result += 1
                elif (i == 1):
                    if (self.board[0][7] == 0 and self.board[2][7] == 0):
                        white_result += 1
                    elif (self.board[0][7] == 1 and self.board[2][7] == 0):
                        white_result += 1
                    elif (self.board[0][7] == 0 and self.board[2][7] == 1):
                        white_result += 1
                elif (i == 2 and self.board[1][7] == 0):
                    white_result += 1
            elif (self.board[i][0] == 2 and self.board[i][7] == 2 and self.board[i][6] == 2):
                # Top left is spammable (i, 0)
                if (self.board[i][1] == 0):
                    black_result += 1
                # Bottom left is spammable (i, 6)
                if (self.board[i][5] == 0):
                    black_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][7] == 0):
                    black_result += 1
                elif (i == 1):
                    if (self.board[0][7] == 0 and self.board[2][7] == 0):
                        black_result += 1
                    elif (self.board[0][7] == 2 and self.board[2][7] == 0):
                        black_result += 1
                    elif (self.board[0][7] == 0 and self.board[2][7] == 2):
                        black_result += 1
                elif (i == 2 and self.board[1][7] == 0):
                    black_result += 1
            if (self.board[i][2] == 1 and self.board[i][3] == 1 and self.board[i][4] == 1):
                # Top right is spammable (i, 2)
                if (self.board[i][1] == 0):
                    white_result += 1
                # Bottom right is spammable (i, 4)
                if (self.board[i][5] == 0):
                    white_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][3] == 0):
                    white_result += 1
                elif (i == 1):
                    if (self.board[0][3] == 0 and self.board[2][3] == 0):
                        white_result += 1
                    elif (self.board[0][3] == 1 and self.board[2][3] == 0):
                        white_result += 1
                    elif (self.board[0][3] == 0 and self.board[2][3] == 1):
                        white_result += 1
                elif (i == 2 and self.board[1][3] == 0):
                    white_result += 1
            elif (self.board[i][2] == 2 and self.board[i][3] == 2 and self.board[i][4] == 2):
                # Top right is spammable (i, 2)
                if (self.board[i][1] == 0):
                    black_result += 1
                # Bottom right is spammable (i, 4)
                if (self.board[i][5] == 0):
                    black_result += 1
                # Check if middle mill pieces are spammable
                if (i == 0 and self.board[1][3] == 0):
                    black_result += 1
                elif (i == 1):
                    if (self.board[0][3] == 0 and self.board[2][3] == 0):
                        black_result += 1
                    elif (self.board[0][3] == 2 and self.board[2][3] == 0):
                        black_result += 1
                    elif (self.board[0][3] == 0 and self.board[2][3] == 2):
                        black_result += 1
                elif (i == 2 and self.board[1][3] == 0):
                    black_result += 1

        # Now check mills on inward lines
        # i = 1, 3, 5, 7
        for i in range(1, 8, 2):
            temp = i + 1
            if temp == 8: temp = 0

            if (self.board[0][i] == 1 and self.board[1][i] == 1 and self.board[2][i] == 1):
                if ((self.board[0][i - 1] == 0 or self.board[0][temp] == 0) and (self.board[0][i - 1] != 2 and self.board[0][temp] != 2)):
                    white_result += 1
                if ((self.board[1][i - 1] == 0 or self.board[1][temp] == 0) and (self.board[1][i - 1] != 2 and self.board[1][temp] != 2)):
                    white_result += 1
                if ((self.board[2][i - 1] == 0 or self.board[2][temp] == 0) and (self.board[2][i - 1] != 2 and self.board[2][temp] != 2)):
                    white_result += 1
            elif (self.board[0][i] == 2 and self.board[1][i] == 2 and self.board[2][i] == 2):
                if ((self.board[0][i - 1] == 0 or self.board[0][temp] == 0) and (self.board[0][i - 1] != 1 and self.board[0][temp] != 1)):
                    black_result += 1
                if ((self.board[1][i - 1] == 0 or self.board[1][temp] == 0) and (self.board[1][i - 1] != 1 and self.board[1][temp] != 1)):
                    black_result += 1
                if ((self.board[2][i - 1] == 0 or self.board[2][temp] == 0) and (self.board[2][i - 1] != 1 and self.board[2][temp] != 1)):
                    black_result += 1

        if (player == 1): return white_result - black_result
        else: return black_result - white_result

    def numIntersectionsHeld(self, player):
        num = 0
        for i in range(0,3):
            if self.board[i][1] == player: num = num + 1
            if self.board[i][3] == player: num = num + 1
            if self.board[i][5] == player: num = num + 1
            if self.board[i][7] == player: num = num + 1
        return num
    
    def numDoubleMills(self, player):
        num = 0
        #check for first level
        if(self.board[0][0] == player and self.board[0][1] == player and self.board[0][2] == player):
            if(self.board[0][7] == 0 and self.isMill((0,0), (0,7), player)): num = num + 1
            if(self.board[1][1] == 0 and self.isMill((0,1), (1,1), player)): num = num + 1
            if(self.board[0][3] == 0 and self.isMill((0,2), (0,3), player)): num = num + 1
        if(self.board[0][2] == player and self.board[0][3] == player and self.board[0][4] == player):
            if(self.board[0][1] == 0 and self.isMill((0,2), (0,1), player)): num = num + 1
            if(self.board[1][3] == 0 and self.isMill((0,3), (1,3), player)): num = num + 1
            if(self.board[0][5] == 0 and self.isMill((0,4), (0,5), player)): num = num + 1
        if(self.board[0][4] == player and self.board[0][5] == player and self.board[0][6] == player):
            if(self.board[0][3] == 0 and self.isMill((0,4), (0,3), player)): num = num + 1
            if(self.board[1][5] == 0 and self.isMill((0,5), (1,5), player)): num = num + 1
            if(self.board[0][7] == 0 and self.isMill((0,6), (0,7), player)): num = num + 1
        if(self.board[0][6] == player and self.board[0][7] == player and self.board[0][0] == player):
            if(self.board[0][5] == 0 and self.isMill((0,6), (0,5), player)): num = num + 1
            if(self.board[1][7] == 0 and self.isMill((0,7), (1,7), player)): num = num + 1
            if(self.board[0][1] == 0 and self.isMill((0,0), (0,1), player)): num = num + 1
        #Second layer
        if(self.board[1][0] == player and self.board[1][1] == player and self.board[1][2] == player):
            if(self.board[1][7] == 0 and self.isMill((1,0), (1,7), player)): num = num + 1
            if(self.board[2][1] == 0 and self.isMill((1,1), (2,1), player)): num = num + 1
            if(self.board[0][1] == 0 and self.isMill((1,1), (0,1), player)): num = num + 1
            if(self.board[1][3] == 0 and self.isMill((1,2), (1,3), player)): num = num + 1
        if(self.board[1][2] == player and self.board[1][3] == player and self.board[1][4] == player):
            if(self.board[1][1] == 0 and self.isMill((1,2), (1,1), player)): num = num + 1
            if(self.board[2][3] == 0 and self.isMill((1,3), (2,3), player)): num = num + 1
            if(self.board[0][3] == 0 and self.isMill((1,3), (0,3), player)): num = num + 1
            if(self.board[1][5] == 0 and self.isMill((1,4), (1,5), player)): num = num + 1
        if(self.board[1][4] == player and self.board[1][5] == player and self.board[1][6] == player):
            if(self.board[1][3] == 0 and self.isMill((1,4), (1,3), player)): num = num + 1
            if(self.board[2][5] == 0 and self.isMill((1,5), (2,5), player)): num = num + 1
            if(self.board[0][5] == 0 and self.isMill((1,5), (0,5), player)): num = num + 1
            if(self.board[1][7] == 0 and self.isMill((1,6), (1,7), player)): num = num + 1
        if(self.board[1][6] == player and self.board[1][7] == player and self.board[1][0] == player):
            if(self.board[1][5] == 0 and self.isMill((1,6), (1,5), player)): num = num + 1
            if(self.board[2][7] == 0 and self.isMill((1,7), (2,7), player)): num = num + 1
            if(self.board[0][7] == 0 and self.isMill((1,7), (0,7), player)): num = num + 1
            if(self.board[1][1] == 0 and self.isMill((1,0), (1,1), player)): num = num + 1
        #Third level
        if(self.board[2][0] == player and self.board[2][1] == player and self.board[2][2] == player):
            if(self.board[2][7] == 0 and self.isMill((2,0), (2,7), player)): num = num + 1
            if(self.board[1][1] == 0 and self.isMill((2,1), (1,1), player)): num = num + 1
            if(self.board[2][3] == 0 and self.isMill((2,2), (2,3), player)): num = num + 1
        if(self.board[2][2] == player and self.board[2][3] == player and self.board[2][4] == player):
            if(self.board[2][1] == 0 and self.isMill((2,2), (2,1), player)): num = num + 1
            if(self.board[1][3] == 0 and self.isMill((2,3), (1,3), player)): num = num + 1
            if(self.board[2][5] == 0 and self.isMill((2,4), (2,5), player)): num = num + 1
        if(self.board[2][4] == player and self.board[2][5] == player and self.board[2][6] == player):
            if(self.board[2][3] == 0 and self.isMill((2,4), (2,3), player)): num = num + 1
            if(self.board[1][5] == 0 and self.isMill((2,5), (1,5), player)): num = num + 1
            if(self.board[2][7] == 0 and self.isMill((2,6), (2,7), player)): num = num + 1
        if(self.board[2][6] == player and self.board[2][7] == player and self.board[2][0] == player):
            if(self.board[2][5] == 0 and self.isMill((2,6), (2,5), player)): num = num + 1
            if(self.board[1][7] == 0 and self.isMill((2,7), (1,7), player)): num = num + 1
            if(self.board[2][1] == 0 and self.isMill((2,0), (2,1), player)): num = num + 1
        #Check for 4 lines going in to center
        if(self.board[0][1] == player and self.board[1][1] == player and self.board[2][1] == player):
            if(self.board[0][0] == 0 and self.isMill((0,1), (0,0), player)): num = num + 1
            if(self.board[0][2] == 0 and self.isMill((0,1), (0,2), player)): num = num + 1
            if(self.board[1][0] == 0 and self.isMill((1,1), (1,0), player)): num = num + 1
            if(self.board[1][2] == 0 and self.isMill((1,1), (1,2), player)): num = num + 1
            if(self.board[2][0] == 0 and self.isMill((2,1), (2,0), player)): num = num + 1
            if(self.board[2][2] == 0 and self.isMill((2,1), (2,2), player)): num = num + 1
        if(self.board[0][3] == player and self.board[1][3] == player and self.board[2][3] == player):
            if(self.board[0][2] == 0 and self.isMill((0,3), (0,2), player)): num = num + 1
            if(self.board[0][4] == 0 and self.isMill((0,3), (0,4), player)): num = num + 1
            if(self.board[1][2] == 0 and self.isMill((1,3), (1,2), player)): num = num + 1
            if(self.board[1][4] == 0 and self.isMill((1,3), (1,4), player)): num = num + 1
            if(self.board[2][2] == 0 and self.isMill((2,3), (2,2), player)): num = num + 1
            if(self.board[2][4] == 0 and self.isMill((2,3), (2,4), player)): num = num + 1
        if(self.board[0][5] == player and self.board[1][5] == player and self.board[2][5] == player):
            if(self.board[0][4] == 0 and self.isMill((0,5), (0,4), player)): num = num + 1
            if(self.board[0][6] == 0 and self.isMill((0,5), (0,6), player)): num = num + 1
            if(self.board[1][4] == 0 and self.isMill((1,5), (1,4), player)): num = num + 1
            if(self.board[1][6] == 0 and self.isMill((1,5), (1,6), player)): num = num + 1
            if(self.board[2][4] == 0 and self.isMill((2,5), (2,4), player)): num = num + 1
            if(self.board[2][6] == 0 and self.isMill((2,5), (2,6), player)): num = num + 1
        if(self.board[0][7] == player and self.board[1][7] == player and self.board[2][7] == player):
            if(self.board[0][6] == 0 and self.isMill((0,7), (0,6), player)): num = num + 1
            if(self.board[0][0] == 0 and self.isMill((0,7), (0,0), player)): num = num + 1
            if(self.board[1][6] == 0 and self.isMill((1,7), (1,6), player)): num = num + 1
            if(self.board[1][0] == 0 and self.isMill((1,7), (1,0), player)): num = num + 1
            if(self.board[2][6] == 0 and self.isMill((2,7), (2,6), player)): num = num + 1
            if(self.board[2][0] == 0 and self.isMill((2,7), (2,0), player)): num = num + 1
        return num


    def numPiecesDifferent (self, player):
        if(player == 1): return self.white_pieces_on_board - self.black_pieces_on_board
        else: return self.black_pieces_on_board - self.white_pieces_on_board
    
    def num3PieceConfigs (self, player):
        num = 0
        for i in range(0, 8, 2):
            #First Layer
            if self.board[0][i] == player:
                if self.board[0][i+1] == player and self.board[1][i+1] == player: num = num + 1
                if self.board[0][(i+7)%8] == player and self.board[1][(i+7)%8] == player: num = num + 1
                if self.board[0][i+1] == player and self.board[0][(i+7)%8] == player: num = num + 1
            #Second Layer
            if self.board[1][i] == player:
                if self.board[1][i+1] == player and self.board[2][i+1] == player: num = num + 1
                if self.board[1][(i+7)%8] == player and self.board[2][(i+7)%8] == player: num = num + 1
                if self.board[1][i+1] == player and self.board[0][i+1] == player: num = num + 1
                if self.board[1][(i+7)%8] == player and self.board[0][(i+7)%8] == player: num = num + 1
                if self.board[1][i+1] == player and self.board[1][(i+7)%8] == player: num = num + 1
            #Third Layer
            if self.board[2][i] == player:
                if self.board[2][i+1] == player and self.board[1][i+1] == player: num = num + 1
                if self.board[2][(i+7)%8] == player and self.board[1][(i+7)%8] == player: num = num + 1
                if self.board[2][i+1] == player and self.board[2][(i+7)%8] == player: num = num + 1
        return num
    
    def num2PieceConfigs(self, player):
        # For each layer, find the 2 piece configs and sum
        return sum([sum([(layer[i] == player and
                         layer[(i+1)%len(layer)] == player)
                         for i in range(len(layer))])
                   for layer in self.board])
    
    
    # The number of open mills for the player (number of two piece configurations with an opening for mill)
    def numOpenMills(self, player):
        num = 0
        # Check layers of board
        for i in range(3):
            for j in range(0, 7, 2): # 0, 2, 4, 6
                if (self.board[i][j] == player and self.board[i][(j + 1) % 8] == player and self.board[i][(j + 2) % 8] == 0):
                    num += 1
                elif (self.board[i][j] == 0 and self.board[i][(j + 1) % 8] == player and self.board[i][(j + 2) % 8] == player):
                    num += 1

        # Check inward lines: 1, 3, 5, 7
        for i in range(1, 8, 2):
            if (self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == 0):
                num += 1
            elif (self.board[0][i] == 0 and self.board[1][i] == player and self.board[2][i] == player):
                num += 1
        
        return num
    

    # The number of double mills which share a common piece
    def numDoubleSharedMill(self, player):
        num = 0
        # Check double mills which share a corner piece
        for i in range(3):
            if (self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player
                and self.board[i][7] == player and self.board[i][6] == player): num += 1
            if (self.board[i][2] == player and self.board[i][0] == player and self.board[i][1] == player
                and self.board[i][3] == player and self.board[i][4] == player): num += 1
            if (self.board[i][4] == player and self.board[i][2] == player and self.board[i][3] == player
                and self.board[i][5] == player and self.board[i][6] == player): num += 1
            if (self.board[i][6] == player and self.board[i][0] == player and self.board[i][7] == player
                and self.board[i][4] == player and self.board[i][5] == player): num += 1
        # Check double mills which share a non corner piece
        for i in range(1, 8, 2): # 1,3,5,7
            if (self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player):
                for j in range(3):
                    if (self.board[j][i-1] == player and self.board[j][(i+1)%8] == player): num += 1
        return num
    
    
    def numNonOppositeCorners(self, player):
        # For each layer, find the non opp corners and sum 
        return sum([sum([(layer[i] == player and
                          layer[(i+2)%len(layer)] == player)
                         for i in range(0, len(layer), 2)])
                   for layer in self.board])

    
    # Evaluates a NMM board state as a value. Uses our heurstic.
    # player = the player whos phase we are basing the board state on
    # player_to_max = the player who is MAX
    def eval(self, player, player_to_max):
        win_result = 1_000_000_000
        
        if (player_to_max == 1): player_to_min = 2
        else: player_to_min = 1

        # If player = 1, evaluate the board state from the phase of player 1
        if (player == 1):
            if (self.white_phase == 1):
                # result = 4a + 7c + 7g + 2i
                a = self.millDifference(player_to_max)
                c = self.numOpenMills(player_to_max) - self.numOpenMills(player_to_min)
                g = self.numIntersectionsHeld(player_to_max) - self.numIntersectionsHeld(player_to_min)
                i = self.minSlidesToMill(player_to_max) - self.minSlidesToMill(player_to_min)
                result = 4*a + 7*c + 7*g + 2*i
            elif (self.white_phase == 2):
                if (self.isWin(player_to_max)): result = win_result
                elif (self.isWin(player_to_min)): result = -win_result
                else:
                    # result = 3a + 1.5c + 2.5d + 2.5e + 2f + 2g + 4h + 2.5i
                    a = self.millDifference(player_to_max)
                    c = self.numOpenMills(player_to_max) - self.numOpenMills(player_to_min)
                    d = self.numPiecesDifferent(player_to_max)
                    e = self.blockedInDifference(player_to_max)
                    f = self.spammableMillPiecesDifference(player_to_max)
                    g = self.numIntersectionsHeld(player_to_max) - self.numIntersectionsHeld(player_to_min)
                    h = self.numDoubleMills(player_to_max) - self.numDoubleMills(player_to_min)
                    i = self.minSlidesToMill(player_to_max) - self.minSlidesToMill(player_to_min)
                    result = 3*a + 1.5*c + 2.5*d + 2.5*e + 2*f + 2*g + 4*h + 2.5*i
            elif (self.white_phase == 3):
                if (self.isWin(player_to_max)): result = win_result
                elif (self.isWin(player_to_min)): result = -win_result
                else:
                    # result = 3c + 10d + 5j + 2k
                    c = self.numOpenMills(player_to_max) - self.numOpenMills(player_to_min)
                    d = self.numPiecesDifferent(player_to_max)
                    j = self.num3PieceConfigs(player_to_max) - self.num3PieceConfigs(player_to_min)
                    k = self.numNonOppositeCorners(player_to_max)
                    result = 3*c + 10*d + 5*j + 2*k
        # If player = 2, evaluate the board state from the phase of player 2
        elif (player == 2):
            if (self.black_phase == 1):
                # result = 4a + 7c + 7g + 2i
                a = self.millDifference(player_to_max)
                c = self.numOpenMills(player_to_max) - self.numOpenMills(player_to_min)
                g = self.numIntersectionsHeld(player_to_max) - self.numIntersectionsHeld(player_to_min)
                i = self.minSlidesToMill(player_to_max) - self.minSlidesToMill(player_to_min)
                result = 4*a + 7*c + 7*g + 2*i
            elif (self.black_phase == 2):
                if (self.isWin(player_to_max)): result = win_result
                elif (self.isWin(player_to_min)): result = -win_result
                else:
                    # result = 3a + 1.5c + 2.5d + 2.5e + 2f + 2g + 4h + 2.5i
                    a = self.millDifference(player_to_max)
                    c = self.numOpenMills(player_to_max) - self.numOpenMills(player_to_min)
                    d = self.numPiecesDifferent(player_to_max)
                    e = self.blockedInDifference(player_to_max)
                    f = self.spammableMillPiecesDifference(player_to_max)
                    g = self.numIntersectionsHeld(player_to_max) - self.numIntersectionsHeld(player_to_min)
                    h = self.numDoubleMills(player_to_max) - self.numDoubleMills(player_to_min)
                    i = self.minSlidesToMill(player_to_max) - self.minSlidesToMill(player_to_min)
                    result = 3*a + 1.5*c + 2.5*d + 2.5*e + 2*f + 2*g + 4*h + 2.5*i
            elif (self.black_phase == 3):
                if (self.isWin(player_to_max)): result = win_result
                elif (self.isWin(player_to_min)): result = -win_result
                else:
                    # result = 3c + 10d + 5j + 2k
                    c = self.numOpenMills(player_to_max) - self.numOpenMills(player_to_min)
                    d = self.numPiecesDifferent(player_to_max)
                    j = self.num3PieceConfigs(player_to_max) - self.num3PieceConfigs(player_to_min)
                    k = self.numNonOppositeCorners(player_to_max)
                    result = 3*c + 10*d + 5*j + 2*k

        return result


    def evalOnlineAlgo(self, player, player_to_max):

        win_result = 1_000_000_000
        
        if (player_to_max == 1): player_to_min = 2
        else: player_to_min = 1
        if (self.isWin(player_to_max)): result = win_result
        elif (self.isWin(player_to_min)): result = -win_result
        else:
            a = self.numPiecesDifferent(player_to_max)
            b = len(self.getValidMoves(player_to_max)) - len(self.getValidMoves(player_to_min))
            c = self.millDifference(player_to_max)
            result = 3 * a + 1 * c + .1 * b
        return result

    def closedMill(self, player, old_white_pieces, old_black_pieces):
        if (self.white_pieces_on_board < old_white_pieces):
            toReturn = 1
        elif(self.black_pieces_on_board < old_black_pieces):
            toReturn = -1
        else:
            toReturn = 0;

        if (player == 1):
            toReturn *= -1

        return toReturn
