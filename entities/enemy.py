import pygame

class Enemy:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,32,32)

    def update(self, player):
        if player.rect.x > self.rect.x:
            self.rect.x += 1
        else:
            self.rect.x -= 1

    def draw(self,screen,camera):
        pygame.draw.rect(screen,(255,0,0),
            (self.rect.x-camera.x,self.rect.y-camera.y,32,32))