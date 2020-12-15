
# Running Text-based Minesweeper.py
No Library Dependencies.
Only used numpy,random and time libraries.

Run the code in the terminal using the syntax "python AI_Minesweeper.py"

# Once the program is executed, the user will be prompted to select a grid size from the list of options.User can input a number between 1-4 corresponding to a grid size and 5 to   exit
# Upon grid selection, the user will input row and column indices in the format "row,column" to select a game square where an action is to be performed. Also you can enter "-1,-1"   to exit to main menu.
# Once a square is selected, the user can choose from 2 valid actions - Reveal, Flag. Reveal will display the value of the sqaure. The Flag option lets you flag/un-flag the         selected square
# Game ends if a mine is revealed (You Lose) or once you have flagged all the mines and revealed all the other game squares (You Win).



# Running AlphaSweeper_MCTS.py
Required Code Dependency - Minesweeper_game.py (Already impported in Code)
used numpy, math, and random

Run the code in the terminal using the syntax "python AlphaSweeper_MCTS.py"


# Once the program is executed, the user will be prompted to input a custom grid size in the format "rowsize,columnsize"
# Upon grid selection, the Tree search algorithm wlll make use of MCTS to perform specified number of rollouts
# When an ideal action is chosen, user will be prompted to press "Enter" to continue the process or enter any other key to exit.

# Running MCTS_Training.py
Required Code Dependency - Minesweeper_game.py,AlphaSweeper_MCTS
Used itertools, torch

Run the file and enter the grid size for which you want to generate training data. After training for a number of games specified by user, the data is outputed to a pkl file which 
can next be used to build the neural network

# Running Minesweeper_NN.py
No Code Dependency
Use torch.nn and torch.optim

Run this file and select the grid size you want to train the network on. make sure you have run the MCTS_training.py file for the corresponding grid size beore you run this.
Once grid size is inputed, the model is trained and the learning curve and the scatterplot for the actual values vs Target values are outputted.

# Running AlphaSweeper_NN+MCTS.py
Required Code Dependency - Minesweeper_game.py,AlphaSweeper_MCTS,MCTS_training, Minesweeper_NN
Run this file and first select the type of user which can be human, a base AI, MCTS AI or a MCTS+NN AI. Then select the corresponding grid size to start running the game.
