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
        self.bullets = pygame.sprite.Group()
        self.map = Map(filename)
        self.map_img = self.map.make_map()
        '''for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'w':
                    Wall(col * SIZE_TILE, row * SIZE_TILE, WALL_IMG, self.all_sprites, self.walls)
                if tile == 'p':
                    self.player = Player(self, col * SIZE_TILE, row * SIZE_TILE, PLAYER_IMG,
                                         100, PLAYER_HIT_BOX, self.all_sprites)
                if tile == "m":
                    Mob(self, col * SIZE_TILE, row * SIZE_TILE, MOB_IMG, 100,
                        MOB_HIT_BOX, self.all_sprites, self.mobs)'''
        self.player = Player(self, 100, 100, PLAYER_IMG, 100, PLAYER_HIT_BOX, self.all_sprites)
        Mob(self, 200, 200, MOB_IMG, 100, MOB_HIT_BOX, self.all_sprites, self.mobs)
        self.camera = Camera(self.map.width, self.map.height)

    def update(self):
        if self.player.hp <= 0:
            self.new_game("f.txt")
        self.all_sprites.update()
        self.camera.update(self.player)
        # self.main_surface.fill(GRAY)
        self.map.render(self.map_img)
        self.window.blit(self.map_img, self.camera.apply_rect(self.map_img.get_rect()))
        # self.main_surface.rect = self.main_surface.get_rect()
        for sprite in self.all_sprites:
            print(sprite.rect.x, sprite.rect.y)
            self.window.blit(sprite.image, self.camera.apply(sprite))
        # self.window.blit(self.map_img, self.camera.apply(self.map))
        pygame.display.update()
        self.dt = pygame.time.Clock().tick(FPS) / 1000
        # pygame.display.set_caption(str(self.dt * 1000))

        # print(self.dt)
        # print(self.player.rect.x, self.player.rect.y)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


game = Game()
game.new_game("maps/map.tmx")
while True:
    game.events()
    game.update()

