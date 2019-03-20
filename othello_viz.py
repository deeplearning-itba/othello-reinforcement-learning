from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

def plot_episode(game, states, initial_player=1):
    player_turn = initial_player
    cols = 6
    rows = int(np.ceil(len(states)/cols))
    f, axs = plt.subplots(rows, cols, figsize = (cols*3, 3*rows))
    f.patch.set_facecolor('lightgray')
    for i in range(cols*rows):
        ax = axs[int(i/cols), i%cols]
        ax.axis('off')
        if i<len(states):
            display_board(game, states[i] * player_turn, player_turn = player_turn, ax = ax)
            player_turn = -1 * player_turn

def display_board(game, board, player_turn= None, valid_moves = None, figsize = (3, 3), ax = None, value_func=None):
    """(1 for white, -1 for black, 0 for empty spaces)"""
    ny, nx = board.shape
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize = figsize)
        f.patch.set_facecolor('lightgray')
    radius = 0.4
    if player_turn:
        if game.getGameEnded(board, 1) == 1:
            ax.set_title('White Wins')
        elif game.getGameEnded(board, -1) == 1:
            ax.set_title('Black Wins')
        elif game.getGameEnded(board, -1) == -0.2:
            ax.set_title('Tie')
        elif player_turn == 1:
            ax.set_title('White Plays')
        else:
            ax.set_title('Black Plays')
    if valid_moves is not None:
        valid_moves_array = valid_moves[:ny*nx].reshape([ny,nx])[::-1].T
    value_data = []
    not_valid_value = 31415
    if value_func and valid_moves is not None:
        for action, move in enumerate(valid_moves[:-1]):
            if move == 1:
                next_board, next_player_turn = game.getNextState(board, player_turn, action)
                next_board = game.getCanonicalForm(next_board, next_player_turn)
                if game.getGameEnded(next_board, 1) != 0:
                    # Game Ends!
                    value_data.append(-value_func[tuple(game.getCanonicalForm(board, player_turn).reshape(-1))])
                elif tuple(next_board.reshape(-1)) in value_func:
                    value_data.append(-value_func[tuple(next_board.reshape(-1))])
                else:
                    print('It should not enter here. Check bug!')
                    value_data.append(0)
            else:
                value_data.append(not_valid_value)
        value_data_array = np.array(value_data).reshape([ny,nx])[::-1].T  
    for j, row in enumerate(board):
        for i, player in enumerate(row):
            ypos = ny - j - 1
            xpos = i
            if player == 1:
                circle = patches.Circle([xpos, ypos], radius, color='w')
                ax.add_patch(circle)
            elif player == -1:
                circle = patches.Circle([xpos, ypos], radius, color='k')
                ax.add_patch(circle)
            elif player == 0:
                circle = patches.Circle([xpos, ypos], radius, color='gray', alpha=0.1)
                ax.add_patch(circle)
            if valid_moves is not None and valid_moves_array[xpos, ypos] == 1:
                circle = patches.Circle([xpos, ypos], radius, color='gray', alpha=0.1)
                ax.add_patch(circle)
                if value_func is not None and value_data_array[xpos, ypos]!=not_valid_value:
                    text = ax.text(xpos, ypos, "", va="bottom", ha="left")
                    text.set_text(value_data_array[xpos, ypos])
                circle = patches.Circle([xpos, ypos], 
                                        radius, 
                                        fill = False,
                                        linewidth=1, 
                                        color='k',
                                        alpha=0.2,
                                        linestyle='-.')
                ax.add_patch(circle)
           
    ax.axis('off')
    ax.set_xlim([-0.5, nx - 0.5])
    ax.set_ylim([-0.5, ny - 0.5])
    ax.set_facecolor([0.5, 0.5, 0.5])