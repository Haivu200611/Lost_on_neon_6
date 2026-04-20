import pygame

from core.game import Game
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game = Game(screen)
    while game.running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            game.handle_event(event)

        game.update(dt)
        game.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
