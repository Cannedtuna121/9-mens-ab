class TTT:

    def __init__(self, state='.........', p1='x', p2='o'):
        self.state = state
        self.p1 = p1
        self.p2 = p2

        self.terminals = [(0, 1, 2), (0, 3, 6), (0, 4, 8), 
                          (1, 4, 7), (2, 4, 6), (2, 5, 8), 
                          (3, 4, 5), (6, 7, 8)]
        self.get_opp = lambda p: p1 if p==p2 else p2
    
    def getValidMoves(self, player = 'x'):
        new_states = []
        for i in range(len(self.state)):
            if self.state[i] == ".":
                new_states.append(TTT(
                    self.state[:i] + player + self.state[i+1:], 
                    self.p1, self.p2))
        return new_states

    def openWins(self, weights=[1,1,1,1,1,1,1,1]):
        player_set = set([self.p1])
        opp_set = set([self.p2])
        open_wins = 0
        for j, terminal in enumerate(self.terminals):
            elements = set([self.state[i] for i in terminal])
            if elements == player_set: return 100
            if elements == opp_set: return -100
            if self.p2 not in elements: open_wins += weights[j]
            elif self.p1 not in elements: open_wins -= weights[j]
        return open_wins
    
    def captured(self, weights=[1,1,1,1,1,1,1,1,1]):
        captured = 0
        for i, e in enumerate(self.state):
            if e == self.p1: captured += weights[i]
            elif e == self.p2: captured -= weights[i]
        return captured
    
    def eval(self, player=None, max_player=None, strategy='open_wins', weights=[]):
        if strategy == 'open_wins':
            return self.openWins()
        elif strategy == 'weighted_open_wins':
            return self.openWins(weights)
        elif strategy == 'captured':
            return self.captured()
        elif strategy == 'weighted_captured':
            return self.captured(weights)
        
    def is_terminal(self):
        return self.eval(self.state) in [100, -100] or '.' not in self.state
        
    def pretty_print(self, state):
        return state[:3] + '\n' + state[3:6] + '\n' + state[6:]