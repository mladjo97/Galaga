from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QLabel
from time import sleep
import config


class ShootLaser(QObject):
    calc_done = pyqtSignal(QLabel, int, int)
    collision_detected = pyqtSignal(QLabel, QLabel)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.laserLabels = []
        self.enemyLabels = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_laser(self, laserLabel: QLabel):
        self.laserLabels.append(laserLabel)

    def remove_laser(self, laserLabel: QLabel):
        self.laserLabels.remove(laserLabel)

    def add_enemy(self, enemyLabel: QLabel):
        self.enemyLabels.append(enemyLabel)

    def remove_enemy(self, enemyLabel: QLabel):
        self.enemyLabels.remove(enemyLabel)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    def __work__(self):
        while self.threadWorking:
            try:
                collided = False
                # COLLISION
                for enemy in self.enemyLabels:
                    if collided:
                        break

                    # Get enemy geometry
                    enemyGeo = enemy.geometry()
                    enemyXStart = enemyGeo.x()
                    enemyXEnd = enemyGeo.x() + config.IMAGE_WIDTH
                    enemyY = enemyGeo.y() + config.IMAGE_HEIGHT

                    for laser in self.laserLabels:
                        # get laser geometry
                        laserGeo = laser.geometry()
                        laserXStart = laserGeo.x()
                        laserXEnd = laserGeo.x() + laserGeo.width()
                        laserX = laserXStart + ((laserXEnd - laserXStart) // 2)
                        laserY = laserGeo.y()

                        # Check for collision
                        xIsEqual = False
                        yIsEqual = False

                        if enemyXStart <= laserX <= enemyXEnd:
                            xIsEqual = True

                        if laserY == enemyY:
                            yIsEqual = True
                        if xIsEqual and yIsEqual:
                            print('Collision detected for y: {} {}'.format(enemyY, laserY))
                            self.remove_enemy(enemy)
                            self.remove_laser(laser)
                            self.collision_detected.emit(enemy, laser)
                            collided = True
                            break

                # MOVE LABELS UP
                for label in self.laserLabels:
                    laserGeo = label.geometry()
                    laserX = laserGeo.x()
                    laserY = laserGeo.y() - config.PLAYER_LASER_SPEED
                    if laserY > 0:
                        self.calc_done.emit(label, laserX, laserY)
                    elif laserY == 0:
                        self.calc_done.emit(label, laserX, laserY)
                        self.laserLabels.remove(label)

                sleep(0.05)
            except Exception as e:
                print('Exception in ShootLaser_Thread: ', str(e))
