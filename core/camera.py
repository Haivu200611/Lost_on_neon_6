from __future__ import annotations

import pygame

from settings import CAMERA_SMOOTHING


class Camera:
    def __init__(self, screen_w: int, screen_h: int, world_w: int, world_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.world_w = world_w
        self.world_h = world_h
        self.x = 0.0
        self.y = 0.0

    def update(self, target_rect: pygame.Rect, dt: float) -> None:
        desired_x = target_rect.centerx - self.screen_w / 2
        desired_y = target_rect.centery - self.screen_h / 2
        desired_x = max(0.0, min(desired_x, self.world_w - self.screen_w))
        desired_y = max(0.0, min(desired_y, self.world_h - self.screen_h))

        lerp = min(1.0, CAMERA_SMOOTHING * 60.0 * dt)
        self.x += (desired_x - self.x) * lerp
        self.y += (desired_y - self.y) * lerp

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-int(self.x), -int(self.y))

    def world_from_screen(self, sx: int, sy: int) -> tuple[float, float]:
        return sx + self.x, sy + self.y
