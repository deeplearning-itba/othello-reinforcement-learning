from othello.OthelloGame import OthelloGame as Game
from othello.OthelloGame import display as displayGame
import numpy as np
import collections
from timeit import time

def bfs_depth(game, root, verbose=0):
    n = root.shape[0]
    root_str = tuple(root.reshape(-1))
    depth = 0
    seen = set([(root_str, np.power(-1, depth))])
    cannonical_states = 0
    # deque es como una pila pero con doble entrada (rear-front)
    queue = collections.deque([root_str, 'level_end'])
    player = 1
    time0 = time.time()
    while queue:
        vertex = queue.popleft()
        if vertex == 'level_end':
            depth = depth + 1
            player = np.power(-1, depth)
            queue.append('level_end')
            vertex = queue.popleft()   
            if verbose == 1:
                print('Profundidad:', depth)
                print('Estados hasta el momento:', cannonical_states)
                time1 = time.time()
                print('Time:', int((time1 - time0) * 100)/100)
                time0 = time1
            if vertex == 'level_end':
                break
        state = np.array(vertex).reshape(n, n)
        valid_moves = np.array(game.getValidMoves(state, player))
        valid_moves = np.where(valid_moves == 1)[0]
        if game.getGameEnded(state, player) == 0:
            for action in valid_moves:
                cannonical_states = cannonical_states + 1
                next_state, _ = game.getNextState(state, player, action)
                node = tuple(next_state.reshape(-1))
                if (node, player) not in seen:
                    seen.add((node, player))
                    queue.append(node)
    return cannonical_states

n = 6
game = Game(n)
board = game.getInitBoard()
states_depth = bfs_depth(game, board, verbose=1)