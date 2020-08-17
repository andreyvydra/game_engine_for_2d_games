import pygame
import math
from settings import *

vec = pygame.math.Vector2


class Someone(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, hp, hit_box, *groups):
        pygame.sprite.Sprite.__init__(self)

        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.original_image = pygame.image.load(img)
        self.image = self.original_image
        self.rect = self.original_image.get_rect()
        self.hit_box = hit_box.copy()

        self.hit_box.center = self.rect.center
        self.rect.center = self.pos
        self.rot = 0
        self.hp = hp
        self.game = game
        # self.last_shot = 0
        # self.hp = 100
        for group in groups:
            group.add(self)

    def transform_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.rot)

    def get_damage(self, damage):
        self.hp -= damage
        self.check_health()

    def check_health(self):
        if self.hp <= 0:
            self.kill()

    def collide_with_objects(self, direction, objects):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, objects, False, lambda x, y: x.hit_box.colliderect(y.rect))
            if hits:
                if hits[0].rect.centerx > self.hit_box.centerx:
                    self.pos.x = hits[0].rect.left - self.hit_box.width / 2
                if hits[0].rect.centerx < self.hit_box.centerx:
                    self.pos.x = hits[0].rect.right + self.hit_box.width / 2
                self.vel.x = 0
                self.hit_box.centerx = self.pos.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, objects, False, lambda x, y: x.hit_box.colliderect(y.rect))
            if hits:
                if hits[0].rect.centery > self.hit_box.centery:
                    self.pos.y = hits[0].rect.top - self.hit_box.height / 2
                if hits[0].rect.centery < self.hit_box.centery:
                    self.pos.y = hits[0].rect.bottom + self.hit_box.height / 2
                self.vel.y = 0
                self.hit_box.centery = self.pos.y

class Player(Someone):
    def __init__(self, game, x, y, img, hp, hit_box, *groups):
        super().__init__(game, x, y, img, hp, hit_box, *groups)
        self.last_shot = 0

    def get_direction_and_make_shot(self):
        keys = pygame.key.get_pressed()
        change_vector = vec(0, 0)
        if keys[pygame.K_w]:
            change_vector.y = -PLAYER_SPEED
            self.rot = 90
        if keys[pygame.K_s]:
            change_vector.y = PLAYER_SPEED
            self.rot = 270
        if keys[pygame.K_a]:
            change_vector.x = -PLAYER_SPEED
            self.rot = 180
        if keys[pygame.K_d]:
            change_vector.x = PLAYER_SPEED
            self.rot = 0
        if change_vector.x and change_vector.y:
            change_vector *= DIAGONAL_COEFFICIENT
            if change_vector.x == change_vector.y:
                self.rot = -45 if abs(change_vector.x) == change_vector.x else -225
            else:
                self.rot = -315 if abs(change_vector.x) == change_vector.x else -135
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.last_shot > CALL_DOWN_SHOT:
                self.last_shot = now
                if self.rot in [270, 90]:
                    rot = self.rot - 90
                elif self.rot in [0, 180]:
                    rot = self.rot + 90
                elif self.rot in [-135, -315]:
                    rot = self.rot
                else:
                    rot = self.rot + 180
                dir = vec(1, 0).rotate(rot)
                pos = self.pos + vec(30, 10).rotate(-self.rot)
                Bullet(self.game, pos, dir, self.game.all_sprites, self.game.bullets)
        return change_vector

    def update(self):
        self.check_health()
        self.vel = self.get_direction_and_make_shot()
        self.transform_image()
        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_box.centerx = self.pos.x
        self.collide_with_objects("x", self.game.walls)
        self.hit_box.centery = self.pos.y
        self.collide_with_objects("y", self.game.walls)
        self.rect.center = self.hit_box.center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, 4))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.game = game
        self.rect.center = self.pos
        self.spawn_time = pygame.time.get_ticks()
        self.vel = vec(direction).rotate(-90) * BULLET_SPEED
        for group in groups:
            group.add(self)

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        hits = pygame.sprite.spritecollide(self, self.game.mobs, False)
        if hits:
            for hit in hits:
                hit.kill()
                self.kill()
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, img, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        for group in groups:
            group.add(self)


class Mob(Someone):
    def __init__(self, game, x, y, img, hp, hit_box, *groups):
        super().__init__(game, x, y, img, hp, hit_box, *groups)

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.transform_image()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot) + self.vel * - 1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_box.centerx = self.pos.x
        self.collide_with_objects("x", self.game.walls)
        self.hit_box.centery = self.pos.y
        self.collide_with_objects("y", self.game.walls)
        self.rect.center = self.hit_box.center
        self.game.player.get_damage(0.5 if pygame.sprite.spritecollide(self.game.player, self.game.mobs, False) else 0)
