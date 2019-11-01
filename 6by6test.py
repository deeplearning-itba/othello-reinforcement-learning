from othello.OthelloGame import OthelloGame as Game
from othello.OthelloGame import display as displayGame
import numpy as np
import collections
from timeit import time

import os
import shelve
import collections
def bfs_cannonical(game, root, folder, first_player=1):
    if not os.path.exists(folder):
        os.makedirs(folder)
    state_str = str(root.reshape(-1) + 1)[1:-1]
    seen = shelve.open(folder+'/seen', flag='n') 
    
    cannonical_states = shelve.open(folder+'/states', flag='c', writeback=True) 
    # cannonical_states = {}
    # deque es como una pila pero con doble entrada (rear-front)
    print('shelve opened... ')
    states_by_N = {}
    queue = collections.deque([state_str])
    count = 0
    while queue:
        count = count + 1
        vertex = queue.popleft()
        state = (np.array(vertex.split(' '), dtype=int) - 1).reshape(game.n, game.n)
        
        new_N = np.sum(abs(state))
        if new_N not in states_by_N:
            states_by_N[new_N] = 0
            
        states_by_N[new_N] = states_by_N[new_N] + 1
        if count % 10000 == 0:
            print('\r'+str(states_by_N), end='')
            seen.sync()
            cannonical_states.sync()
                
        
        valid_moves = np.array(game.getValidMoves(state, 1))
        valid_moves = np.where(valid_moves == 1)[0]
        if game.getGameEnded(state, 1) == 0:
            if vertex not in cannonical_states:
                cannonical_states[vertex] = {}
                for action in valid_moves:
                    cannonical_states[vertex][action] = {}
                    next_state, next_player = game.getNextState(state, 1, action)
                    next_state = game.getCanonicalForm(next_state, -1)
                    node = str(next_state.reshape(-1) + 1)[1:-1]
                    cannonical_states[vertex][action]['winner'] = game.getGameEnded(next_state, 1) # * np.abs(next_state.sum())
                    cannonical_states[vertex][action]['next_node'] = node
                    if node not in seen:
                        seen[node] = 1
                        # seen.add(node)
                        queue.append(node)
            else:
                for action, data in cannonical_states[vertex].items():
                    node = data['next_node']
                    if node not in seen:
                        seen[node] = 1
                        # seen.add(node)
                        queue.append(node)
                
        N = len(cannonical_states)
        if N%10000 == 0:
            print('\rstates: {}'.format(N), end='')
            cannonical_states.sync()
    print()
    cannonical_states.close()
    return


n = 6
game = Game(n)
board = game.getInitBoard()

bfs_cannonical(game, board, './data/6by6', first_player=1)