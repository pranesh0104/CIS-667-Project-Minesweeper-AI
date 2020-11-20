# Importing required Libraries
import numpy as np # data structure for game state representation
import random # Package to introduce randomness
import time # Used to keep track of the duration taken to solve Minesweeper

class Alpha_Sweeper(object):
    
    def __init__(self,i,j=None):
        if j is None:
            self.ms_grid = i 
        else:
            self.frame = np.zeros((i,j))
            total = j-np.random.randint(1,j-2)
            rand_rows = np.random.randint(0, i, total)
            rand_cols = np.random.randint(0, j, total)
            # For generating mines in the grid
            for i in range(total):
                self.frame[rand_rows[i], rand_cols[i]] = -99
            root_frame = self.fill_matrix()
            
    def __str__(self):
        return "\n".join(["".join(str(row)) for row in self.ms_grid])
    def is_leaf(self):
        if self.player_score() != 0: return True
        return ((self.ms_grid == -1).sum() == 0)
    def player_score(self):
        # Player Score -> [win,lose,noResult] : [+1,-1,0]
        # Lose Condition
        if np.any(self.ms_grid == -99): return -1
        # Win Condition
        if np.all(self.ms_grid != -1)  : return 1
        return 0 
    def valid_actions(self):
        valid_actions = np.asarray(np.where(self.ms_grid == -1)).T.tolist()
        return valid_actions
    def perform_action(self,alpha_ms,m,n,action):
        temp_grid = np.empty(alpha_ms.shape)
        np.copyto(temp_grid,self.ms_grid)
        new_state = Alpha_Sweeper(temp_grid)
        
        if action == 0:
            if alpha_ms[m,n] > 0:
                new_state.ms_grid = new_state.chance(m,n,alpha_ms)
            elif (alpha_ms[m,n] < 0):
                new_state.ms_grid[m,n] = alpha_ms[m,n]
            if alpha_ms[m,n] == 0:
                new_state = self.reveal(alpha_ms, m,n,new_state,check=[])
            return new_state,m,n
        
        if action == 1:
            new_state = Alpha_Sweeper(temp_grid)
            new_state.ms_grid[m,n] = -2
            return new_state,m,n              
        
    def fill_matrix(self):
        for i in range(self.frame.shape[0]):
            for j in range(self.frame.shape[1]):
                if (self.frame[i,j] < 0):
                    if (i == 0 and j == 0):
                        self.frame[i:i+2, j:j+2] +=1
                    elif (i == 0):
                        self.frame[i:i+2, j-1:j+2] +=1
                    elif (j == 0):
                        self.frame[i-1:i+2, j:j+2] +=1
                    else: 
                        self.frame[i-1:i+2, j-1:j+2] +=1
        self.frame[self.frame<0] = -99
        return self.frame

    # To reveal all adjecent safe cells when a safe cell is selected
    def reveal(self,alpha_ms, i,j,new_state,check):
        if (i<0 or i>=alpha_ms.shape[0] or j<0 or j>=alpha_ms.shape[1]):
            return
        if str(i)+str(j) in check:
            return
        if (alpha_ms[i,j] == -99 or new_state.ms_grid[i,j] == -2):
            return
        if (alpha_ms[i,j] not in (0, -99)):
            new_state.ms_grid = new_state.chance(i,j,alpha_ms)
            check.append(str(i)+str(j))
            return
        else:
            new_state.ms_grid[i,j]=0
            check.append(str(i)+str(j))
            for k in range (i-1, i+2):
                for l in range (j-1, j+2):
                    self.reveal(alpha_ms,k,l,new_state,check)    
        return new_state
    # To implement the rule modification
    def chance(self,m,n,alpha_ms):
        chnc = random.randint(0,100)
         #if chnc in random.sample(range(0,100), 5):
        if chnc in (1,2,3,4,5):
            self.ms_grid[m,n] = random.randint(0,9)
        else:
            self.ms_grid[m,n] = alpha_ms[m,n]
        return self.ms_grid
def initial_state(i,j):
    alpha_ms = Alpha_Sweeper(i,j)
    ms_grid = np.ones((i,j))
    ms_grid = ms_grid*(-1)
    return alpha_ms.frame,Alpha_Sweeper(ms_grid)
    
