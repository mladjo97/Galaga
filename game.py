from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import config
from time import sleep
from threading import Thread, Lock
from player_actions import MoveLaser
from player import Player
from enemy_actions import MoveEnemy
from collision_actions import LaserEnemyCollision


class Game(QWidget):

    def __init__(self, players):
        super().__init__()

        # MoveLaser thread
        self.moveLaser = MoveLaser()
        self.moveLaser.calc_done.connect(self.move_laser_up)
        self.moveLaser.start()

        # MoveEnemy thread
        self.moveEnemy = MoveEnemy()
        self.moveEnemy.calc_done.connect(self.move_enemy)
        self.moveEnemy.start()

        # LaserEnemyCollision
        self.laserEnemyCollision = LaserEnemyCollision()
        self.laserEnemyCollision.collision_detected.connect(self.player_laser_enemy_collide)
        self.laserEnemyCollision.start()

        # Gameplay options
        self.activePlayers = players
        self.playerSpeed = config.PLAYER_SPEED

        # Add player one
        self.playerPixmap = QPixmap('images/ship.png')
        self.playerLabel = QLabel(self)
        self.player = Player(0, 0)

        # Set enemy pixmaps
        self.enemyPixmap = QPixmap('images/enemy.png')
        self.enemyPixmap = self.enemyPixmap.scaledToWidth(config.IMAGE_WIDTH - 20)
        self.enemyPixmap = self.enemyPixmap.scaledToHeight(config.IMAGE_HEIGHT - 20)

        self.__init_ui__()

    def __init_ui__(self):
        # Set player start position
        self.playerLabel.setPixmap(self.playerPixmap)
        playerLabelX = config.BOARD_WIDTH // 2 - config.IMAGE_WIDTH
        playerLabelY = config.BOARD_HEIGHT - config.IMAGE_HEIGHT
        self.playerLabel.setGeometry(playerLabelX, playerLabelY, config.IMAGE_WIDTH, config.IMAGE_HEIGHT)

        # Set enemy start positions
        self.enemyLabels = []

        for i in range(3):
            for j in range(10):
                enemyLabel = QLabel(self)
                enemyLabel.setPixmap(self.enemyPixmap)
                positionX = config.IMAGE_WIDTH * (j+3)
                positionY = config.IMAGE_WIDTH * (i+1)
                enemyLabel.setGeometry(positionX, positionY, config.IMAGE_WIDTH, config.IMAGE_HEIGHT)
                enemyLabel.show()
                self.enemyLabels.append(enemyLabel)

        self.activate_enemy_threads()

    def activate_enemy_threads(self):
        for i in range(len(self.enemyLabels)):
            self.moveEnemy.add_enemy(self.enemyLabels[i])
            self.laserEnemyCollision.add_enemy(self.enemyLabels[i])

    def move_enemy(self, enemyLabel: QLabel, newX, newY):
        enemyLabel.move(newX, newY)

    def player_laser_enemy_collide(self, enemyLabel: QLabel, laserLabel: QLabel):
        try:
            enemyLabel.hide()
            laserLabel.hide()
            self.enemyLabels.remove(enemyLabel)
            self.moveEnemy.remove_enemy(enemyLabel)
            self.moveLaser.remove_label(laserLabel)
        except Exception as e:
            print('Exception in Main_Thread/player_laser_enemy_collide method: ', str(e))

    def try_move_player(self, x):
        if (x > (config.BOARD_WIDTH - config.IMAGE_WIDTH)) or (x < 0):
            return False
        return True

    def player_shoot_laser(self, startX, startY):
        laserPixmap = QPixmap('images/laser.png')
        laserLabel = QLabel(self)

        laserLabel.setPixmap(laserPixmap)
        laserLabel.setGeometry(startX, startY, config.IMAGE_WIDTH, config.IMAGE_HEIGHT)
        laserLabel.show()

        self.moveLaser.add_label(laserLabel)
        self.laserEnemyCollision.add_laser(laserLabel)

    def move_laser_up(self, laserLabel: QLabel, newX, newY):
        if newY > 0:
            laserLabel.move(newX, newY)
        else:
            laserLabel.hide()
            self.laserEnemyCollision.remove_laser(laserLabel)

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
