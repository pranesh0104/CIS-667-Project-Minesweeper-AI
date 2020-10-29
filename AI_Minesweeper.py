# Importing required Libraries
import numpy as np # data structure for game state representation
import random # Package to introduce randomness
import time # Used to keep track of the duration taken to solve Minesweeper

class Alpha_Sweeper(object):
    
    def __init__(self,i,j):
        self.frame = np.zeros((i,j))
        total = j-np.random.randint(1,j-2)
        rand_rows = np.random.randint(0, i, total)
        rand_cols = np.random.randint(0, j, total)
        # For generating mines in the grid
        for i in range(total):
            self.frame[rand_rows[i], rand_cols[i]] = -99
        self.fill_matrix()
    
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
        self.begin_game()
        
    #To implement the game
    def begin_game(self):
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
                        output_frame = self.chance(i,j,output_frame)
                    elif (self.frame[i,j] < 0):
                        print ("Oops! You stepped on a MINE ('_') . Better luck next time!\n ")
                        break
                    if (self.frame[i,j] == 0):
                        self.reveal(i,j,output_frame)
                
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

    check = []
    # To reveal all adjecent safe cells when a safe cell is selected
    def reveal(self,i,j,output_frame):
        if (i<0 or i>=self.frame.shape[0] or j<0 or j>=self.frame.shape[1]):
            return
        if str(i)+str(j) in self.check:
            return
        if (self.frame[i,j] == -99 or output_frame[i,j] == '>'):
            return
        if (self.frame[i,j] not in (0, -99)):
            output_frame = self.chance(i,j,output_frame)
            self.check.append(str(i)+str(j))
            return
        else:
            output_frame[i,j]='S'
            self.check.append(str(i)+str(j))
            for k in range (i-1, i+2):
                for l in range (j-1, j+2):
                    self.reveal(k,l,output_frame)    

    # To implement the rule modification
    def chance(self,m,n,output_frame):
        chnc = random.randint(0,100)
         #if chnc in random.sample(range(0,100), 5):
        if chnc in (1,2,3,4,5):
            output_frame[m,n] = random.randint(0,9)
        else:
            output_frame[m,n] = self.frame[m,n]
        return output_frame

    
if __name__ == "__main__":
    print('Lets play Minesweeper!\n')
    f = 0
    while True:
        try:
            if f!=0:
                print ('Wanna try again?\n')
            f=1
            print ('Select grid size:\n')
            ch = int(input(' 1. 4x4 \n 2. 8x6 \n 3. 12x10 \n 4. 14x12 \n 5. exit\n'))
            if (ch == 1):
                alpha_ms = Alpha_Sweeper(4,4)
            elif (ch == 2):        
                alpha_ms = Alpha_Sweeper(8,6)
            elif (ch == 3):
                alpha_ms = Alpha_Sweeper(12,10)
            elif (ch == 4):
                alpha_ms = Alpha_Sweeper(14,12)
            elif (ch == 5):
                print("Lets play some other time")
                break
            else:
                print('Invalid response. Please try again')
        except KeyboardInterrupt:
            print("\nLets play some other time")
            break
        except:
            print('Invalid response. Please try again')
            f=0
            continue