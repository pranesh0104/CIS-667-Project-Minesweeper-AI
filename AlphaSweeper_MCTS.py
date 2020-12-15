import numpy as np
import math
import random
import Minesweeper_game as ms

acc_nodes_rollout = 0

def uniform(node,alpha_ms):
    best_choice = np.random.choice(len(node.children(alpha_ms))) # choose child at random
    return node.children(alpha_ms)[best_choice]

def puct(node,alpha_ms):
    best_choice = np.random.choice(len(node.children(alpha_ms)), p=child_UCT_probs(node))
    return node.children(alpha_ms)[best_choice]

    
class Node(object):
    
    def __init__(self,state,depth = 0, child_method=uniform):
        self.state = state
        self.child_list = None
        self.visit_count = 0
        self.score_total = 0
        #self.score_estimate = 0
        self.depth = depth
        self.child_method = child_method
        
    def make_child_list(self,alpha_ms):
        self.child_list = []
        actions = self.state.valid_actions()
        #if (actions == []): print("No actions")
        for row,col in actions:
            for option in range(2):
                child_state = self.state.perform_action(alpha_ms,row,col,option)
                if child_state != None and np.count_nonzero(child_state.ms_grid == -2) <= np.count_nonzero(alpha_ms == -99) :
                    self.child_list.append(Node(child_state,self.depth+1,self.child_method))
                    
            
    def children(self,alpha_ms):
        if self.child_list is None: self.make_child_list(alpha_ms)
        return self.child_list
    
    def get_score_estimates(self):
        Q = []
        for child in self.child_list:
            if child.visit_count == 0:
                Q.append(0)
            else:
                Q.append(child.score_total/child.visit_count)
        return Q
    
    def get_visit_counts(self):
        N = []
        for child in self.child_list:
            N.append(child.visit_count)
        return N
    
    def choose_child(self,alpha_ms):
        return self.child_method(self,alpha_ms)

    
def child_UCT_probs(node):
    U = []
    N = node.get_visit_counts()
    Q = node.get_score_estimates()
    if len(N) == len(Q):
        for Nc,Qc in zip(N,Q):
            U.append(Qc + math.sqrt(math.log(node.visit_count+1)/(Nc+1)))
    softmax_sum = np.sum(np.exp(U),axis=0)
    probs = [math.exp(num)/softmax_sum for num in U]
    return probs

    
def rollout(node, alpha_ms,max_depth=None):
    
    global acc_nodes_rollout
    if node.depth == max_depth or node.state.is_leaf(alpha_ms): result = node.state.player_score(alpha_ms)
    else:
        acc_nodes_rollout +=1
        result = rollout(node.choose_child(alpha_ms),alpha_ms,max_depth)
    node.visit_count += 1
    node.score_total += result
    return result
            
def mcts_action(state,alpha_ms,num_rollouts,max_depth,child_method=puct,verbose=False):
    global acc_nodes_rollout
    acc_nodes_rollout = 0
    curr_node = Node(state,child_method=child_method)
    for roll_ctr in range(num_rollouts):
        if verbose and roll_ctr%100 == 0: print("%d Rollout of %d ..."% (roll_ctr+1,num_rollouts))
        rollout(curr_node, alpha_ms,max_depth=max_depth)
    action_select = np.argmax(curr_node.get_score_estimates())
    return action_select,curr_node,acc_nodes_rollout

def uniform_action(state,alpha_ms,num_rollouts,max_depth,child_method=uniform,verbose=False):
    curr_node = Node(state,child_method=child_method)
    for roll_ctr in range(num_rollouts):
        if verbose and roll_ctr%100 == 0: print("%d Rollout of %d ..."% (roll_ctr+1,num_rollouts))
        rollout(curr_node, alpha_ms,max_depth=max_depth)
    action_select = np.argmax(curr_node.get_score_estimates())
    return action_select,curr_node

if __name__ == "__main__":
    
    
    game_type = int(input('Select Game Type\n(1) Text Based Playable Game\n(2) Baseline AI\n(3) MCTS AI'))
    if game_type == 1:
    	ms.textBasedGame()
    else:
        print('Select grid size:\n')
        ch = int(input(' 1. 4x4 \n 2. 5x5 \n 3. 6x6 \n 4. 7x7 \n 5. 8x8 6.exit\n'))
        if ch == 1: r,c = 4,4
        elif ch == 2: r,c = 5,5
        elif ch == 3: r,c = 6,6
        elif ch == 4: r,c = 7,7
        else: r,c = 8,8
        alpha_ms, curr_state = ms.initial_state(r,c)
        print("Initial Grid\n",curr_state)
        print("Generated Grid\n",alpha_ms)
        while (not(curr_state.is_leaf(alpha_ms))): # stop when game is over
	        # Select child action using the mcts_action module in mcts
	        if game_type == 2: child,curr_node = uniform_action(curr_state,alpha_ms,num_rollouts=1000,max_depth=100,child_method=uniform,verbose=True)
	        elif game_type == 3:
	            child,curr_node,acc_tnodes = mcts_action(curr_state,alpha_ms,num_rollouts=1000,max_depth=100,child_method=puct,verbose=True)
	            print("Number of nodes accessed for choosing ACTION -> ",acc_tnodes)
	        curr_state = curr_node.children(alpha_ms)[child].state
	        print(curr_state)
	        if (input("Press Enter to run next step (Any other key to exit)\n") == ""): continue
	        else:
	            break 
	    