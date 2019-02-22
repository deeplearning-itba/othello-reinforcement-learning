import collections
from othello.OthelloGame import OthelloGame as Game
from othello.OthelloGame import display as displayGame
import numpy as np
from timeit import time

def dfs(game, state, visited):
    state_str = game.stringRepresentation(state)
    if state_str not in visited:
        visited.append(state_str)
        valid_moves = np.array(game.getValidMoves(state, 1))
        valid_moves = np.where(valid_moves == 1)[0]
        if game.getGameEnded(state, 1) == 0:
            for action in valid_moves:
                next_state, _ = game.getNextState(state, 1, action)
                next_state = game.getCanonicalForm(next_state, -1)
                dfs(game, next_state, visited)
    return visited

def bfs_no_depth(game, root):
    root_str = game.stringRepresentation(root)
    seen = set([(root_str, 1)])
    cannonical_states = []
    # deque es como una pila pero con doble entrada (rear-front)
    queue = collections.deque([(root_str, 1)])
    
    while queue:
        vertex, player = queue.popleft()
        state = np.frombuffer(vertex, dtype=int).reshape(game.n, game.n)
        valid_moves = np.array(game.getValidMoves(state, player))
        valid_moves = np.where(valid_moves == 1)[0]
        cannonical_states.append(game.stringRepresentation(game.getCanonicalForm(state, player)))
        if game.getGameEnded(state, player) == 0:
            for action in valid_moves:
                next_state, next_player = game.getNextState(state, player, action)
                next_state_str = game.stringRepresentation(next_state)
                #print(action, next_state)
                if (next_state_str, next_player) not in seen:
                    seen.add((next_state_str, next_player))
                    queue.append((next_state_str, next_player))
            player = next_player
    return cannonical_states

def bfs_depth(game, root, verbose=0):
    n = root.shape[0]
    root_str = tuple(root.reshape(-1))
    depth = 0
    seen = set([(root_str, np.power(-1, depth))])
    cannonical_states = {}
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
                print('Estados hasta el momento:', len(cannonical_states))
                time1 = time.time()
                print('Time:', int((time1 - time0) * 100)/100)
                time0 = time1
            if vertex == 'level_end':
                break
        state = np.array(vertex).reshape(n, n)
        valid_moves = np.array(game.getValidMoves(state, player))
        valid_moves = np.where(valid_moves == 1)[0]
        if game.getGameEnded(state, player) == 0:
            cannonical_states[vertex] = {}
            for action in valid_moves:
                cannonical_states[vertex][action] = {}
                next_state, _ = game.getNextState(state, player, action)
                node = tuple(next_state.reshape(-1))
                if (node, player) not in seen:
                    cannonical_states[vertex][action]['next_node'] = node*player
                    seen.add((node, player))
                    queue.append(node)
    return cannonical_states

def bfs_cannonical(game, root):
    state_str = game.stringRepresentation(root)
    seen = set([])
    cannonical_states = {}
    # deque es como una pila pero con doble entrada (rear-front)
    queue = collections.deque([state_str])
    while queue:
        vertex = queue.popleft()
        state = np.frombuffer(vertex, dtype=int).reshape(game.n, game.n)
        valid_moves = np.array(game.getValidMoves(state, 1))
        valid_moves = np.where(valid_moves == 1)[0]
        if game.getGameEnded(state, 1) == 0:
            cannonical_states[vertex] = {}
            for action in valid_moves:
                cannonical_states[vertex][action] = {}
                next_state, next_player = game.getNextState(state, 1, action)
                next_state = game.getCanonicalForm(next_state, -1)
                node = game.stringRepresentation(next_state)
                cannonical_states[vertex][action]['reward'] = game.getGameEnded(next_state, 1)
                cannonical_states[vertex][action]['next_node'] = node
                if node not in seen:
                    seen.add(node)
                    queue.append(node)
        
    return cannonical_states