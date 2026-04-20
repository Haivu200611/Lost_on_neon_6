from settings import GRAVITY

def apply_gravity(entity):
    entity.vel_y += GRAVITY
    entity.rect.y += entity.vel_y

def check_collision(entity, tiles):
    entity.on_ground = False

    for tile in tiles:
        if entity.rect.colliderect(tile.rect):
            if entity.vel_y > 0:
                entity.rect.bottom = tile.rect.top
                entity.vel_y = 0
                entity.on_ground = True