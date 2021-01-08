import pygame, random

GREEN = (0, 85, 0)


class Pipe:
    def __init__(self, WIDTH, HEIGHT, x=1000, y=1300):
        self.x = x
        self.y = y
        self.color = GREEN
        self.height = 900
        self.gap = 200
        self.upper = 400
        self.lower = self.height - self.upper - self.gap
        self.reset()
        self.width = 100

    def reset(self):
        self.x = random.choice([500, 525, 550, 575, 600, 700])
        self.gap = random.choice([150, 175, 200, 225, 250, 275, 300, 325, 350])
        self.upper = random.choice(
            [
                15,
                20,
                40,
                50,
                100,
                150,
                200,
                250,
                300,
                350,
                400,
                450,
                475,
                500,
                525,
                550,
                600,
            ]
        )
        self.lower = self.height - self.upper - self.gap
        if self.lower <= 0:
            self.lower = random.choice([25, 50])

    def move(self, weight=2):
        self.x -= weight

    def display(self, window):
        if self.x <= -700:
            self.reset()

        pygame.draw.rect(window, self.color, (self.x, 0, self.width, self.upper))
        pygame.draw.rect(
            window,
            self.color,
            (self.x, self.height - self.lower, self.width, self.lower),
        )
