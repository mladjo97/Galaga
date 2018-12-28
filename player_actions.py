from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QLabel
from time import sleep
import config


class MoveLaser(QObject):
    calc_done = pyqtSignal(QLabel, int, int)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.labels = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_label(self, laserLabel: QLabel):
        self.labels.append(laserLabel)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    def __work__(self):
        while self.threadWorking:
            for label in self.labels:
                laserGeo = label.geometry()
                laserX = laserGeo.x()
                laserY = laserGeo.y() - config.PLAYER_LASER_SPEED
                if laserY > 0:
                    self.calc_done.emit(label, laserX, laserY)
                elif laserY == 0:
                    self.calc_done.emit(label, laserX, laserY)
                    self.labels.remove(label)
            sleep(0.05)
