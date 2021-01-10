import pygame, random
from pipe import Pipe
from bird import Bird
from base import Base
from pygame import mixer

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont("Comic Sans MS", 35)
myfont2 = pygame.font.SysFont("Comic Sans MS", 60)


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


def draw(window, bird, floor, pipe, HIGHEST_SCORE):
    window.fill(ORANGE)
    pipe.display(window)
    floor.display(window)
    bird.display(window)
    window.blit(myfont.render(f"SCORE: {bird.score}", False, (0, 0, 0)), (0, 0))
    window.blit(
        myfont.render(f"HIGHEST SCORE: {HIGHEST_SCORE}", False, (0, 0, 0)), (350, 0)
    )
    pygame.display.update()


def reset(window, HIGHEST_SCORE):
    game(window, HIGHEST_SCORE)


def checkCollision(bird, pipe):
    if pipe.x - 50 <= bird.x <= pipe.x + pipe.width - 50:
        if bird.y >= (pipe.height - pipe.lower) - 50 or bird.y <= pipe.upper - 20:
            return True


HIGHEST_SCORE = 0


def main(window, bird, floor, pipe, HIGHEST_SCORE):
    run = True
    start = False
    object_frame = 2.5
    while run:
        draw(window, bird, floor, pipe, HIGHEST_SCORE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        navigation_key = pygame.key.get_pressed()
        if navigation_key[pygame.K_UP]:
            bird.moveUp(lambda: draw(window, bird, floor, pipe, HIGHEST_SCORE))
        if navigation_key[pygame.K_DOWN]:
            bird.moveDown(lambda: draw(window, bird, floor, pipe, HIGHEST_SCORE))
        if navigation_key[pygame.K_RIGHT]:
            bird.moveRight(lambda: draw(window, bird, floor, pipe, HIGHEST_SCORE))
        if navigation_key[pygame.K_LEFT]:
            bird.moveLeft(lambda: draw(window, bird, floor, pipe, HIGHEST_SCORE))
        if navigation_key[pygame.K_SPACE]:
            bird.jump(lambda: draw(window, bird, floor, pipe, HIGHEST_SCORE))
        clock.tick(300)
        bird.fall()
        bird.gravity += 0.005
        if bird.hitGround() or bird.hitTop() or checkCollision(bird, pipe):
            mixer.music.load("Sounds/Dying-Sound.wav")
            pygame.mixer.music.play()
            HIGHEST_SCORE = max((HIGHEST_SCORE, bird.score))
            pygame.time.delay(300)
            bird.kill()
            window.fill(RED)
            font = pygame.font.Font("freesansbold.ttf", 50)
            text = font.render(f"SCORE: {bird.score}", True, GREEN, PURPLE)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2)
            window.blit(text, textRect)
            window.blit(
                myfont2.render(f"HIGHEST SCORE: {HIGHEST_SCORE}", False, (0, 0, 0)),
                (130, 550),
            )
            pygame.display.update()
            pygame.time.delay(2000)
            reset(window, HIGHEST_SCORE)
        floor.move(object_frame)
        pipe.move(object_frame)
        if bird.x == pipe.x + pipe.width:
            mixer.music.load("Sounds/Coin-Bonus.wav")
            pygame.mixer.music.play()
            bird.score += 1

    pygame.quit()


def game(window, HIGHEST_SCORE):
    bird = Bird(WIDTH, HEIGHT)
    floor = Base(WIDTH, HEIGHT)
    pipe = Pipe(WIDTH, HEIGHT)
    draw(window, bird, floor, pipe, HIGHEST_SCORE)
    window.blit(myfont2.render("PRESS SPACE TO START", False, RED), (0, 200))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        navigation_key = pygame.key.get_pressed()
        if navigation_key[pygame.K_SPACE]:
            main(window, bird, floor, pipe, HIGHEST_SCORE)
    pygame.quit()


game(window, HIGHEST_SCORE)
