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
            self.t_flags = np.count_nonzero(self.frame == -99 )
            
            
    def __str__(self):
        return "\n".join(["".join(str(row)) for row in self.ms_grid])
    def is_leaf(self,alpha_ms):
        if np.any(self.ms_grid == -99): return True
        # Win Condition
        if np.all(self.ms_grid != -1):
            bomb_locations = np.asarray(np.where(alpha_ms == -99)).T.tolist()
            for [r,c] in bomb_locations:
                if self.ms_grid[r,c] != -2: return False
            return True
        return False    

            
    def player_score(self,alpha_ms):
        # Player Score -> [win,lose,noResult] : [+1,-1,0]
        # Lose Condition
        score = (alpha_ms.shape[0]*alpha_ms.shape[1])-np.count_nonzero(alpha_ms == -99)
        if np.any(self.ms_grid == -99): return -1
        # Win Condition
        if np.all(self.ms_grid != -1):
            bomb_locations = np.asarray(np.where(alpha_ms == -99)).T.tolist()
            for [r,c] in bomb_locations:
                if self.ms_grid[r,c] != -2: return 0
            return 1
        return 0    
    def valid_actions(self):
        
        valid_actions = np.asarray(np.where((self.ms_grid == -1) | (self.ms_grid == -2))).T.tolist()
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
            return new_state
        
        if action == 1:
            if temp_grid[m,n] != -2:                
                new_state.ms_grid[m,n] = -2
                return new_state
        return None
        
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

    def reveal_text(self,i,j,output_frame,check):
        if (i<0 or i>=self.frame.shape[0] or j<0 or j>=self.frame.shape[1]):
            return
        if str(i)+str(j) in check:
            return
        if (self.frame[i,j] == -99 or output_frame[i,j] == '>'):
            return
        if (self.frame[i,j] not in (0, -99)):
            output_frame = self.chanceText(i,j,output_frame)
            check.append(str(i)+str(j))
            return
        else:
            output_frame[i,j]='S'
            check.append(str(i)+str(j))
            for k in range (i-1, i+2):
                for l in range (j-1, j+2):
                    self.reveal_text(k,l,output_frame,check)    
    
    # To implement the rule modification
    def chance(self,m,n,alpha_ms):
        chnc = random.randint(0,100)
         #if chnc in random.sample(range(0,100), 5):
        if chnc in (1,2,3,4,5):
            self.ms_grid[m,n] = random.randint(0,9)
        else:
            self.ms_grid[m,n] = alpha_ms[m,n]
        return self.ms_grid

    def chanceText(self,m,n,output_frame):
        chnc = random.randint(0,100)
         #if chnc in random.sample(range(0,100), 5):
        if chnc in (1,2,3,4,5):
            output_frame[m,n] = random.randint(0,9)
        else:
            output_frame[m,n] = self.frame[m,n]
        return output_frame


    def begin_text_game(self):
        start_time = time.time()
        output_frame = np.empty(self.frame.shape, dtype='str')
        output_frame[:] = '_'
        tbombs = np.count_nonzero(self.frame < 0 )
        flags = tbombs
        while True:
            try:
                if ((np.count_nonzero(output_frame != '_')) == (output_frame.shape[0]*output_frame.shape[1]) and (flags == 0) ):
                    end_time = time.time()
                    print('Congrats! You have won the game')
                    print('\n Game Score -> %0.2f'%(end_time-start_time))
                    break
                i, j = map(int, input('Input row and column(i,j) or -1,-1 to exit').split(','))
                if (i==-1 and j==-1):
                    print("Play again later!")
                    break
                op = int(input('Select operation\n 1. Reveal\n 2. Flag'))
                if ((i < 0 or i >= self.frame.shape[0])  or (j < 0 or j >= self.frame.shape[1]) or op not in (1, 2)):
                    print("Invalid response. Please try again")
                    continue
                if (op == 1):
                    if (output_frame[i,j] == '>'):
                        flags += 1
                    if (output_frame[i,j] not in ('_', '>')):
                        print ("Cell is already revealed. Please choose another cell")
                        continue
                    if (self.frame[i,j] > 0):
                        output_frame = self.chanceText(i,j,output_frame)
                    elif (self.frame[i,j] < 0):
                        print ("Oops! You stepped on a MINE ('_') . Better luck next time!\n ")
                        break
                    if (self.frame[i,j] == 0):
                        self.reveal_text(i,j,output_frame, check = [])
                
                if (op == 2):
                    if(output_frame[i,j] == '>'):
                        output_frame[i,j] = '_'
                        flags += 1
                        print("Total flags left = ", flags)
                        print ("Total bombs in the grid = ", tbombs)   
                        print(output_frame)
                        continue
                    if(flags == 0):
                        print("Cannot assign more flags. Please try again.")
                        continue                
                    if (output_frame[i,j] not in ('_', '>')):
                        print ("Cannot flag revealed cell. Please choose another cell")
                        continue
                        
                    output_frame[i,j] = '>'
                    flags -= 1
                    print("Total flags left = ", flags)

                print ("Total bombs in the grid = ", tbombs)   
                print(output_frame)
            except KeyboardInterrupt:
                break
            except:
                print('Invalid response')
                continue


def textBasedGame():
    print('Lets play Minesweeper!\n')
    f = 0
    while True:
        try:
            if f!=0:
                print ('Wanna try again?\n')
            f=1
            print ('Select grid size:\n')
            ch = int(input(' 1. 4x4 \n 2. 5x5 \n 3. 6x6 \n 4. 7x7 \n 5. 8x8 6.exit\n'))
            if (ch == 1):
                alpha_ms = Alpha_Sweeper(4,4)
                alpha_ms.begin_text_game()
            elif (ch == 2):        
                alpha_ms = Alpha_Sweeper(5,5)
                alpha_ms.begin_text_game()
            elif (ch == 3):
                alpha_ms = Alpha_Sweeper(6,6)
                alpha_ms.begin_text_game()
            elif (ch == 4):
                alpha_ms = Alpha_Sweeper(7,7)
                alpha_ms.begin_text_game()
            elif (ch == 5):
                alpha_ms = Alpha_Sweeper(8,8)
                alpha_ms.begin_text_game()
            elif (ch == 6):
                print("Lets play some other time")
                return 
            else:
                print('Invalid response. Please try again')
                continue


        except KeyboardInterrupt:
            print("\nLets play some other time")
            return
        except:
            print('Invalid response. Please try again')
            f=0
            continue



def initial_state(i,j):
    alpha_ms = Alpha_Sweeper(i,j)
    initial_grid = np.ones((i,j))
    initial_grid = initial_grid*(-1) # -1 denotes empty position
    return alpha_ms.frame,Alpha_Sweeper(initial_grid)
    
