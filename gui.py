from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QStackedWidget, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
import game
import config
import sys


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainMenuWidget = MainMenu()
        self.menu()

        self.setWindowTitle('Galaga')
        self.setWindowIcon(QIcon('images/ship.png'))
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def menu(self):
        self.mainMenuWidget.playGameSignal.connect(self.play)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)

        self.centralWidget.addWidget(self.mainMenuWidget)
        self.centralWidget.setCurrentWidget(self.mainMenuWidget)

        self.resize(240, 250)
        self.center()

    def play(self):
        self.resize(config.BOARD_WIDTH * config.TILE_WIDTH, config.BOARD_HEIGHT * config.TILE_HEIGHT)
        self.center()
        self.game = game.Game(2)
        self.setCentralWidget(self.game)

    def quit(self):
        sys.exit()

    def closeEvent(self, event):
        print('Stopping all threads')
        self.game.shouldEnemyMove = False
        self.game.shouldEnemyHitPlayer = False
        self.game.shouldEnemyShoot = False
        self.game.souldNextLevel = False
        sys.exit()


class MainMenu(QWidget):

    playGameSignal = pyqtSignal()
    quitGameSignal = pyqtSignal()

    def __init__(self):
        super(MainMenu, self).__init__()

        button_width = 190
        button_height = 50
        button_offset = 25

        play_button = QPushButton('Play', self)
        play_button.setFixedWidth(button_width)
        play_button.setFixedHeight(button_height)
        play_button.move(button_offset, (button_offset * 1) + (button_height * 0))
        play_button.clicked.connect(self.play)

        quit_button = QPushButton('Quit', self)
        quit_button.setFixedWidth(button_width)
        quit_button.setFixedHeight(button_height)
        quit_button.move(button_offset, (button_offset * 3) + (button_height * 2))
        quit_button.clicked.connect(self.quit)

        self.show()

    def play(self):
        self.playGameSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()