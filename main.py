import pygame
import sys
from sprites import *
from settings import *



class Game:
    def __init__(self):
        pygame.init()
        self.size = SIZE_WINDOW
        self.window = pygame.display.set_mode(self.size)
        self.main_surface = pygame.Surface(self.size)
        self.main_surface.fill(DEFAULT_COLOR)
        self.dt = 0

    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
<<<<<<< Updated upstream
        self.player = Player(self, 0, 0, self.all_sprites)
        Wall(300, 400, self.all_sprites, self.walls)
        Wall(300, 432, self.all_sprites, self.walls)
        Wall(300, 464, self.all_sprites, self.walls)
=======
        self.player = Player(self, 100, 300, PLAYER_IMG, self.all_sprites)
        self.load_data_map()
>>>>>>> Stashed changes

    def update(self):
        self.all_sprites.update()
        self.main_surface.fill(DEFAULT_COLOR)
        self.all_sprites.draw(self.main_surface)
        self.window.blit(self.main_surface, (0, 0))
        pygame.display.update()
        self.dt = pygame.time.Clock().tick(FPS) / 1000
<<<<<<< Updated upstream
=======
        # print(self.dt)
        # print(self.player.rect.x, self.player.rect.y)
>>>>>>> Stashed changes

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


game = Game()
game.new_game()
while True:
    game.events()
    game.update()

