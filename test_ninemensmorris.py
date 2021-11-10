import ninemensmorris as nmm

# Making sure we detect wins due to lack of moves correctly 
def test_no_move_win():
    state = nmm.NineMensMorris();
    state.board[0][0] = 1;
    state.board[0][1] = 1;
    state.board[0][2] = 1;
    state.board[0][7] = 2;
    state.board[1][1] = 2;
    state.board[0][3] = 2;
    state.white_pieces_on_board = 3;
    state.black_pieces_on_board = 3;
    state.white_pieces_avail = 0;
    state.black_pieces_avail = 0;
    state.white_phase = 3;
    state.black_phase = 3;
    assert(len(state.getValidMoves(1)) == 3 * 18); # Both player have moves and no one has won
    assert(len(state.getValidMoves(2)) == 3 * 18);
    assert(not state.isWin(1));
    assert(not state.isWin(2));

    state.board[0][6] = 1;
    state.board[0][5] = 2;
    state.white_phase = 2;
    state.black_phase = 2;
    state.white_pieces_on_board = 4;
    state.black_pieces_on_board = 5;
    assert(len(state.getValidMoves(1)) == 0); # Player 1 can't move, so player 2 has won
    assert(len(state.getValidMoves(2)) == 8);
    assert(not state.isWin(1));
    assert(state.isWin(2));


# Testing that variables are updated properly
def test_variable_update():
    state = nmm.NineMensMorris();
    state = state.move(None, (2, 7), None, 1);
    assert(state.white_pieces_avail == 8);
    assert(state.white_pieces_on_board == 1);
    assert(state.white_phase == 1);
    expandedStates = state.getValidMoves(2);
    assert(len(expandedStates) == 23);
    for newState in expandedStates:
        assert(newState.white_pieces_avail == 8)
        assert(newState.black_pieces_avail == 8)
        assert(newState.white_phase == 1)
        assert(newState.black_phase == 1)
        assert(newState.white_pieces_on_board == 1)
        assert(newState.black_pieces_on_board == 1)

# Testing that the correct value is returned
def test_minSlidesToMill():
    state = nmm.NineMensMorris();
    state.board[0][0] = 1
    state.board[0][7] = 1
    state.board[0][2] = 1
    assert(state.minSlidesToMill(1) == 4)
    state.board[0][4] = 2
    assert(state.minSlidesToMill(1) == 4)
    state.board[1][0] = 2
    assert(state.minSlidesToMill(1) == 6)
    state.board[1][6] = 2;
    assert(state.minSlidesToMill(2) == 6)
    assert(state.minSlidesToMill(1) == 6)
