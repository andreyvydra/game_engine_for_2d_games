from settings import *
import pygame


class Map:
    def __init__(self, src):
        self.data = []
        with open(src, "rt") as map:
            for line in map:
                self.data.append(line)
        self.width = (len(sorted(self.data, key=lambda x: len(x))[-1]) - 1) * SIZE_TILE
        self.height = len(self.data) * SIZE_TILE
