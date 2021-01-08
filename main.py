import math
import pygame
import random

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 60)

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
RED = (255, 0, 0)
ORANGE = (255, 106, 0)
LIME = (78, 253, 0)
GREEN = (0, 85, 0)
PURPLE = (98, 20, 220)

WIDTH, HEIGHT = 600, 1000

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()


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


def draw(window, bird, floor, pipe):
    window.fill(ORANGE)
    pipe.display(window)
    floor.display(window)
    bird.display(window)
    window.blit(myfont.render(f"SCORE: {bird.score}", False, (0, 0, 0)), (0, 0))
    pygame.display.update()


def reset(window):
    game(window)


def checkCollision(bird, pipe):
    if pipe.x - 50 <= bird.x <= pipe.x + pipe.width - 50:
        if bird.y >= (pipe.height - pipe.lower) - 50 or bird.y <= pipe.upper - 20:
            return True


def updateHighestScore(HIGHEST_SCORE, score):
    HIGHEST_SCORE -= HIGHEST_SCORE
    max(HIGHEST_SCORE, score)


def main(window, bird, floor, pipe):
    run = True
    start = False
    object_frame = 2.5
    while run:
        draw(window, bird, floor, pipe)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        navigation_key = pygame.key.get_pressed()
        if navigation_key[pygame.K_UP]:
            bird.moveUp(lambda: draw(window, bird, floor, pipe))
        if navigation_key[pygame.K_DOWN]:
            bird.moveDown(lambda: draw(window, bird, floor, pipe))
        if navigation_key[pygame.K_RIGHT]:
            bird.moveRight(lambda: draw(window, bird, floor, pipe))
        if navigation_key[pygame.K_LEFT]:
            bird.moveLeft(lambda: draw(window, bird, floor, pipe))
        if navigation_key[pygame.K_SPACE]:
            bird.jump(lambda: draw(window, bird, floor, pipe))
        clock.tick(300)
        bird.fall()
        bird.gravity += 0.005
        if bird.hitGround() or checkCollision(bird, pipe):
            pygame.time.delay(300)
            bird.kill()
            window.fill(RED)
            font = pygame.font.Font("freesansbold.ttf", 50)
            text = font.render(f"SCORE: {bird.score}", True, GREEN, PURPLE)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2)
            window.blit(text, textRect)
            pygame.display.update()
            pygame.time.delay(2000)
            reset(window)
        floor.move(object_frame)
        pipe.move(object_frame)
        if bird.x == pipe.x + pipe.width:
            bird.score += 1

    pygame.quit()


def game(window):
    bird = Bird(WIDTH, HEIGHT)
    floor = Base(WIDTH, HEIGHT)
    pipe = Pipe(WIDTH, HEIGHT)
    draw(window, bird, floor, pipe)
    window.blit(myfont.render("PRESS SPACE TO START", False, RED), (0, 200))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        navigation_key = pygame.key.get_pressed()
        if navigation_key[pygame.K_SPACE]:
            main(window, bird, floor, pipe)
    pygame.quit()


game(window)
