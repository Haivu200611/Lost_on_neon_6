import pygame
from settings import *
from core.physics import apply_gravity, check_collision

class Player:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,32,48)
        self.vel_y = 0
        self.on_ground = False

        self.health = 100
        self.oxygen = OXYGEN_MAX

    def update(self,dt,terrain):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED

        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = JUMP_FORCE

        apply_gravity(self)
        check_collision(self, terrain.tiles)

        self.oxygen -= OXYGEN_DECREASE

    def draw(self,screen,camera):
        pygame.draw.rect(screen,(0,255,255),
            (self.rect.x-camera.x,self.rect.y-camera.y,32,48))