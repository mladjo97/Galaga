import board
from PyQt5.QtCore import Qt, QEvent
from PyQt5.Qt import QTimer
from PyQt5.QtWidgets import QWidget, qApp
from PyQt5.QtGui import QPainter, QPixmap
import config
from time import sleep
from threading import Thread
import random


class Game(QWidget):

    def __init__(self, players):
        super(Game, self).__init__()
        qApp.installEventFilter(self)
        self.released = True

        self.enemiesLeft = 30
        self.players = players
        self.board = board.Board()

        # initial movement side for enemy
        self.enemyGoLeft = True
        self.enemyGoRight = False

        self.drawBoardTimer = QTimer()
        self.drawBoardTimer.setInterval(config.GAME_SPEED)
        self.drawBoardTimer.timeout.connect(self.repaint)
        self.drawBoardTimer.start()

        self.enemyCountTimer = QTimer()
        self.enemyCountTimer.setInterval(config.GAME_SPEED)
        self.enemyCountTimer.timeout.connect(self.count_enemies)
        self.enemyCountTimer.start()

        Thread(target=self.enemy_movement_ai, name="Enemy_Movement_Thread").start()
        Thread(target=self.enemy_shooting_ai, name="Enemy_Shooting_Thread").start()
        Thread(target=self.enemy_hit_player, name="Enemy_HitPlayer_Thread").start()

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

    def count_enemies(self):
        count = 0
        for x in range(config.BOARD_WIDTH):
            for y in range(config.BOARD_HEIGHT):
                if self.board.tiles[x, y] == config.TILE_ENEMY:
                    count += 1
        self.enemiesLeft = count

    def update_lives(self):
        if self.board.player.lives == 3:
            self.board.tiles[1, 0] = config.TILE_THREELIVES
        elif self.board.player.lives == 2:
            self.board.tiles[1, 0] = config.TILE_TWOLIVES
        elif self.board.player.lives == 1:
            self.board.tiles[1, 0] = config.TILE_ONELIFE
        else:
            self.board.tiles[1, 0] = config.TILE_ZEROLIVES

    def enemy_movement_ai(self):
        enemySpritesHeight = 4      # for slight optimization only
        while True:
            if self.enemiesLeft == 0:
                break
            # determine movement side
            for y in range(enemySpritesHeight):
                if self.board.tiles[0, y - 1] == config.TILE_ENEMY:
                    if self.enemyGoLeft and not self.enemyGoRight:
                        self.enemyGoLeft = False
                        self.enemyGoRight = True
                if self.board.tiles[config.BOARD_WIDTH - 1, y - 1] == config.TILE_ENEMY:
                    if self.enemyGoRight and not self.enemyGoLeft:
                        self.enemyGoRight = False
                        self.enemyGoLeft = True

            # move left
            if self.enemyGoLeft:
                for x in range(config.BOARD_WIDTH):
                    for y in range(enemySpritesHeight):
                        if self.board.tiles[x, y] == config.TILE_ENEMY:
                                self.board.tiles[x-1, y] = self.board.tiles[x, y]
                                if not x == config.BOARD_WIDTH-1:
                                    if not self.board.tiles[x+1, y] == config.TILE_PLAYERLASER \
                                            and not self.board.tiles[x+1, y] == config.TILE_PLAYERLASER:
                                        self.board.tiles[x, y] = self.board.tiles[x+1, y]
                                    else:
                                        self.board.tiles[x, y] = config.TILE_BACKGROUND
                                else:
                                    self.board.tiles[x, y] = config.TILE_BACKGROUND
            # move right
            if self.enemyGoRight:
                for x in reversed(range(config.BOARD_WIDTH)):
                    for y in reversed(range(enemySpritesHeight)):
                        if self.board.tiles[x, y] == config.TILE_ENEMY:
                            self.board.tiles[x+1, y] = self.board.tiles[x, y]
                            if not x == 0:
                                if not self.board.tiles[x - 1, y] == config.TILE_PLAYERLASER \
                                        and not self.board.tiles[x - 1, y] == config.TILE_PLAYERLASER:
                                    self.board.tiles[x, y] = self.board.tiles[x - 1, y]
                                else:
                                    self.board.tiles[x, y] = config.TILE_BACKGROUND
                            else:
                                self.board.tiles[x, y] = config.TILE_BACKGROUND
            sleep(0.5)

    def enemy_shooting_ai(self):
        # FIX: Ako je ispod drugi Enemy, nemoj pucati, nadji drugog
        sleep(2)
        enemySpritesHeight = 4  # for slight optimization only
        while True:
            print('Enemies left: {}'.format(self.enemiesLeft))
            if self.enemiesLeft == 0:
                continue

            enemyLastRow = 0
            enemyXPositions = []

            # Find the last row where an enemy is and count how many enemies are in that row
            for x in range(config.BOARD_WIDTH):
                if enemyLastRow == 0:
                    for y in (range(enemySpritesHeight)):
                        if self.board.tiles[x, y] == config.TILE_ENEMY:
                            if enemyLastRow < y:
                                enemyLastRow = y

                if not enemyLastRow == 0:
                    if self.board.tiles[x, enemyLastRow] == config.TILE_ENEMY:
                        enemyXPositions.append(x)

            if not enemyLastRow == 0:
                # Randomly choose which enemy fires the shot
                enemyPositionY = enemyLastRow
                enemyFirstX = self.get_first_enemy_X(enemyPositionY)
                enemyXPositions = self.fix_enemy_positions(enemyXPositions, enemyFirstX)
                enemyPositionX = enemyXPositions[random.randint(0, len(enemyXPositions) - 1)]
                self.enemy_shoot_laser(enemyPositionX, enemyPositionY)
                sleep(random.randint(1, 3))

    def fix_enemy_positions(self, array, newPosition):
        newArray = array
        if not newArray[0] == newPosition:
            diff = newPosition - newArray[0]
            for i in range(len(newArray)):
                newArray[i] += diff
        return newArray

    def get_first_enemy_X(self, y):
        for x in range(config.BOARD_WIDTH):
            if self.board.tiles[x, y] == config.TILE_ENEMY:
                return x

    def enemy_shoot_laser(self, x, y):
        laserX = x
        laserY = y + 1
        hitPlayer = False
        # ignore double instance
        if not self.board.tiles[laserX, laserY] == config.TILE_ENEMYLASER:
            self.board.tiles[laserX, laserY] = config.TILE_ENEMYLASER

        # Keep moving the laser down
        while laserY < config.BOARD_HEIGHT - 1:
            laserY += 1
            if not self.board.tiles[laserX, laserY] == config.TILE_PLAYER:
                self.board.tiles[laserX, laserY] = config.TILE_ENEMYLASER
                self.board.tiles[laserX, laserY - 1] = config.TILE_BACKGROUND
            else:
                self.board.tiles[laserX, laserY - 1] = config.TILE_BACKGROUND
                self.board.player.lower_lives()
                hitPlayer = True
                print('Player lives: {}'.format(self.board.player.lives))
                self.update_lives()
                break
            sleep(0.2)

        # when its on last y position
        if not hitPlayer:
            self.board.tiles[laserX, laserY] = config.TILE_BACKGROUND

    def enemy_hit_player(self):
        sleep(5)
        while True:
            enemyPositionY = -1
            playerPositionX = self.board.player.get_x()
            enemySpritesHeight = 4  # for slight optimization only
            hitPlayer = False
            # Find Enemy above Player
            for y in reversed(range(enemySpritesHeight)):
                if self.board.tiles[playerPositionX, y] == config.TILE_ENEMY:
                    enemyPositionY = y
                    # Keep moving the Enemy down
                    while enemyPositionY < config.BOARD_HEIGHT - 1:
                        enemyPositionY += 1
                        # If a laser already hit the Enemy
                        if self.board.tiles[playerPositionX, enemyPositionY - 1] == config.TILE_BACKGROUND:
                            break
                        # If not, just slide the Enemy down
                        if self.board.tiles[playerPositionX, enemyPositionY] == config.TILE_PLAYER:
                            self.board.tiles[playerPositionX, enemyPositionY - 1] = config.TILE_BACKGROUND
                            self.board.player.lower_lives()
                            hitPlayer = True
                            print('Player lives: {}'.format(self.board.player.lives))
                            self.update_lives()
                            break
                        elif self.board.tiles[playerPositionX, enemyPositionY] == config.TILE_PLAYERLASER:
                            self.board.tiles[playerPositionX, enemyPositionY] = config.TILE_BACKGROUND
                            self.board.tiles[playerPositionX, enemyPositionY - 1] = config.TILE_BACKGROUND
                            break
                        else:
                            self.board.tiles[playerPositionX, enemyPositionY] = config.TILE_ENEMY
                            self.board.tiles[playerPositionX, enemyPositionY - 1] = config.TILE_BACKGROUND
                        sleep(0.2)
                    break

            # when its on last y position
            if not hitPlayer and not enemyPositionY == -1:
                self.board.tiles[playerPositionX, enemyPositionY] = config.TILE_BACKGROUND
            sleep(5)

    def move_player(self, x, y):
        # FIX: kad se igrac pomeri na Enemy_Laser onda nestane
        if 0 <= x <= config.BOARD_WIDTH-1 and 8 <= y <= config.BOARD_HEIGHT-1:
            playerX = self.board.player.get_x()
            playerY = self.board.player.get_y()
            if self.board.tiles[playerX, playerY] == config.TILE_PLAYER:
                self.board.tiles[x, y] = self.board.tiles[playerX, playerY]
                self.board.tiles[playerX, playerY] = config.TILE_BACKGROUND
                self.board.player.move(x, y)

    def shoot_laser(self):
        laserX = self.board.player.get_x()
        laserY = self.board.player.get_y() - 1
        # ignore double instance
        if not self.board.tiles[laserX, laserY] == config.TILE_PLAYERLASER:
            self.board.tiles[laserX, laserY] = config.TILE_PLAYERLASER

        # Keep moving the laser up
        while laserY > 0:
            laserY -= 1
            # If a laser hit something already, just quit the loop
            if self.board.tiles[laserX, laserY + 1] == config.TILE_BACKGROUND:
                break
            # Destroy before Lives tiles
            if config.TILE_LIVES <= self.board.tiles[laserX, laserY] <= config.TILE_THREELIVES:
                laserY += 1
                break

            # If not then continue with execution
            if self.board.tiles[laserX, laserY] == config.TILE_ENEMY:
                self.board.tiles[laserX, laserY + 1] = config.TILE_BACKGROUND
                self.board.tiles[laserX, laserY] = config.TILE_BACKGROUND
                break
            else:
                self.board.tiles[laserX, laserY] = config.TILE_PLAYERLASER
                self.board.tiles[laserX, laserY + 1] = config.TILE_BACKGROUND
            sleep(0.1)

        # when its on 0 position
        self.board.tiles[laserX, laserY] = config.TILE_BACKGROUND

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyRelease:
            self.released = True

        if event.type() == QEvent.KeyPress and self.released and self.players != 0:
            self.released = False

            if event.key() == Qt.Key_A:
                self.move_player(self.board.player.get_x() - 1, self.board.player.get_y())
            elif event.key() == Qt.Key_D:
                self.move_player(self.board.player.get_x() + 1, self.board.player.get_y())
            elif event.key() == Qt.Key_W:
                self.move_player(self.board.player.get_x(), self.board.player.get_y() - 1)
            elif event.key() == Qt.Key_S:
                self.move_player(self.board.player.get_x(), self.board.player.get_y() + 1)
            elif event.key() == Qt.Key_Space:
                Thread(target=self.shoot_laser, name="Player_Shooting_Thread").start()

        return super(Game, self).eventFilter(obj, event)
