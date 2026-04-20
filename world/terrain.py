import random
from world.tile import Tile
from settings import *

class Terrain:
    def __init__(self):
        self.tiles = []
        self.generate()

    def generate(self):
        for x in range(WORLD_WIDTH):
            h = random.randint(10,15)

            for y in range(h, WORLD_HEIGHT):
                t = "dirt"

                if random.random() < 0.05:
                    t = "iron"

                if random.random() < 0.02:
                    t = "core"

                self.tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,t))

    def draw(self, screen, camera):
        for t in self.tiles:
            t.draw(screen, camera)