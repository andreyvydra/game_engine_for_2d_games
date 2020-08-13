import pygame
import math
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.size = SIZE_TILE
        self.original_image = pygame.image.load(img)
        self.image = self.original_image
        self.rect = self.original_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        for group in groups:
            group.add(self)

    def change_rotation_image(self, x, y):
        if x and not y:
            if x > 0:
                self.image = pygame.transform.rotate(self.original_image, 0)
            else:
                self.image = pygame.transform.rotate(self.original_image, -180)
        elif y and not x:
            if y > 0:
                self.image = pygame.transform.rotate(self.original_image, -90)
            else:
                self.image = pygame.transform.rotate(self.original_image, -270)
        elif x and y:
            if x == y:
                if abs(x) == x:
                    self.image = pygame.transform.rotate(self.original_image, -45)
                else:
                    self.image = pygame.transform.rotate(self.original_image, -225)
            else:
                if abs(x) == x:
                    self.image = pygame.transform.rotate(self.original_image, -315)
                else:
                    self.image = pygame.transform.rotate(self.original_image, -135)

        # mouse_pos = pygame.mouse.get_pos()
        # self.rot = (180 / math.pi) * math.atan2(mouse_pos[0] - self.rect.centerx,
        #                                        mouse_pos[1] - self.rect.centery)
        # self.image = pygame.transform.rotate(self.original_image, self.rot)
        # print(self.rot)

    def get_direction(self):
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
        x, y = self.get_direction()
        current_x, current_y = self.rect.x, self.rect.y
        self.rect.x = self.collide_with_objects("x", x, self.game.walls)
        self.rect.y = self.collide_with_objects("y", y, self.game.walls)
        self.change_rotation_image(self.rect.x - current_x, self.rect.y - current_y)

    def collide_with_objects(self, direction, move, objects):
        if direction == "x":
            if abs(move) == move and move != 0:
                self.rect.x += move * self.game.dt + 1
            else:
                self.rect.x += move * self.game.dt
            hits = pygame.sprite.spritecollide(self, objects, False)
            if hits:
                return hits[0].rect.left - self.rect.width if move > 0 else hits[0].rect.right
            return self.rect.x
        if direction == "y":
            if abs(move) == move and move != 0:
                self.rect.y += move * self.game.dt + 1
            else:
                self.rect.y += move * self.game.dt
            hits = pygame.sprite.spritecollide(self, objects, False)
            if hits:
                return hits[0].rect.top - self.rect.height if move > 0 else hits[0].rect.bottom
            return self.rect.y


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, img, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        for group in groups:
            group.add(self)


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(img)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.game = game
        for group in groups:
            group.add(self)

    def update(self):
        self.rot = (180 / math.pi) * math.atan2(self.game.player.rect.centerx - self.rect.centerx,
                                                self.game.player.rect.centery - self.rect.centery) - 90
        self.image = pygame.transform.rotate(self.original_image, self.rot)
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
