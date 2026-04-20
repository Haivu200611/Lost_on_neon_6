import pygame
from core.physics import resolve_entity_movement
from settings import (
    JUMP_VELOCITY,
    MAX_HEALTH,
    MAX_OXYGEN,
    OXYGEN_DRAIN_RATE,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    SUFFOCATION_DAMAGE_RATE,
)


class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.pos = pygame.Vector2(float(x), float(y))
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.on_ground = False

        self.max_health = float(MAX_HEALTH)
        self.health = float(MAX_HEALTH)
        self.max_oxygen = float(MAX_OXYGEN)
        self.oxygen = float(MAX_OXYGEN)

        self.drill_level = 0
        self.weapon = "none"
        self.ammo = 0
        self.facing = 1

    def update(self, dt: float, terrain) -> None:
        keys = pygame.key.get_pressed()
        self.velocity.x = 0.0

        if keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
            self.facing = 1

        if keys[pygame.K_w] and self.on_ground:
            self.velocity.y = JUMP_VELOCITY

        resolve_entity_movement(self, terrain, dt)
        self._update_survival(dt)

    def _update_survival(self, dt: float) -> None:
        self.oxygen = max(0.0, self.oxygen - OXYGEN_DRAIN_RATE * dt)
        if self.oxygen <= 0.0:
            self.take_damage(SUFFOCATION_DAMAGE_RATE * dt)

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def heal(self, amount: float) -> None:
        self.health = min(self.max_health, self.health + amount)

    def add_oxygen(self, amount: float) -> None:
        self.oxygen = min(self.max_oxygen, self.oxygen + amount)

    def upgrade_drill(self, target_level: int) -> bool:
        if target_level <= self.drill_level:
            return False
        self.drill_level = target_level
        return True

    def add_ammo(self, amount: int) -> None:
        self.ammo += amount

    def draw(self, screen: pygame.Surface, camera) -> None:
        body = pygame.Rect(
            self.rect.x - int(camera.x),
            self.rect.y - int(camera.y),
            self.rect.width,
            self.rect.height,
        )
        visor = pygame.Rect(body.x + 5, body.y + 8, body.width - 10, 10)
        accent = pygame.Rect(body.x + 4, body.bottom - 12, body.width - 8, 7)

        pygame.draw.rect(screen, (54, 220, 255), body, border_radius=6)
        pygame.draw.rect(screen, (15, 35, 58), visor, border_radius=4)
        pygame.draw.rect(screen, (125, 250, 255), accent, border_radius=3)
