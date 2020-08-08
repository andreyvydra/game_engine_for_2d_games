from pygame import sprite, Rect, Surface
from settings import *


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.size = SIZE_TILE
        self.rect = Rect(x, y, self.size, self.size)
        self.image = Surface((SIZE_TILE, SIZE_TILE))
        self.image.fill((255, 255, 255))

    def move(self, move_set):
        self.rect.x += move_set[0]
        self.rect.y += move_set[1]
