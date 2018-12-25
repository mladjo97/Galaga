class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lives = 3

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def move(self, x, y):
        self.x = x
        self.y = y

    def lower_lives(self):
        if self.lives > 0:
            self.lives -= 1
