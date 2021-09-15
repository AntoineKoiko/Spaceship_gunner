#!/usr/bin/env python3

import pygame as pg
import os
from Ship import RedShip, YellowShip, Ship
import Colors

# Already init in Ship
# pg.font.init()
pg.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("First Game !!")

# custom events
YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

FPS = 60

#BULLET_HIT_SOUND = pg.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
#BULLET_FIRE_SOUND = pg.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

SPACE = pg.transform.scale(pg.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)

BORDER = pg.Rect((WIDTH // 2) - (10 / 2), 0, 10, HEIGHT)


def draw_window(red, yellow):
    WIN.blit(SPACE, (0, 0))

    # draw surface
    pg.draw.rect(WIN, Colors.BLACK, BORDER)

    red.draw_health(WIN, WIDTH)
    yellow.draw_health(WIN, WIDTH)

    red.draw(WIN)
    yellow.draw(WIN)

    red.draw_bullets(WIN)
    yellow.draw_bullets(WIN)

    pg.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pg.K_q] and yellow.x - Ship.speed > 0:  # left
        yellow.x -= Ship.speed
    if keys_pressed[pg.K_d] and yellow.x + Ship.speed + yellow.width - 15 < BORDER.x:  # right
        yellow.x += Ship.speed
    if keys_pressed[pg.K_z] and yellow.y - Ship.speed > 0:  # up
        yellow.y -= Ship.speed
    if keys_pressed[pg.K_s] and yellow.y + Ship.speed + yellow.height < HEIGHT - 15:  # down
        yellow.y += Ship.speed


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pg.K_LEFT] and red.x - Ship.speed > BORDER.x + BORDER.width:  # left
        red.x -= Ship.speed
    if keys_pressed[pg.K_RIGHT] and red.x + Ship.speed + red.width - 15 < WIDTH:  # right
        red.x += Ship.speed
    if keys_pressed[pg.K_UP] and red.y - Ship.speed > 0:  # up
        red.y -= Ship.speed
    if keys_pressed[pg.K_DOWN] and red.y + Ship.speed + red.height < HEIGHT - 15:  # down
        red.y += Ship.speed


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.move()
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.move()
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, Colors.WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pg.display.update()
    pg.time.delay(5000)


def main():
    red = RedShip(700, 300)
    yellow = YellowShip(100, 300)

    winner_text = ""

    clock = pg.time.Clock()
    running = True

    while running:

        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                return

            if event.type == YELLOW_HIT:
                yellow.loose_health()
                #BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red.loose_health()
                #BULLET_HIT_SOUND.play()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and yellow.can_shoot():
                    yellow.shoot()
                    #BULLET_FIRE_SOUND.play()

                if event.key == pg.K_RCTRL and red.can_shoot():
                    red.shoot()
                    #BULLET_FIRE_SOUND.play()

        if red.health <= 0:
            winner_text = "Yellow Wins!"

        if yellow.health <= 0:
            winner_text = "Red winds!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pg.key.get_pressed()
        handle_red_movement(keys_pressed, red)
        handle_yellow_movement(keys_pressed, yellow)
        handle_bullets(yellow.bullets, red.bullets, yellow, red)

        draw_window(red, yellow)

    main()


if __name__ == '__main__':
    main()
