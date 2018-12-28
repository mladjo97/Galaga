from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Game(QWidget):

    def __init__(self, players):
        super(Game, self).__init__()

        self.activePlayers = players

        self.pix1 = QPixmap('images/ship.png')
        self.pix2 = QPixmap('images/ship.png')
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        self.__init_ui__()

    def __init_ui__(self):

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(100, 40, 50, 50)

        self.label2.setPixmap(self.pix2)
        self.label2.setGeometry(10, 40, 50, 50)

    def keyPressEvent(self, e):
        print('KeyPressEvent fired.')
        self.__update_position__(e.key())

    def __update_position__(self, key):
        print('_update_position_')
        rec1 = self.label1.geometry()
        rec2 = self.label2.geometry()

        if key == Qt.Key_Right:
            self.label1.setGeometry(rec1.x() + 5, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Down:
            self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Left:
            self.label1.setGeometry(rec1.x() - 5, rec1.y(), rec1.width(), rec1.height())

        if key == Qt.Key_D:
            self.label2.setGeometry(rec2.x() + 5, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_S:
            self.label2.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
        elif key == Qt.Key_W:
            self.label2.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
        elif key == Qt.Key_A:
            self.label2.setGeometry(rec2.x() - 5, rec2.y(), rec2.width(), rec2.height())

