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

    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(0, 0)
        self.all_sprites.add(self.player)

    def update(self):
        self.main_surface.fill(DEFAULT_COLOR)
        self.all_sprites.draw(self.main_surface)
        self.window.blit(self.main_surface, (0, 0))
        pygame.display.update()

        # Realization with FPS lock for game
        # Just uncomment
        # pygame.time.Clock().tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.move((5, 0))
                if event.key == pygame.K_a:
                    self.player.move((-5, 0))
                if event.key == pygame.K_s:
                    self.player.move((0, 5))
                if event.key == pygame.K_w:
                    self.player.move((0, -5))



game = Game()
game.new_game()
while True:
    game.events()
    game.update()

