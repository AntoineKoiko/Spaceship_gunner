import pygame as pg

BULLET_VELOCITY = 7
BULLET_WIDTH = 10
BULLET_HEIGHT = 5

class Bullet(pg.Rect):
    speed = BULLET_VELOCITY
    width = BULLET_WIDTH
    height = BULLET_HEIGHT

    def __init__(self, x, y, direction):
        super().__init__(x, y, Bullet.width, Bullet.height)
        self.direction = direction

    def draw(self, win, color):
        pg.draw.rect(win, color, self)

    def move(self):
        if self.direction is "right":
            self.x += self.speed
        else:
            self.x -= self.speed
