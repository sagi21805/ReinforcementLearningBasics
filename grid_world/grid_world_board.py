# |---------------------------------------
# |                                      |
# |     This is a Board creator class    |
# |                                      |
# |   This class is used with the Agent  |
# |     to create a working learning     |
# |                                      |
# ----------------------------------------


import numpy as np



class Board:
    
    def __init__(self, rows, cols, start_position = (2, 0), win_position = (0, 3), lose_position = (1, 3), walls = [(1, 1)]):
        
        self.rows = rows
        self.cols = cols
        
        self.walls = walls
        self.board = np.zeros([rows, cols])
        for wall in walls:
            self.board[wall] = -1
            
        self.start_position = start_position
        
        self.end = False
        
        self.determine = True
        
        self.win_state = win_position
        self.lose_state = lose_position


        
