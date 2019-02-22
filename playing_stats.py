import numpy as np

class EvaluatePolicy():
    def __init__(self, pi):
        self.pi = pi
        
    def random_player(self, game, board):
        valid_modes = game.getValidMoves(board, 1)
        valid_moves_idxs = np.where(valid_modes == 1)[0]
        action = np.random.choice(valid_moves_idxs)
        return action

    def greedy_player(self, game, board):
        valids = np.array(game.getValidMoves(board, 1))
        scores = []
        indexes = []
        for a in np.where(valids == 1)[0]:
            nextBoard, _ = game.getNextState(board, 1, a)
            score = game.getScore(nextBoard, 1)
            scores.append(score)
            indexes.append(a)
        scores_indxs = np.where(np.array(scores) == max(scores))[0]    
        return indexes[np.random.choice(scores_indxs)]

    def policy_player(self, game, board):
        board_str = game.stringRepresentation(board)
        return self.pi[board_str]
    
    def play_episode(self, game, board, players_policies):
        player = 1
        while game.getGameEnded(board, player) == 0:
            # Jugador 1
            board_cann = game.getCanonicalForm(board, player)
            board_str = game.stringRepresentation(board_cann)
            action = players_policies[player](game, board_cann)
            board, player = game.getNextState(board, player, action)
        return board
    
    def get_stats(self, game, board, players_dict, episodes = 100):
        player_1_wins = 0
        player_2_wins = 0
        ties = 0
        for i in range(episodes):
            last_board = self.play_episode(game, board, players_dict)
            diff = last_board.sum()
            if diff > 0:
                player_1_wins = player_1_wins + 1
            if diff < 0:
                player_2_wins = player_2_wins + 1
            if diff == 0:
                ties = ties + 1   
        return player_1_wins, player_2_wins, ties