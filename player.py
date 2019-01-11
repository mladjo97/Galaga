from PyQt5.QtWidgets import QLabel

class Player:
    def __init__(self, playerLabelParam: QLabel):
        self.lives = 3
        self.playerLabel = playerLabelParam

    def lower_lives(self):
        if self.lives > 0:
            self.lives -= 1

    def get_lives(self):
        return self.lives

    def reset_lives(self):
        self.lives = 3
