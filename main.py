import pygame
import sys
from sprites import *
from settings import *
from map import *
from camera import *


class Game:
    def __init__(self):
        pygame.init()
        self.size = SIZE_WINDOW
        self.window = pygame.display.set_mode(self.size)
        self.main_surface = pygame.Surface(self.size)
        self.main_surface.fill(DEFAULT_COLOR)
        self.dt = 0

    def new_game(self, filename):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.map = Map(filename)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'w':
                    Wall(col * SIZE_TILE, row * SIZE_TILE, WALL_IMG, self.all_sprites, self.walls)
                if tile == 'p':
                    self.player = Player(self, col * SIZE_TILE, row * SIZE_TILE, PLAYER_IMG, self.all_sprites)
                if tile == "m":
                    Mob(self, col * SIZE_TILE, row * SIZE_TILE, MOB_IMG, self.all_sprites, self.mobs)
        self.camera = Camera(self.map.width, self.map.height)

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        self.main_surface.fill(GRAY)
        for sprite in self.all_sprites:
            self.main_surface.blit(sprite.image, self.camera.apply(sprite))
        self.window.blit(self.main_surface, (0, 0))
        pygame.display.update()
        self.dt = pygame.time.Clock().tick(FPS) / 1000

        # print(self.dt)
        # print(self.player.rect.x, self.player.rect.y)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


game = Game()
game.new_game("f.txt")
while True:
    game.events()
    game.update()

