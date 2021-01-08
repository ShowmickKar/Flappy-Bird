import pygame, random


RED = (255, 0, 0)


class Bird:
    def __init__(self, WIDTH, HEIGHT, x=50, y=450, radius=20):
        self.radius = radius
        self.color = RED
        self.x = x
        self.y = y
        self.width = WIDTH
        self.height = HEIGHT
        self.image = pygame.transform.scale(
            pygame.image.load("Assets/yellow_bird.png"), (80, 80)
        )
        self.right_facing = True
        self.score = 0
        self.alive = True
        self.gravity = 1.9

    def moveUp(self, draw):
        if self.y >= 0:
            self.y -= 2
            draw()

    def moveDown(self, draw):
        if self.y + 170 <= self.height:
            self.y += 2
            draw()

    def moveRight(self, draw):
        self.right_facing = True
        if self.x + 80 <= self.width:
            self.x += 2
            draw()

    def moveLeft(self, draw):
        self.right_facing = False
        if self.x >= 0:
            self.x -= 2
            draw()

    def jump(self, draw):
        if self.y - 5 >= 0:
            self.y -= 5
            draw()
        self.gravity = 1.9

    def hitGround(self):
        return self.y >= 830

    def hitTop(self):
        return self.y <= 3

    def fall(self):
        if self.y + 170 <= self.height:
            self.y += self.gravity

    def display(self, window):
        if self.right_facing:
            window.blit(self.image, (self.x, self.y))
        else:
            window.blit(
                pygame.transform.flip(self.image, True, False), (self.x, self.y)
            )

    def kill(self):
        self.alive = False
