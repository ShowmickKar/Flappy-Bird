import pygame, random


class Base:
    def __init__(self, WIDTH, HEIGHT, x=0, y=900):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(
            pygame.image.load("Assets/Base.png"), (1400, 120)
        )

    def move(self, weight=2):
        self.x -= weight

    def display(self, window):
        if self.x <= -700:
            self.x = 0
        window.blit(self.img, (self.x, 900))