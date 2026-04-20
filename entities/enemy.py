import pygame
from core.physics import resolve_entity_movement
from settings import (
    ENEMY_HEIGHT,
    ENEMY_WIDTH,
    JUMP_VELOCITY,
    VOID_BUG_DAMAGE_PER_SECOND,
    VOID_BUG_SPEED,
)


class VoidBug:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.pos = pygame.Vector2(float(x), float(y))
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.on_ground = False

    def update(self, dt: float, player, terrain) -> None:
        dx = player.rect.centerx - self.rect.centerx
        if dx > 4:
            self.velocity.x = VOID_BUG_SPEED
        elif dx < -4:
            self.velocity.x = -VOID_BUG_SPEED
        else:
            self.velocity.x = 0.0

        if self.on_ground and abs(dx) < 220 and player.rect.centery < self.rect.centery - 16:
            self.velocity.y = JUMP_VELOCITY * 0.72

        resolve_entity_movement(self, terrain, dt)

    def deal_contact_damage(self, player, dt: float) -> None:
        if self.rect.colliderect(player.rect):
            player.take_damage(VOID_BUG_DAMAGE_PER_SECOND * dt)

    def draw(self, screen: pygame.Surface, camera) -> None:
        body = pygame.Rect(
            self.rect.x - int(camera.x),
            self.rect.y - int(camera.y),
            self.rect.width,
            self.rect.height,
        )
        eye = pygame.Rect(body.centerx - 3, body.y + 4, 6, 6)
        pygame.draw.ellipse(screen, (188, 42, 68), body)
        pygame.draw.ellipse(screen, (236, 86, 116), eye)
