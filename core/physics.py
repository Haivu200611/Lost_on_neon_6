from __future__ import annotations

from settings import GRAVITY, TERMINAL_VELOCITY


def resolve_entity_movement(entity, terrain, dt: float) -> None:
    entity.on_ground = False

    entity.velocity.y = min(entity.velocity.y + GRAVITY * dt, TERMINAL_VELOCITY)

    entity.pos.x += entity.velocity.x * dt
    entity.rect.x = round(entity.pos.x)
    for tile in terrain.get_solid_tiles_in_rect(entity.rect):
        if entity.rect.colliderect(tile.rect):
            if entity.velocity.x > 0:
                entity.rect.right = tile.rect.left
            elif entity.velocity.x < 0:
                entity.rect.left = tile.rect.right
            entity.pos.x = float(entity.rect.x)

    entity.pos.y += entity.velocity.y * dt
    entity.rect.y = round(entity.pos.y)
    for tile in terrain.get_solid_tiles_in_rect(entity.rect):
        if entity.rect.colliderect(tile.rect):
            if entity.velocity.y > 0:
                entity.rect.bottom = tile.rect.top
                entity.on_ground = True
            elif entity.velocity.y < 0:
                entity.rect.top = tile.rect.bottom
            entity.velocity.y = 0.0
            entity.pos.y = float(entity.rect.y)


def clamp_entity_to_world(entity, world_w: int, world_h: int) -> None:
    if entity.rect.left < 0:
        entity.rect.left = 0
        entity.pos.x = float(entity.rect.x)
    if entity.rect.right > world_w:
        entity.rect.right = world_w
        entity.pos.x = float(entity.rect.x)
    if entity.rect.top < 0:
        entity.rect.top = 0
        entity.pos.y = float(entity.rect.y)
    if entity.rect.bottom > world_h:
        entity.rect.bottom = world_h
        entity.velocity.y = 0.0
        entity.on_ground = True
        entity.pos.y = float(entity.rect.y)
