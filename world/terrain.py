import random
import pygame

from settings import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SURFACE_MAX,
    SURFACE_MIN,
    TILE_SIZE,
    WORLD_HEIGHT_TILES,
    WORLD_WIDTH_TILES,
)
from world.tile import Tile


class Terrain:
    def __init__(self, seed: int = 6):
        self.rng = random.Random(seed)
        self.tiles: dict[tuple[int, int], Tile] = {}
        self.surface_heights = [0] * WORLD_WIDTH_TILES
        self._generate()

    def _generate(self) -> None:
        previous_surface = self.rng.randint(SURFACE_MIN, SURFACE_MAX)

        for x in range(WORLD_WIDTH_TILES):
            step = self.rng.choice([-1, 0, 0, 0, 1])
            surface = max(SURFACE_MIN, min(SURFACE_MAX, previous_surface + step))
            if x < 8:
                surface = SURFACE_MIN + 2
            self.surface_heights[x] = surface
            previous_surface = surface

            for y in range(surface, WORLD_HEIGHT_TILES):
                self.tiles[(x, y)] = Tile(x, y, self._pick_tile_type(surface, y))

        self._inject_core_nodes(target_count=42)

    def _pick_tile_type(self, surface: int, y: int) -> str:
        depth = y - surface
        roll = self.rng.random()
        world_depth = y / WORLD_HEIGHT_TILES

        if depth <= 1:
            return "dirt"
        if depth <= 3:
            return "dirt" if roll < 0.68 else "stone"
        if world_depth > 0.72:
            if roll < 0.16:
                return "iron"
            if roll < 0.38:
                return "copper"
            return "stone"
        if world_depth > 0.52:
            return "copper" if roll < 0.11 else "stone"
        return "stone"

    def _inject_core_nodes(self, target_count: int) -> None:
        current = sum(1 for tile in self.tiles.values() if tile.tile_type == "core")
        if current >= target_count:
            return

        candidates = [
            key
            for key, tile in self.tiles.items()
            if tile.tile_type in {"stone", "copper", "iron"}
            and key[1] > self.surface_heights[key[0]] + 5
        ]
        self.rng.shuffle(candidates)
        for x, y in candidates[: target_count - current]:
            self.tiles[(x, y)] = Tile(x, y, "core")

    def get_surface_y_px(self, column: int) -> int:
        column = max(0, min(column, WORLD_WIDTH_TILES - 1))
        return self.surface_heights[column] * TILE_SIZE

    def get_ground_spawn_y(self, x_px: float, entity_h: int) -> int:
        column = int(max(0, min(x_px // TILE_SIZE, WORLD_WIDTH_TILES - 1)))
        return self.get_surface_y_px(column) - entity_h

    def get_tile_at_world(self, x: float, y: float) -> Tile | None:
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        return self.tiles.get((grid_x, grid_y))

    def remove_tile(self, tile: Tile) -> None:
        self.tiles.pop((tile.grid_x, tile.grid_y), None)

    def get_solid_tiles_in_rect(self, rect: pygame.Rect) -> list[Tile]:
        min_x = max(0, rect.left // TILE_SIZE - 1)
        max_x = min(WORLD_WIDTH_TILES - 1, rect.right // TILE_SIZE + 1)
        min_y = max(0, rect.top // TILE_SIZE - 1)
        max_y = min(WORLD_HEIGHT_TILES - 1, rect.bottom // TILE_SIZE + 1)

        hits: list[Tile] = []
        for grid_x in range(min_x, max_x + 1):
            for grid_y in range(min_y, max_y + 1):
                tile = self.tiles.get((grid_x, grid_y))
                if tile:
                    hits.append(tile)
        return hits

    def draw(self, screen: pygame.Surface, camera) -> None:
        start_x = max(0, int(camera.x // TILE_SIZE) - 1)
        end_x = min(
            WORLD_WIDTH_TILES - 1, int((camera.x + SCREEN_WIDTH) // TILE_SIZE) + 1
        )
        start_y = max(0, int(camera.y // TILE_SIZE) - 1)
        end_y = min(
            WORLD_HEIGHT_TILES - 1, int((camera.y + SCREEN_HEIGHT) // TILE_SIZE) + 1
        )

        for grid_x in range(start_x, end_x + 1):
            for grid_y in range(start_y, end_y + 1):
                tile = self.tiles.get((grid_x, grid_y))
                if tile:
                    tile.draw(screen, camera.x, camera.y)
