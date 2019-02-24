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
        # board_str = game.stringRepresentation(board)
        board_str = tuple(board.reshape(-1))
        return self.pi[board_str]
    
    def play_episode(self, game, board, players_policies):
        player = 1
        steps = 0
        while game.getGameEnded(board, player) == 0:
            # Jugador 1
            board_cann = game.getCanonicalForm(board, player)
            # board_str = game.stringRepresentation(board_cann)
            board_str = tuple(board_cann.reshape(-1))
            action = players_policies[player](game, board_cann)
            board, player = game.getNextState(board, player, action)
            steps += 1
        return board, steps
    
    def get_stats(self, game, board, players_dict, episodes = 100):
        player_1_wins = 0
        player_2_wins = 0
        ties = 0
        margins = []
        steps_array = []
        pieces = []
        for i in range(episodes):
            last_board, steps = self.play_episode(game, board, players_dict)
            steps_array.append(steps)
            margin = last_board.sum()
            pieces.append(np.abs(last_board).sum())
            margins.append(margin)
            if margin > 0:
                player_1_wins = player_1_wins + 1
            if margin < 0:
                player_2_wins = player_2_wins + 1
            if margin == 0:
                ties = ties + 1   
        return player_1_wins, player_2_wins, ties, np.array(margins), np.array(steps_array), np.array(pieces) 