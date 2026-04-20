import pygame
from core.game import Game
from settings import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LOST ON NEON-6")

clock = pygame.time.Clock()
game = Game(screen)

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

    game.update(dt)
    game.draw()

pygame.quit()