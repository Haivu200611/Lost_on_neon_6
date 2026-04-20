import random

import pygame

from settings import COLOR_BG_BOTTOM, COLOR_BG_TOP


class Sky:
    def __init__(self, width: int, height: int, seed: int = 6):
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        self.background = pygame.Surface((width, height))
        self._build_background()

    def _build_background(self) -> None:
        for y in range(self.height):
            t = y / max(1, self.height - 1)
            r = int(COLOR_BG_TOP[0] + (COLOR_BG_BOTTOM[0] - COLOR_BG_TOP[0]) * t)
            g = int(COLOR_BG_TOP[1] + (COLOR_BG_BOTTOM[1] - COLOR_BG_TOP[1]) * t)
            b = int(COLOR_BG_TOP[2] + (COLOR_BG_BOTTOM[2] - COLOR_BG_TOP[2]) * t)
            pygame.draw.line(self.background, (r, g, b), (0, y), (self.width, y))

        for _ in range(170):
            x = self.rng.randint(0, self.width - 1)
            y = self.rng.randint(0, int(self.height * 0.58))
            radius = self.rng.choice([1, 1, 1, 2])
            shade = self.rng.randint(160, 255)
            pygame.draw.circle(self.background, (shade, shade, shade), (x, y), radius)

        pygame.draw.circle(
            self.background,
            (72, 196, 255),
            (self.width - 160, 120),
            54,
        )
        pygame.draw.circle(
            self.background,
            (20, 44, 84),
            (self.width - 145, 110),
            48,
        )

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
