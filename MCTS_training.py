# Importing required libraries
import itertools as it
import Minesweeper_game as ms
import AlphaSweeper_MCTS as mcts
import torch as tr


def generate(r_grid,c_grid,num_games,num_rollouts,max_depth,choose_method=None):

    if choose_method is None: choose_method = mcts.puct

    data = []    
    for game in range(num_games):
    
        alpha_ms, curr_state = ms.initial_state(r_grid,c_grid)
        for turn in it.count():
            print("game %d, turn %d..." % (game, turn))
    
            # Stop when game is over
            if curr_state.is_leaf(alpha_ms): break
                
            # Otherwise, use MCTS
            child,curr_node,tnodes = mcts.mcts_action(curr_state,alpha_ms,num_rollouts=1000,max_depth=100,child_method=choose_method,verbose=True)
            curr_state = curr_node.children(alpha_ms)[child].state
            
            # Add child states and their values to the data
            Q = curr_node.get_score_estimates()
            for ctr,child in enumerate(curr_node.children(alpha_ms)):
                data.append((child.state, Q[ctr]))

    return data


def encode(state):
    encoded_tensor = tr.zeros(5,state.ms_grid.shape[0],state.ms_grid.shape[1])
    for rctr in range(state.ms_grid.shape[0]):
        for cctr in range(state.ms_grid.shape[1]):
            if state.ms_grid[rctr][cctr] == -1:
                encoded_tensor[:,rctr,cctr] = tr.tensor([1,0,0,0,0])
            elif state.ms_grid[rctr][cctr] == -2:
                encoded_tensor[:,rctr,cctr] = tr.tensor([0,1,0,0,0])
            elif state.ms_grid[rctr][cctr] == 0:
                encoded_tensor[:,rctr,cctr] = tr.tensor([0,0,1,0,0])
            elif state.ms_grid[rctr][cctr] > 0:
                encoded_tensor[:,rctr,cctr] = tr.tensor([0,0,0,1,0])
            elif state.ms_grid[rctr][cctr] == -99:
                encoded_tensor[:,rctr,cctr] = tr.tensor([0,0,0,0,1])          
    return encoded_tensor


def get_batch(r_grid,c_grid,num_games,num_rollouts=100,max_depth=10,choose_method=None):
    data = generate(r_grid=r_grid,c_grid=c_grid,num_games=num_games,num_rollouts=num_rollouts,max_depth=max_depth,choose_method=choose_method)
    
    enc_states = []
    score_list = []
    for state,score in data:
        enc_states.append(encode(state))
        score_list.append(tr.tensor(float(score)))
    inputs = tr.stack(enc_states)
    outputs = tr.stack(score_list)
    outputs = tr.reshape(outputs,(len(score_list),1))
    return inputs,outputs
        
if __name__ == "__main__":
    
    r, c = map(int, input('Enter the Grid Size : (row,column)').split(','))
    num_games = int(input('Enter the number of games to simulate :'))
    inputs, outputs = get_batch(r_grid=r,c_grid=c, num_games=num_games)
    print(inputs[-1])
    print(outputs[-1])

    import pickle as pk
    with open("data-%dX%d.pkl" % (r,c),"wb") as f: pk.dump((inputs, outputs), f)
