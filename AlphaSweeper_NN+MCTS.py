import itertools as it
import numpy as np
import torch as tr
import Minesweeper_game as ms
import AlphaSweeper_MCTS as mcts
import MCTS_training as ms_data
import Minesweeper_NN as ms_nn


AI_type = int(input('Choose User - (1) Human, (2) Baseline AI, (3) MCTS AI, (4) MCTS+NN AI : '))
if AI_type!=1:
    print ('Select grid size:\n')
    ch = int(input(' 1. 4x4 \n 2. 5x5 \n 3. 6x6 \n 4. 7x7 \n 5. 8x8 6.exit\n'))
    if ch == 1: r,c = 4,4
    elif ch == 2: r,c = 5,5
    elif ch == 3: r,c = 6,6
    elif ch == 4: r,c = 7,7
    else: r,c = 8,8
    net = ms_nn.MSNet1(r,c)
    net.load_state_dict(tr.load("model-%dX%d.pth" % (r,c)))

def nn_puct(node,alpha_ms):
    with tr.no_grad():
        x = tr.stack(tuple(map(ms_data.encode, [child.state for child in node.children(alpha_ms)])))
        y = net(x)
        probs = tr.softmax(y.flatten(), dim=0)
        best_choice = np.random.choice(len(probs), p=probs.detach().numpy())
    return node.children(alpha_ms)[best_choice]

   

if __name__ == "__main__":
    
    if AI_type ==1:
        ms.textBasedGame()
    else:
        alpha_ms, curr_state = ms.initial_state(r,c)
        print("Initial Grid\n",curr_state)
        print("Generated Grid\n",alpha_ms)
        
    
        while (not(curr_state.is_leaf(alpha_ms))): # stop when game is over
            # Select child action using the mcts_action module in mcts
            if AI_type == 2: child,curr_node = mcts.uniform_action(curr_state,alpha_ms,num_rollouts=50,max_depth=100,child_method=mcts.uniform,verbose=True)
            elif AI_type == 3:
                child,curr_node,acc_tnodes = mcts.mcts_action(curr_state,alpha_ms,num_rollouts=50,max_depth=100,child_method=mcts.puct,verbose=True)
                print("Number of nodes accessed for choosing ACTION -> ",acc_tnodes)
            elif AI_type == 4:
                child,curr_node,acc_tnodes = mcts.mcts_action(curr_state,alpha_ms,num_rollouts=50,max_depth=100,child_method=nn_puct,verbose=True)
                print("Number of nodes accessed for choosing ACTION -> ",acc_tnodes)
            curr_state = curr_node.children(alpha_ms)[child].state
            print(curr_state)
            if (input("Press Enter to run next step (Any other key to exit)\n") == ""): continue
            else:
                break
        print("Game over!")