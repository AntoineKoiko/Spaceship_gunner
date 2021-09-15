import pygame as pg
import os
from Bullet import Bullet
import Colors
pg.font.init()

HEALTH_FONT = pg.font.SysFont('comicsans', 40)

VELOCITY = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
MAX_BULLETS = 3
MAX_HEALTH = 5

YELLOW_SPACESHIP_IMG = pg.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pg.transform.rotate(pg.transform.scale(
    YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMG = pg.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pg.transform.rotate(pg.transform.scale(
    RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_text(win, text, x, y):
    win.blit(text, (x, y))


class Ship(pg.Rect):
    speed = VELOCITY
    width = SPACESHIP_WIDTH
    height = SPACESHIP_HEIGHT
    max_health = MAX_HEALTH
    max_bullets = MAX_BULLETS

    def __init__(self, x, y, color):
        super().__init__(x, y, Ship.width, Ship.height)
        self.health = Ship.max_health
        self.bullets = []
        self.color = color

    def loose_health(self):
        self.health -= 1

    def draw_bullets(self, win):
        for bullet in self.bullets:
            bullet.draw(win, self.color)

    def get_health_text(self):
        return HEALTH_FONT.render(f'Health: {self.health}', 1, Colors.WHITE)

    def can_shoot(self):
        if len(self.bullets) < Ship.max_bullets:
            return True
        return False

class RedShip(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, Colors.RED)

    def draw(self, win):
        win.blit(RED_SPACESHIP, (self.x, self.y))

    def shoot(self):
        bullet = Bullet(self.x, self.y + (self.height // 2) - 2, "left")
        self.bullets.append(bullet)

    def draw_health(self, win, width):
        health_text = self.get_health_text()
        x = width - health_text.get_width() - 10
        draw_text(win, health_text, x, 10)

class YellowShip(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, Colors.YELLOW)

    def draw(self, win):
        win.blit(YELLOW_SPACESHIP, (self.x, self.y))

    def shoot(self):
        bullet = Bullet(self.x + self.width, self.y + (self.height // 2) - 2, "right")
        self.bullets.append(bullet)

    def draw_health(self, win, width):
        text = self.get_health_text()
        draw_text(win, text, 10, 10)
