import numpy as np
from progressbar import ProgressBar
# global variables
BOARD_ROWS = 3
BOARD_COLS = 4
WIN_STATE = (0, 3)
LOSE_STATE = (1, 3)
START = (2, 0)
DETERMINISTIC = True
WALLS = [(1, 1)]

class State:
    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.board[1, 1] = -1
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC
        self.win_state = (0, 3)
        self.lose_state = (1, 3)

    def give_reward(self):
        match self.state:
            
            case self.win_state:
                return 1
            
            case self.lose_state:
                return -1
            
            case _:
                return 0
            

    def check_end(self):
        if (self.state == WIN_STATE) or (self.state == LOSE_STATE):
            return True
        else:
            return False

    def next_position(self, action):
        """
        action: up-0, down-1, left-2, right-3
        -------------
        0 | 1 | 2| 3|
        1 |
        2 |
        return next position
        """
        if self.determine:
            match action:
                case 0:
                    next_state = (self.state[0] - 1, self.state[1])
                case 1:
                    next_state = (self.state[0] + 1, self.state[1])
                case 2:
                    next_state = (self.state[0], self.state[1] - 1)
                case 3:
                    next_state = (self.state[0], self.state[1] + 1)
                case _:
                    print("action is illegal")
            
            # check if the move is legal
            if (next_state[0] >= 0) and (next_state[0] <= (BOARD_ROWS -1)):
                if (next_state[1] >= 0) and (next_state[1] <= (BOARD_COLS -1)):
                    if next_state not in WALLS:
                        return next_state
            
            #else don't move
            return self.state

    def showBoard(self):
        self.board[self.state] = 1
        for i in range(0, BOARD_ROWS):
            print('-----------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = '*'
                if self.board[i, j] == -1:
                    token = 'z'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
            print(out)
        print('-----------------')


# Agent of player

class Agent:

    def __init__(self):
        self.states = []
        self.actions = [0, 1, 2, 3]
        self.State = State()
        self.lr = 0.2
        self.exp_rate = 0.3

        # initial state reward
        self.state_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.state_values[(i,j)] = 0  # set initial value to 0

    def choose_action(self):
        # choose action with most expected value
        max_reward = 0
        action = np.random.choice(self.actions)

        if np.random.uniform(0, 1) < self.exp_rate:
            # greedy action
            for a in self.actions:
                # if the action is deterministic
                action_reward = self.state_values[self.State.next_position(a)]
                if action_reward > max_reward:
                    action = a
                    max_reward = action
        
        return action

    def take_action(self, action):
        position = self.State.next_position(action)
        return State(state=position)

    def reset(self):
        self.states = []
        self.State = State()

    def play(self, rounds=10):
        BAR = ProgressBar(min_value=0, max_value=rounds)
        for i in range(rounds):
            action = self.choose_action()
            # append trace
            self.states.append(self.State.next_position(action))
            # by taking the action, it reaches the next state
            self.State = self.take_action(action)

            if self.State.check_end():
            # back propagate
                reward = self.State.give_reward()
                # explicitly assign end state to reward values
                self.state_values[self.State.state] = reward  # this is optional
                for s in reversed(self.states):
                    self.state_values[s] = round(self.state_values[s] + self.lr * (reward - self.state_values[s]), 3)
                self.reset()
                
                BAR.update(i)


    def showValues(self):
        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')


if __name__ == "__main__":
    ag = Agent()
    ag.play(5000)
    ag.showValues()