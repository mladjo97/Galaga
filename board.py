import numpy as np
import config
import player


class Board(object):

    def __init__(self):
        super(Board, self).__init__()

        self.width = config.BOARD_WIDTH
        self.height = config.BOARD_HEIGHT
        self.player = player.Player(0, 0)

        self.tiles = np.zeros((self.width, self.height), dtype=int)
        self.create_board()

    def create_board(self):
        # init background
        for i in range(self.width):
            for j in range(self.height):
                self.tiles[i, j] = config.TILE_BACKGROUND

        for i in range(5, 15):
            for j in range(1, 4):
                self.tiles[i, j] = config.TILE_ENEMY

        # Set Player 1
        self.tiles[config.BOARD_WIDTH // 2 - 1, config.BOARD_HEIGHT - 1] = config.TILE_PLAYER
        self.player.move(config.BOARD_WIDTH // 2 - 1, config.BOARD_HEIGHT - 1)

        # Set Lives label
        self.tiles[0, 0] = config.TILE_LIVES
        self.tiles[1, 0] = config.TILE_THREELIVES
