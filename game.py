from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import config
from player import Player
from time import sleep
from threading import Thread, Lock
from player_actions import MoveLaser


class Game(QWidget):

    def __init__(self, players):
        super().__init__()

        # MoveLaser 'thread'
        self.moveLaser = MoveLaser()
        self.moveLaser.calc_done.connect(self.move_laser_up)
        self.moveLaser.start()

        # Gameplay options
        self.activePlayers = players
        self.playerSpeed = config.PLAYER_SPEED
        self.playerWidth = config.IMAGE_WIDTH
        self.playerHeight = config.IMAGE_HEIGHT

        # Add player one
        self.playerPixmap = QPixmap('images/ship.png')
        self.playerLabel = QLabel(self)
        self.player = Player(0, 0)

        self.__init_ui__()

    def __init_ui__(self):
        # Set player start position
        self.playerLabel.setPixmap(self.playerPixmap)
        playerLabelX = config.BOARD_WIDTH // 2 - self.playerWidth
        playerLabelY = config.BOARD_HEIGHT - self.playerHeight
        self.playerLabel.setGeometry(playerLabelX, playerLabelY, self.playerWidth, self.playerHeight)

    def try_move_player(self, x):
        if x == config.BOARD_WIDTH - self.playerWidth or x == 0:
            return False
        return True

    def player_shoot_laser(self, startX, startY):
        laserPixmap = QPixmap('images/laser.png')
        laserLabel = QLabel(self)

        laserLabel.setPixmap(laserPixmap)
        laserLabel.setGeometry(startX, startY, config.IMAGE_WIDTH, config.IMAGE_HEIGHT)
        laserLabel.show()

        self.moveLaser.add_label(laserLabel)

    def move_laser_up(self, laserLabel: QLabel, newX, newY):
        if newY > 0:
            laserLabel.move(newX, newY)
        else:
            laserLabel.hide()

    def __update_position__(self, key):
        playerPos = self.playerLabel.geometry()

        if key == Qt.Key_D:
            if self.try_move_player(playerPos.x() + self.playerSpeed):
                self.playerLabel.setGeometry(playerPos.x() + self.playerSpeed, playerPos.y(), playerPos.width(), playerPos.height())
        elif key == Qt.Key_A:
            if self.try_move_player(playerPos.x() - self.playerSpeed):
                self.playerLabel.setGeometry(playerPos.x() - self.playerSpeed, playerPos.y(), playerPos.width(), playerPos.height())
        elif key == Qt.Key_Space:
            if self.player.lives > 0:
                self.player_shoot_laser(playerPos.x() + config.IMAGE_WIDTH//2, playerPos.y() - config.IMAGE_HEIGHT)
