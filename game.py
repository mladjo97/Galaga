from PyQt5.QtWidgets import QWidget, qApp
import board


class Game(QWidget):

    def __init__(self, players):
        super(Game, self).__init__()

        self.players = players
        self.board = board.Board()
