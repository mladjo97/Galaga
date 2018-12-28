from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import config

class Game(QWidget):

    def __init__(self, players):
        super(Game, self).__init__()

        self.activePlayers = players
        self.playerSpeed = config.PLAYER_SPEED
        self.playerWidth = config.PLAYER_WIDTH
        self.playerHeight = config.PLAYER_HEIGHT

        self.playerPixmap = QPixmap('images/ship.png')
        self.playerLabel = QLabel(self)

        self.__init_ui__()

    def __init_ui__(self):
        # Set player
        self.playerLabel.setPixmap(self.playerPixmap)
        self.playerLabel.setGeometry(config.BOARD_WIDTH // 2 - self.playerWidth, config.BOARD_HEIGHT - 50, self.playerWidth, self.playerHeight)

    def try_move_player(self, x):
        if x == config.BOARD_WIDTH - self.playerWidth or x == 0:
            print('udara granicu')
            return False
        return True

    def __update_position__(self, key):
        playerPos = self.playerLabel.geometry()

        if key == Qt.Key_D:
            if self.try_move_player(playerPos.x() + self.playerSpeed):
                self.playerLabel.setGeometry(playerPos.x() + self.playerSpeed, playerPos.y(), playerPos.width(), playerPos.height())
        elif key == Qt.Key_A:
            if self.try_move_player(playerPos.x() - self.playerSpeed):
                self.playerLabel.setGeometry(playerPos.x() - self.playerSpeed, playerPos.y(), playerPos.width(), playerPos.height())

