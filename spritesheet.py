import pygame

class SpriteSheet:
    def __init__(self, path=None):
        self.sheet = pygame.image.load(path).convert_alpha() if path else None

    def get_image(self, x,y,w,h):
        surf = pygame.Surface((w,h), pygame.SRCALPHA)
        if self.sheet:
            surf.blit(self.sheet,(0,0),(x,y,w,h))
        return surf