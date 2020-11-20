import numpy as np
import math
import random
from Minesweeper_game import initial_state

class Node(object):
    def __init__(self,state):
        self.state = state
        self.visit_count = 0.
        self.score_total = 0.
        self.score_estimate = 0.
    def children(self, alpha_ms):
        actions = self.state.valid_actions() # will return empty list ("[]") when no actions possible (end state reached)
        child_list = []
        for r,c in actions:
            for option in range(2):
                child,i,j = self.state.perform_action(alpha_ms,r,c,option)
                child_list.append(Node(child))
        return child_list
    def choose_child_UCT(self, alpha_ms):
        child_nodes = self.children(alpha_ms)
        max_uct = -100
        child_uct = child_nodes[random.randint(0,len(child_nodes)-1)]
        for child in child_nodes:
            if (self.visit_count == 0. or child.visit_count == 0.):
                comp_uct = math.inf
            else:
                comp_uct = child.score_estimate + (2)*(math.log(self.visit_count)/(child.visit_count))
            if comp_uct > max_uct:
                max_uct = comp_uct
                child_uct = child
        print("Chosen child ->",child_uct,"-Score-",max_uct)
        return child_uct

def rollout(node, alpha_ms):
    if node.state.is_leaf(): result = node.state.player_score()
    else: result = rollout(node.choose_child_UCT(alpha_ms),alpha_ms)
    node.visit_count += 1
    node.score_total += result
    node.score_estimate = node.score_total/node.visit_count
    return result
            
def mcts(node, alpha_ms):
    for roll_ctr in range(20):
        if roll_ctr%2 == 0:
            print(roll_ctr+1," out of 20")
        rollout(node, alpha_ms)
    a = np.argmax([child.score_estimate for child in node.children(alpha_ms)])
    print(node.children(alpha_ms)[a].state)
    return (node.children(alpha_ms)[a])

if __name__ == "__main__":
    
    i, j = map(int, input('Enter the Grid Size : (row,column)').split(','))
    alpha_ms, state = initial_state(i,j)
    print(state)
    print(alpha_ms)
    move_list = []
    current_cell = Node(state)
    while (not(current_cell.state.is_leaf())):
        child = mcts(current_cell, alpha_ms)
        current_cell = child
        move_list.append(current_cell)
        if (input("Press Enter to run next step (Any other key to exit)\n") == ""): continue
        else:
            break
    
    