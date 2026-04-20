import pygame
from settings import REQUIRED_DRILL_LEVEL, RESOURCE_FROM_TILE, TILE_COLORS, TILE_SIZE


class Tile:
    def __init__(self, grid_x: int, grid_y: int, tile_type: str):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_type = tile_type
        self.rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    @property
    def required_drill_level(self) -> int:
        return REQUIRED_DRILL_LEVEL[self.tile_type]

    def is_mineable(self, drill_level: int) -> bool:
        return drill_level >= self.required_drill_level

    def mine(self, drill_level: int) -> tuple[str | None, int]:
        if not self.is_mineable(drill_level):
            return None, 0

        if self.tile_type == "core":
            amount = 2 if drill_level >= 3 else 1
            return "core", amount

        resource = RESOURCE_FROM_TILE[self.tile_type]
        if resource is None:
            return None, 0
        return resource, 1

    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float) -> None:
        sx = self.rect.x - int(camera_x)
        sy = self.rect.y - int(camera_y)
        color = TILE_COLORS[self.tile_type]
        pygame.draw.rect(screen, color, (sx, sy, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, (0, 0, 0), (sx, sy, TILE_SIZE, TILE_SIZE), 1)
