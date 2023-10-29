# |---------------------------------------
# |                                      |
# |     This is a Agent creator class    |
# |                                      |
# |   This class is used with the Board  |
# |     to create a working learning     |
# |                                      |
# ----------------------------------------

import sys
sys.path.append("./grid_world")
import numpy as np
from grid_world_board import Board

class Agent:

    def __init__(self, board: Board):
        self.trajectory = []
        self.actions = [0, 1, 2, 3]
        self.lr = 0.1
        self.exp_rate = 0.3
        self.board = board
        self.position = board.start_position
        self.determenistic = True 
        self.gamma_decay = 0.4
        self.initialize_Q_values()

    def initialize_state_values(self):
        self.state_values = {}
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                self.state_values[(i,j)] = 0
    
    def initialize_Q_values(self):
        self.Q_values = {}
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                self.Q_values[(i, j)] = {}
                for a in self.actions:
                    self.Q_values[(i, j)][a] = 0 
                
    def give_reward(self):
        match self.position:
            case self.board.win_state:
                return 1
            case self.board.lose_state:
                return -1
            case _:
                return 0

    def inside_grid(self, position: tuple[int, int]):
        if (position[0] >= 0) and (position[0] < (self.board.rows)) and (position[1] >= 0) and (position[1] <= (self.board.cols -1)):
            return True
        return False

    def check_valid_position(self, position: tuple[int, int]):
        if self.inside_grid(position) and position not in self.board.walls:
            return position
                
    def next_position(self, action):
        """
        action: up-0, down-1, left-2, right-3
        -------------
        0 | 1 | 2| 3|
        1 |
        2 |
        return next position
        """
        if not self.determenistic:
            same_action_prob = 0.75
            other_action_prob = (1 - same_action_prob) / (len(self.actions) - 1)
            probs = [same_action_prob if a == action else other_action_prob for a in self.actions]
            action = np.random.choice(self.actions, p = probs)
            
        match action:
            case 0:
                next_position = (self.position[0] - 1, self.position[1])
            case 1:
                next_position = (self.position[0] + 1, self.position[1])
            case 2:
                next_position = (self.position[0], self.position[1] - 1)
            case 3:
                next_position = (self.position[0], self.position[1] + 1)
            case _:
                print("action is illegal")
        
        # check if the move is legal
        if self.check_valid_position(next_position):
            return next_position
        
        #else don't move
        return self.position
    
    def value_action(self, action):
        return self.state_values[self.next_position(action)]
    
    def value_Q_action(self, action):
        return self.Q_values[self.position][action]
        
    def choose_action(self):
        # choose action with most expected value
        action = np.random.choice(self.actions)

        if np.random.uniform(0, 1) < self.exp_rate:
            action = max(self.actions, key = self.value_action)
        
        return action
    
    def choose_Q_action(self):
        # choose action with most expected value
        action = np.random.choice(self.actions)

        if np.random.uniform(0, 1) < self.exp_rate:
            action = max(self.actions, key = self.value_Q_action)
        
        return action
      
                
            

    def take_action(self, action):
        self.position = self.next_position(action)
        self.trajectory.append(self.next_position(action))
        
    def take_Q_action(self, action):
        self.position = self.next_position(action)
        self.trajectory.append((self.next_position(action), action))


    def reset(self):    
        self.trajectory = []
        self.position = self.board.start_position
        self.state_values[(self.board.win_state)] = 1
        self.state_values[(self.board.lose_state)] = -1
        for a in self.actions:
            self.Q_values[self.board.win_state][a] = 1
            self.state_values[(self.board.lose_state)] = -1
    
    def reset_Q(self):
        self.trajectory = []
        self.position = self.board.start_position
        for a in self.actions:
            self.Q_values[self.board.win_state][a] = 1
            self.Q_values[self.board.lose_state][a] = -1
    
    def play(self, rounds=10):
        i = 0
        while i < rounds:
            action = self.choose_action()
            # append trace
            self.take_action(action)
            # by taking the action, it reaches the next state
            
            reward = self.give_reward()
            if reward != 0:

                # explicitly assign end state to reward values
                self.state_values[(self.position)] = reward
                for s in reversed(self.trajectory):
                    self.state_values[s] = round(self.state_values[s] + self.lr * (reward - self.state_values[s]), 3)
                self.reset()
                i+= 1
                
    def play_Q(self, rounds=10):
        i = 0
        while i < rounds:
            action = self.choose_Q_action()
            # append trace
            self.take_Q_action(action)
            # by taking the action, it reaches the next state
            
            reward = self.give_reward()
            if reward != 0:

                # explicitly assign end state to reward values
                for s in reversed(self.trajectory):
                    self.Q_values[s[0]][s[1]] = round((1 - self.lr) * (self.Q_values[s[0]][s[1]]) + self.lr * (reward + self.gamma_decay * self.Q_values[s[0]][max(self.actions, key = self.value_Q_action)]), 2)
                    # self.Q_values[s[0]][s[1]] = round(self.Q_values[s[0]][s[1]] + self.lr * (self.gamma_decay * reward - self.Q_values[s[0]][s[1]]), 2)

                self.reset_Q()
                i+= 1


    def showQValues(self):
        for i in range(0, self.board.rows):
            print('------------------------------' * 5)
            out = '| '
            for j in range(0, self.board.cols):
                out += str(self.Q_values[(i, j)]).ljust(34) + ' | '
            print(out)
        print('-----------------------------' * 5)
        
    def showValues(self):
        for i in range(0, self.board.rows):
            print('----------------------------------')
            out = '| '
            for j in range(0, self.board.cols):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')

#TODO create test function that I cant see the bot plays on the board

board = Board(3, 4)
agent = Agent(board)

agent.play_Q(5000)
agent.showQValues()
