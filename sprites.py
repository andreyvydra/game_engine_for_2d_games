import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.size = SIZE_TILE
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.image = pygame.Surface((SIZE_TILE, SIZE_TILE))
        self.game = game
        self.image.fill(WHITE)
        for group in groups:
            group.add(self)

    def get_change_direction(self):
        keys = pygame.key.get_pressed()
        x, y = 0, 0
        if keys[pygame.K_w]:
            y = -PLAYER_SPEED
        if keys[pygame.K_s]:
            y = PLAYER_SPEED
        if keys[pygame.K_a]:
            x = -PLAYER_SPEED
        if keys[pygame.K_d]:
            x = PLAYER_SPEED
        if x and y:
            x, y = x * DIAGONAL_COEFFICIENT, y * DIAGONAL_COEFFICIENT
        return x, y

    def update(self):
        x, y = self.get_change_direction()
        self.rect.x = self.collide_with_objects("x", x, self.game.walls)
        self.rect.y = self.collide_with_objects("y", y, self.game.walls)

    def collide_with_objects(self, direction, move, objects):
        if direction == "x":
            self.rect.x += move * self.game.dt
            hits = pygame.sprite.spritecollide(self, objects, False)
            if hits:
                return hits[0].rect.left - self.rect.width if move > 0 else hits[0].rect.right
            return self.rect.x
        if direction == "y":
            self.rect.y += move * self.game.dt
            hits = pygame.sprite.spritecollide(self, objects, False)
            if hits:
                return hits[0].rect.top - self.rect.height if move > 0 else hits[0].rect.bottom
            return self.rect.y


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.size = SIZE_TILE
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.image = pygame.Surface((SIZE_TILE, SIZE_TILE))
        self.image.fill(GRAY)
        for group in groups:
            group.add(self)
