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

    def load_data_map(self):
        for y, row in enumerate(self.map.data):
            for x, col in enumerate(row):
                if col == "w":
                    Wall(x * SIZE_TILE, y * SIZE_TILE, self.all_sprites, self.walls)

    def new_game(self, src):
        self.map = Map(src)
        self.camera = Camera(self.map.width, self.map.height)
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 0, 0, self.all_sprites)
        self.load_data_map()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        self.main_surface.fill(DEFAULT_COLOR)
        for sprite in self.all_sprites:
            self.main_surface.blit(sprite.image, self.camera.apply(sprite))
        self.window.blit(self.main_surface, (0, 0))
        pygame.display.update()
        self.dt = pygame.time.Clock().tick(FPS) / 1000
        print(self.player.rect.x, self.player.rect.y)

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

