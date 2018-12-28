import numpy as np
import config
import player


class Board(object):

    def __init__(self):
        super(Board, self).__init__()

        self.width = config.BOARD_WIDTH
        self.height = config.BOARD_HEIGHT
        self.player = player.Player(0, 0)

        self.create_board()

    def create_board(self):
        pass

