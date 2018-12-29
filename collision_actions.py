from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QLabel
from time import sleep
import config


class LaserEnemyCollision(QObject):
    # Prva QLabel-a je enemy a druga laser koji je pogodio enemy-a
    collision_detected = pyqtSignal(QLabel, QLabel)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.enemies = []
        self.laserLabels = []

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
        self.laserLabels.append(laserLabel)

    def remove_laser(self, laserLabel: QLabel):
        self.laserLabels.remove(laserLabel)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    def __work__(self):
        while self.threadWorking:
            try:
                # Get x, y
                collided = False
                for enemy in self.enemies:
                    if collided:
                        print('Collided = True')
                        break

                    enemyGeo = enemy.geometry()
                    enemyXStart = enemyGeo.x()
                    enemyXEnd = enemyGeo.x() + config.IMAGE_WIDTH
                    enemyY = enemyGeo.y() + config.IMAGE_HEIGHT

                    for laser in self.laserLabels:
                        laserGeo = laser.geometry()
                        laserXStart = laserGeo.x()
                        laserXEnd = laserGeo.x() + laserGeo.width()
                        laserX = laserXStart + ((laserXEnd - laserXStart) // 2)
                        laserY = laserGeo.y() + laserGeo.height()

                        # Check for collision
                        xIsEqual = False
                        yIsEqual = False

                        if enemyXStart <= laserX <= enemyXEnd:
                            xIsEqual = True

                        if laserY == enemyY:
                            yIsEqual = True

                        if xIsEqual and yIsEqual:
                            print('Collision detected')
                            self.remove_enemy(enemy)
                            self.remove_laser(laser)
                            self.collision_detected.emit(enemy, laser)
                            collided = True
                            break
                sleep(0.05)
            except Exception as e:
                print('Exception in LaserEnemy_Collision_Thread: ', str(e))
