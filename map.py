from settings import *
import pytmx
import pygame


'''class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.width = len(self.data[0]) * SIZE_TILE
        self.height = len(self.data) * SIZE_TILE
'''


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight

    def render(self, surface):
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * SIZE_TILE, y * SIZE_TILE))

    def make_map(self):
        self.map_img = pygame.Surface((self.width, self.height))
        self.render(self.map_img)
        return self.map_img



