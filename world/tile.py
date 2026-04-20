import pygame
from settings import TILE_SIZE

class Tile:
    def __init__(self, x,y,type_):
        self.rect = pygame.Rect(x,y,TILE_SIZE,TILE_SIZE)
        self.type = type_

    def draw(self, screen, camera):
        color = (150,80,200)

        if self.type == "iron":
            color = (200,100,100)
        elif self.type == "core":
            color = (255,255,0)

        pygame.draw.rect(screen,color,
            (self.rect.x-camera.x,self.rect.y-camera.y,TILE_SIZE,TILE_SIZE))