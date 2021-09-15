#!/usr/bin/env python3
import pygame
import pygame as pg
import os
pg.font.init()
pg.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("First Game !!")

# custom events
YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
MAX_BULLETS = 3
MAX_HEALTH = 5

YELLOW_SPACESHIP_IMG = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pg.transform.rotate(pg.transform.scale(
    YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMG = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pg.transform.rotate(pg.transform.scale(
    RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

#BULLET_HIT_SOUND = pg.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
#BULLET_FIRE_SOUND = pg.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

SPACE = pg.transform.scale(pg.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)

BORDER = pygame.Rect((WIDTH // 2) - (10 / 2), 0, 10, HEIGHT)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))

    # draw surface
    pg.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f'Health: {red_health}', 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f'Health: {yellow_health}', 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pg.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(WIN, YELLOW, bullet)

    pg.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pg.K_q] and yellow.x - VELOCITY > 0:  # left
        yellow.x -= VELOCITY
    if keys_pressed[pg.K_d] and yellow.x + VELOCITY + yellow.width - 15 < BORDER.x:  # right
        yellow.x += VELOCITY
    if keys_pressed[pg.K_z] and yellow.y - VELOCITY > 0:  # up
        yellow.y -= VELOCITY
    if keys_pressed[pg.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:  # down
        yellow.y += VELOCITY


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pg.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:  # left
        red.x -= VELOCITY
    if keys_pressed[pg.K_RIGHT] and red.x + VELOCITY + red.width - 15 < WIDTH:  # right
        red.x += VELOCITY
    if keys_pressed[pg.K_UP] and red.y - VELOCITY > 0:  # up
        red.y -= VELOCITY
    if keys_pressed[pg.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15:  # down
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pg.display.update()
    pg.time.delay(5000)


def main():
    red = pg.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pg.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = MAX_HEALTH
    yellow_health = MAX_HEALTH

    winner_text = ""

    clock = pg.time.Clock()
    running = True

    while running:

        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                return

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                #BULLET_HIT_SOUND.play()


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(yellow.x + yellow.width, yellow.y + (yellow.height // 2) - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pg.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(red.x, red.y + (red.height // 2) - 2, 10, 5)
                    red_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()


        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red winds!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pg.key.get_pressed()
        handle_red_movement(keys_pressed, red)
        handle_yellow_movement(keys_pressed, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == '__main__':
    main()
