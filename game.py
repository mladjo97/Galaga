from PyQt5.Qt import QTimer
from PyQt5.QtWidgets import QWidget, qApp
from PyQt5.QtGui import QPainter, QPixmap
from threading import Thread
import board
import config


class Game(QWidget):

    def __init__(self, players):
        super(Game, self).__init__()

        self.enemiesLeft = 30
        self.players = players
        self.board = board.Board()

        self.drawBoardTimer = QTimer()
        self.drawBoardTimer.setInterval(config.GAME_SPEED)
        self.drawBoardTimer.timeout.connect(self.repaint)
        self.drawBoardTimer.start()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_board(painter)
        painter.end()

    def draw_board(self, painter):
        width = config.TILE_WIDTH
        height = config.TILE_HEIGHT

        for x in range(config.BOARD_WIDTH):
            for y in range(config.BOARD_HEIGHT):
                pos_x = x * width
                pos_y = y * height

                if self.board.tiles[x, y] == config.TILE_BACKGROUND:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/background.png'))
                elif self.board.tiles[x, y] == config.TILE_LIVES:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/lives.png'))
                elif self.board.tiles[x, y] == config.TILE_ZEROLIVES:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/zero.png'))
                elif self.board.tiles[x, y] == config.TILE_ONELIFE:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/one.png'))
                elif self.board.tiles[x, y] == config.TILE_TWOLIVES:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/two.png'))
                elif self.board.tiles[x, y] == config.TILE_THREELIVES:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/three.png'))
                elif self.board.tiles[x, y] == config.TILE_PLAYER:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/ship.png'))
                elif self.board.tiles[x, y] == config.TILE_ENEMY:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/enemy.png'))
                elif self.board.tiles[x, y] == config.TILE_PLAYERLASER:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/laser.png'))
                elif self.board.tiles[x, y] == config.TILE_ENEMYLASER:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/enemy_laser.png'))
                else:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('images/background.png'))

