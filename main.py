import pygame, random
from pipe import Pipe
from bird import Bird
from base import Base

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
