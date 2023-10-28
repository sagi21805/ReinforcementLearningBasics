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
        self.determine = True #TODO learn what happens when changes.
        self.initialize_state_values()

    def initialize_state_values(self):
        self.state_values = {}
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                self.state_values[(i,j)] = 0
        
    

                
    def give_reward(self):
        match self.position:
            case self.board.win_state:
                return 1
            case self.board.lose_state:
                return -1
            case _:
                return 0

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
            if (next_position[0] >= 0) and (next_position[0] <= (self.board.rows -1)):
                if (next_position[1] >= 0) and (next_position[1] <= (self.board.cols -1)):
                    if next_position not in self.board.walls:
                        return next_position
            
            #else don't move
            return self.position
    
    def choose_action(self):
        # choose action with most expected value
        max_reward = 0
        action = np.random.choice(self.actions)

        if np.random.uniform(0, 1) < self.exp_rate:
            # greedy action
            for a in self.actions:
                # if the action is deterministic
                action_reward = self.state_values[self.next_position(a)]
                if action_reward > max_reward:
                    action = a
                    max_reward = action
        
        return action

    def take_action(self, action):
        self.position = self.next_position(action)
        self.trajectory.append(self.next_position(action))


    def reset(self):    
        self.trajectory = []
        self.position = self.board.start_position
        self.state_values[(self.board.win_state)] = 1
        self.state_values[(self.board.lose_state)] = -1
        
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
                for s in reversed(self.trajectory):
                    self.state_values[s] = round(self.state_values[s] + self.lr * (reward - self.state_values[s]), 3)
                self.reset()
                i+= 1


    def showValues(self):
        for i in range(0, self.board.rows):
            print('----------------------------------')
            out = '| '
            for j in range(0, self.board.cols):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')


board = Board(3, 4)
agent = Agent(board)

agent.play(5000)
agent.showValues()