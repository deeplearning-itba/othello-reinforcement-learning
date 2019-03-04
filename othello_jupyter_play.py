from othello_viz import display_board
from othello.OthelloGame import OthelloGame as Game
from matplotlib import pyplot as plt

class Play_Othello:
    def __init__(self, n=4, first_player = 1, board=None):
        self.game = Game(n)
        if board is None:
            self.board = self.game.getInitBoard()
        else:
            if n != board.shape[0]:
                print('n and board mismatch!!')
                return
            else:
                self.board = board
        self.n = self.board.shape[0]
        self.figure, self.ax = plt.subplots(1, 1, figsize = (3, 3), num='Othello for Jupyter lab')
        self.figure.patch.set_facecolor('lightgray')
        self.text = self.ax.text(-1,-1, "", va="bottom", ha="left")
        self.player = first_player
        
        display_board(self.game, 
                      self.board, 
                      player_turn= self.player, 
                      valid_moves = self.game.getValidMoves(self.board, self.player), 
                      figsize = (3, 3), 
                      ax = self.ax)
        self.connect()
        self.text.set_text('Comenzado')
        
    def connect(self):
        self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        
    def clearBoard(self):
        self.ax.cla()
        self.text = self.ax.text(-1,-1, "", va="bottom", ha="left")
        
    def onclick(self, event):
        x = int(event.xdata + 0.5)
        y = int(event.ydata + 0.5)
        action = x + (self.n - 1 -y) * self.n
        #tx = 'action=%d, xdata=%f, ydata=%f' % (action, x, y)
        # self.text.set_text(str(action))
        if self.game.getValidMoves(self.board, self.player)[action] == 1:
            self.clearBoard()
            self.board, self.player = self.game.getNextState(self.board, self.player, action)
            display_board(self.game, 
                          self.board, 
                          player_turn= self.player, 
                          valid_moves = self.game.getValidMoves(self.board, self.player), 
                          figsize = (3, 3), 
                          ax = self.ax)
            self.text.set_text('')
            ended = self.game.getGameEnded(self.board, self.player)
            if ended==0 and self.game.getValidMoves(self.board, self.player)[self.n*self.n] == 1:
                self.clearBoard()
                self.board, self.player = self.game.getNextState(self.board, self.player, 16)
                display_board(self.game, 
                              self.board, 
                              player_turn= self.player, 
                              valid_moves = self.game.getValidMoves(self.board, self.player), 
                              figsize = (3, 3), 
                              ax = self.ax)
                ended = self.game.getGameEnded(self.board, self.player)
            if ended!=0:
                self.text.set_text('Terminado')
        else:
            # tx = 'action=%d, xdata=%f, ydata=%f' % (action, x, y)
            self.text.set_text('Invalid move: ' + str(action))