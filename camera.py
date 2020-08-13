import pygame
from settings import *


class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.height = height
        self.width = width

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + SIZE_WINDOW[0] // 2
        y = -target.rect.centery + SIZE_WINDOW[1] // 2
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SIZE_WINDOW[0]), x)  # right
        y = max(-(self.height - SIZE_WINDOW[1]), y)  # bottom
        self.camera_rect = pygame.Rect(x, y, self.width, self.height)
