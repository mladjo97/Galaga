from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QLabel
from time import sleep
import config


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
