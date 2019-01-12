from PyQt5.QtCore import pyqtSignal, QThread, QObject
from time import sleep
from PyQt5.QtWidgets import QLabel
from time import time
import config


class DeusExMachina(QObject):
    collision_detected = pyqtSignal(QLabel, QLabel)
    powerup_timeout = pyqtSignal(QLabel)

    def __init__(self):
        super().__init__()

        self.threadWorking = True

        self.playerLabels = []
        self.powerUpLabels = []

        self.powerUpTime = time()

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    def add_player(self, playerLabel: QLabel):
        self.playerLabels.append(playerLabel)

    def remove_player(self, playerLabel: QLabel):
        if playerLabel in self.playerLabels:
            self.playerLabels.remove(playerLabel)

    def add_powerup(self, powerUpLabel: QLabel):
        self.powerUpLabels.append(powerUpLabel)
        self.powerUpTime = time()
        print('Power up time in ADD: ', self.powerUpTime)

    def remove_powerup(self, powerUpLabel: QLabel):
        if powerUpLabel in self.powerUpLabels:
            self.powerUpLabels.remove(powerUpLabel)

    def __work__(self):
        while self.threadWorking:
            try:
                #print("len of powerup: ", len(self.powerUpLabels))
                #print('len of players: ', len(self.playerLabels))

                currentTime = time()
                #print('Current time: ', currentTime)

                if len(self.powerUpLabels) > 0:
                    if currentTime - self.powerUpTime > 2:
                        print('DVE SEKUNDE PROSLE')
                        for powerUpLabel in self.powerUpLabels:
                            self.powerUpLabels.remove(powerUpLabel)
                            self.powerup_timeout.emit(powerUpLabel)

                for playerLabel in self.playerLabels:
                    playerLabelGeo = playerLabel.geometry()
                    playerLabelXStart = playerLabelGeo.x()
                    playerLabelXEnd = playerLabelGeo.x() + config.IMAGE_WIDTH
                    playerLabelXArray = range(playerLabelXStart, playerLabelXEnd)

                    # check for collision with player
                    for powerupLabel in self.powerUpLabels:
                        powerupLabelGeo = powerupLabel.geometry()
                        powerupLabelXStart = powerupLabelGeo.x()
                        powerupLabelXEnd = powerupLabelGeo.x() + config.IMAGE_WIDTH
                        powerupLabelXArray = range(powerupLabelXStart, powerupLabelXEnd)

                        # detect collision
                        for playerLabelX in playerLabelXArray:
                            if playerLabelX in powerupLabelXArray:
                                print('uzeo power up')
                                self.remove_powerup(powerupLabel)
                                self.collision_detected.emit(powerupLabel, playerLabel)
                                break

                sleep(0.05)
            except Exception as e:
                print('Exception in PowerUp_Thread: ', str(e))