from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.Qt import QIcon
import config
import sys


class Galaga(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # initiates application UI
        self.setFixedSize(config.BOARD_WIDTH * config.TILE_WIDTH, config.BOARD_HEIGHT * config.TILE_HEIGHT)
        self.center()

        self.setWindowTitle('Galaga')
        self.setWindowIcon(QIcon('images/ship.png'))
        self.show()

    def center(self):
        # centers the window on the screen
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    galaga = Galaga()
    sys.exit(app.exec_())
