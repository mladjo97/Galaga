class Player:
    def __init__(self):
        self.lives = 3

    def lower_lives(self):
        if self.lives > 0:
            self.lives -= 1

    def get_lives(self):
        return self.lives

    def reset_lives(self):
        self.lives = 3
