from settings import *


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.width = len(self.data[0]) * SIZE_TILE
        self.height = len(self.data) * SIZE_TILE
