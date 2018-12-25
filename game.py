from PyQt5.Qt import QTimer
from PyQt5.QtWidgets import QWidget, qApp
from PyQt5.QtGui import QPainter, QPixmap
from threading import Thread
from time import sleep
import board
import config
import random



class Game(QWidget):

    def __init__(self, players):
        super(Game, self).__init__()

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
        print(self.enemiesLeft)

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
