from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QLabel
from time import sleep
import numpy as np
import config
from random import randint


class MoveEnemy(QObject):
    calc_done = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.enemies = []
        self.goLeft = True
        self.goRight = False

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_enemy(self, enemyLabel: QLabel):
        self.enemies.append(enemyLabel)

    def remove_enemy(self, enemyLabel: QLabel):
        self.enemies.remove(enemyLabel)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    def __work__(self):
        while self.threadWorking:
            try:
                # movement logic
                if self.goLeft:
                    for enemy in self.enemies:
                        enemyGeo = enemy.geometry()
                        enemyX = enemyGeo.x()
                        enemyY = enemyGeo.y()
                        if enemyX > 0:
                            self.goLeft = True
                            self.goRight = False
                            self.calc_done.emit(enemy, enemyX - 10, enemyY)
                        else:
                            self.goLeft = False
                            self.goRight = True
                            break
                    sleep(config.ENEMY_MOVE_SLEEP)

                elif self.goRight:
                    for enemy in reversed(self.enemies):
                        enemyGeo = enemy.geometry()
                        enemyX = enemyGeo.x()
                        enemyY = enemyGeo.y()

                        if enemyX < config.BOARD_WIDTH - config.IMAGE_WIDTH:
                            self.goRight = True
                            self.goLeft = False
                            self.calc_done.emit(enemy, enemyX + 10, enemyY)
                        else:
                            self.goRight = False
                            self.goLeft = True
                            break
                    sleep(config.ENEMY_MOVE_SLEEP)
            except Exception as e:
                print('Exception in MoveEnemy_Thread: ', str(e))


class EnemyShoot(QObject):
    can_shoot = pyqtSignal(int, int)
    move_down = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.enemies = []
        self.lasers = []

        self.shootingTimer = config.ENEMY_SHOOT_TIMER

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_enemy(self, enemyLabel: QLabel):
        self.enemies.append(enemyLabel)

    def remove_enemy(self, enemyLabel: QLabel):
        self.enemies.remove(enemyLabel)

    def add_laser(self, laserLabel: QLabel):
        self.lasers.append(laserLabel)

    def remove_laser(self, laserLabel: QLabel):
        self.lasers.remove(laserLabel)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    def find_ymax(self):
        if len(self.enemies) > 0:
            enemy = self.enemies[0]
            enemyGeo = enemy.geometry()
            yMax = enemyGeo.y()
            for i in range(1, len(self.enemies)):
                enemy = self.enemies[i]
                enemyGeo = enemy.geometry()
                y = enemyGeo.y()
                if yMax < y:
                    yMax = y
            return yMax

    def get_enemies_from_y(self, yParam):
        result = []
        if len(self.enemies) > 0:
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]
                enemyGeo = enemy.geometry()
                y = enemyGeo.y()
                if y == yParam:
                    result.append(enemy)
        return result

    def __work__(self):
        while self.threadWorking:
            # Timer for shooting
            if (self.shootingTimer - 0.1) > 0:
                self.shootingTimer -= 0.05
            else:
                self.shootingTimer = 0

            try:
                if self.shootingTimer == 0:
                    # CHOOSE A SHOOTER
                    yMax = self.find_ymax()
                    lowestRowEnemies = self.get_enemies_from_y(yMax)
                    print('Enemy count in lowestRowEnemies: ', len(lowestRowEnemies))

                    if len(lowestRowEnemies) == 10:
                        # Posto ih imamo 10, mozemo ih sve uzeti i jedan od njih ce da puca
                        randIndex = randint(0, 9)
                        enemy = lowestRowEnemies[randIndex]
                        enemyGeo = enemy.geometry()
                        laserX = enemyGeo.x() + (config.IMAGE_WIDTH // 2)
                        laserY = enemyGeo.y() + config.IMAGE_HEIGHT
                        self.can_shoot.emit(laserX, laserY)
                        self.shootingTimer = config.ENEMY_SHOOT_TIMER

                    elif len(lowestRowEnemies) < 10:
                        print('Imamo manje od 10, moramo jos traziti')
                        # TO DO:
                        # Posto ih imamo manje od 10, moramo uzeti sledeci yMax nakon ovog
                        # i osigurati da im se X ne poklapa jer nema 'friendly-fire'
                    else:
                        print('Okej, nesto ovde ne radi ...')

                # MOVE LASER DOWN
                if len(self.lasers) > 0:
                    for laser in self.lasers:
                        laserGeo = laser.geometry()
                        x = laserGeo.x()
                        newY = laserGeo.y() + config.ENEMY_LASER_SPEED
                        self.move_down.emit(laser, x, newY)

                sleep(0.05)
            except Exception as e:
                print('Exception in EnemyShoot_Thread: ', str(e))
