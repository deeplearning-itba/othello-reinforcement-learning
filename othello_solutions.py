from urllib.request import urlopen # Python 3
import os
import numpy as np

def download_value_func(link, filename):
    response = urlopen(link)
    file_size = response.length
    CHUNK = 16 * 1024
    downloaded = 0
    print('Donwloading: ', link)
    print('Saving it as: ', filename)
    with open(filename, 'wb') as f:
        while True:
            read_chunk = response.read(CHUNK)
            if not read_chunk:
                break
            downloaded = downloaded + len(read_chunk)
            print('\r','Progress: %'+str(int(100*downloaded/file_size + 0.5)), end='')
            f.write(read_chunk)
    print()
    
def get_solution(name):
    """
    WIN_LOOSE: The reward is 1 for winning, -1 for loosing, 0 for tie
    MAXIMIZE_MARGIN: The reward is different between the number winner pieces vs number of looser pieces at the end of the game
    MINIMIZE_PIECES: The reward is (16 - number of pieces in the board) for the winner
    MINIMIZE_STEPS: The reward is (N - number of steps) for the winner. Where N should be bigger than the maximim possible number of steps
    """
    solutions = {
        'WIN_LOOSE': {'value_func': {'filename': 'V_WIN_LOOSE.npy', 'url': 'https://github.com/jganzabal/othello-reinforcement-learning/blob/master/V_WIN_LOOSE.npy?raw=true'}},
        'MAXIMIZE_MARGIN': {'value_func': {'filename': 'V_MAXIMIZE_MARGIN.npy', 'url': 'https://github.com/jganzabal/othello-reinforcement-learning/blob/master/V_MAXIMIZE_MARGIN.npy?raw=true'}},
        'MINIMIZE_PIECES': {'value_func': {'filename': 'V_MINIMIZE_PIECES.npy', 'url': 'https://github.com/jganzabal/othello-reinforcement-learning/blob/master/V_MINIMIZE_PIECES.npy?raw=true'}},
        'MINIMIZE_STEPS': {'value_func': {'filename': 'V_MINIMIZE_STEPS.npy', 'url': 'https://github.com/jganzabal/othello-reinforcement-learning/blob/master/V_MINIMIZE_STEPS.npy?raw=true'}}
    }
    val_func = solutions[name]['value_func']
    if os.path.isfile(val_func['filename']):
        print('Already downloaded, remove it if you want to download it again.')
    else:
        download_value_func(val_func['url'], val_func['filename'])
    
    return np.load(val_func['filename'], allow_pickle=True).item()