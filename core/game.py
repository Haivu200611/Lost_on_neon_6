import pygame
import random

from core.camera import Camera
from core.physics import clamp_entity_to_world
from entities.enemy import VoidBug
from entities.npc import TraderNPC
from entities.player import Player
from items.inventory import Inventory
from settings import (
    COLOR_SHIP,
    COLOR_SHIP_ACCENT,
    COLOR_UI_OK,
    COLOR_UI_PANEL,
    COLOR_UI_TEXT,
    COLOR_UI_WARN,
    ENEMY_HEIGHT,
    MAX_HEALTH,
    MAX_OXYGEN,
    MINING_RANGE,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    REQUIRED_CORES_TO_ESCAPE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    WORLD_HEIGHT_PX,
    WORLD_WIDTH_PX,
    WORLD_WIDTH_TILES,
)
from world.sky import Sky
from world.terrain import Terrain


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.running = True
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 42, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 18)
        self.reset()

    def reset(self) -> None:
        self.state = "playing"
        self.trade_open = False
        self.message = ""
        self.message_time = 0.0

        seed = random.randint(0, 999_999)
        self.terrain = Terrain(seed=seed)
        self.sky = Sky(SCREEN_WIDTH, SCREEN_HEIGHT, seed=seed)

        self.ship_rect = self._build_ship_rect()
        spawn_x = self.ship_rect.centerx - PLAYER_WIDTH // 2
        spawn_y = self.ship_rect.top - PLAYER_HEIGHT - 4
        self.player = Player(spawn_x, spawn_y)
        self.inventory = Inventory()

        npc_x = self.ship_rect.right + TILE_SIZE * 2
        npc_y = self.terrain.get_ground_spawn_y(npc_x, 52)
        self.npc = TraderNPC(npc_x, npc_y)

        self.enemies = self._spawn_enemies(9)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH_PX, WORLD_HEIGHT_PX)
        self.camera.update(self.player.rect, 1.0)

    def _build_ship_rect(self) -> pygame.Rect:
        ship_column = 5
        ship_y = self.terrain.get_surface_y_px(ship_column) - TILE_SIZE * 2
        return pygame.Rect(ship_column * TILE_SIZE, ship_y, TILE_SIZE * 2, TILE_SIZE * 2)

    def _spawn_enemies(self, count: int) -> list[VoidBug]:
        enemies: list[VoidBug] = []
        for _ in range(count):
            column = random.randint(26, WORLD_WIDTH_TILES - 6)
            x = column * TILE_SIZE + random.randint(0, TILE_SIZE - 1)
            y = self.terrain.get_ground_spawn_y(x, ENEMY_HEIGHT)
            enemies.append(VoidBug(x, y))
        return enemies

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
            return

        if self.state in {"win", "lose"}:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self._handle_interaction_key()
            elif event.key == pygame.K_ESCAPE and self.trade_open:
                self.trade_open = False
            elif self.trade_open and event.unicode in "1234567":
                success, msg = self.npc.try_trade(event.unicode, self.player, self.inventory)
                self._set_message(msg, 2.4 if success else 2.8)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.trade_open:
            self._mine_from_screen(event.pos)

    def _handle_interaction_key(self) -> None:
        if self.trade_open:
            self.trade_open = False
            return

        if self.npc.is_near_player(self.player.rect):
            self.trade_open = True
            self._set_message("Trading channel opened. Press 1..7.", 1.6)
            return

        if self._can_escape():
            self.state = "win"
            return

        if self._is_near_ship():
            missing = max(0, REQUIRED_CORES_TO_ESCAPE - self.inventory.get("core"))
            if missing > 0:
                self._set_message(f"Need {missing} more core(s) to escape.", 2.0)

    def _is_near_ship(self) -> bool:
        return self.player.rect.colliderect(self.ship_rect.inflate(96, 96))

    def _can_escape(self) -> bool:
        return self._is_near_ship() and self.inventory.get("core") >= REQUIRED_CORES_TO_ESCAPE

    def _mine_from_screen(self, screen_pos: tuple[int, int]) -> None:
        world_x, world_y = self.camera.world_from_screen(screen_pos[0], screen_pos[1])
        player_center = pygame.Vector2(self.player.rect.center)
        if player_center.distance_to((world_x, world_y)) > MINING_RANGE:
            self._set_message("Target too far to mine.", 1.4)
            return

        tile = self.terrain.get_tile_at_world(world_x, world_y)
        if not tile:
            return

        if not tile.is_mineable(self.player.drill_level):
            self._set_message(
                f"Drill level {tile.required_drill_level} required for {tile.tile_type}.",
                1.8,
            )
            return

        resource, amount = tile.mine(self.player.drill_level)
        self.terrain.remove_tile(tile)
        if resource:
            self.inventory.add(resource, amount)
            self._set_message(f"Mined +{amount} {resource}.", 1.0)
        else:
            self._set_message("Dirt cleared.", 0.8)

    def _set_message(self, text: str, duration: float) -> None:
        self.message = text
        self.message_time = duration

    def update(self, dt: float) -> None:
        if self.state != "playing":
            return

        self.player.update(dt, self.terrain)
        clamp_entity_to_world(self.player, WORLD_WIDTH_PX, WORLD_HEIGHT_PX)

        for enemy in self.enemies:
            enemy.update(dt, self.player, self.terrain)
            enemy.deal_contact_damage(self.player, dt)

        if self.player.health <= 0:
            self.state = "lose"

        if self.message_time > 0:
            self.message_time = max(0.0, self.message_time - dt)

        self.camera.update(self.player.rect, dt)

    def draw(self) -> None:
        self.sky.draw(self.screen)
        self.terrain.draw(self.screen, self.camera)
        self._draw_ship()
        self.npc.draw(self.screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        self._draw_hud()
        self._draw_context_prompts()
        if self.trade_open:
            self._draw_trade_panel()

        if self.state == "lose":
            self._draw_overlay("MISSION FAILED", "Press R to restart")
        elif self.state == "win":
            self._draw_overlay("ESCAPED NEON-6", "Press R to play again")

        pygame.display.flip()

    def _draw_ship(self) -> None:
        ship = self.camera.apply_rect(self.ship_rect)
        cockpit = pygame.Rect(ship.x + 6, ship.y + 5, ship.width - 12, 12)
        engine_left = pygame.Rect(ship.x + 4, ship.bottom - 10, 8, 10)
        engine_right = pygame.Rect(ship.right - 12, ship.bottom - 10, 8, 10)
        pygame.draw.rect(self.screen, COLOR_SHIP, ship, border_radius=4)
        pygame.draw.rect(self.screen, COLOR_SHIP_ACCENT, cockpit, border_radius=3)
        pygame.draw.rect(self.screen, (255, 150, 90), engine_left)
        pygame.draw.rect(self.screen, (255, 150, 90), engine_right)

    def _draw_hud(self) -> None:
        panel = pygame.Rect(16, 14, 360, 154)
        pygame.draw.rect(self.screen, COLOR_UI_PANEL, panel, border_radius=8)
        pygame.draw.rect(self.screen, (96, 104, 136), panel, 2, border_radius=8)

        self._draw_bar(
            label="HEALTH",
            x=28,
            y=28,
            width=220,
            value=self.player.health,
            maximum=MAX_HEALTH,
            color=(255, 94, 94),
        )
        self._draw_bar(
            label="OXYGEN",
            x=28,
            y=62,
            width=220,
            value=self.player.oxygen,
            maximum=MAX_OXYGEN,
            color=(92, 214, 255),
        )

        status = [
            f"drill lv: {self.player.drill_level}",
            f"weapon: {self.player.weapon}",
            f"ammo: {self.player.ammo}",
            f"core: {self.inventory.get('core')}/{REQUIRED_CORES_TO_ESCAPE}",
            f"stone:{self.inventory.get('stone')} copper:{self.inventory.get('copper')}",
            f"iron:{self.inventory.get('iron')}",
        ]
        y = 97
        for line in status:
            text = self.small_font.render(line, True, COLOR_UI_TEXT)
            self.screen.blit(text, (28, y))
            y += 18

    def _draw_bar(
        self,
        label: str,
        x: int,
        y: int,
        width: int,
        value: float,
        maximum: float,
        color: tuple[int, int, int],
    ) -> None:
        ratio = 0.0 if maximum <= 0 else max(0.0, min(1.0, value / maximum))
        bg = pygame.Rect(x, y + 2, width, 16)
        fg = pygame.Rect(x, y + 2, int(width * ratio), 16)
        label_text = self.small_font.render(label, True, COLOR_UI_TEXT)
        self.screen.blit(label_text, (x + width + 12, y))
        pygame.draw.rect(self.screen, (34, 34, 44), bg, border_radius=4)
        pygame.draw.rect(self.screen, color, fg, border_radius=4)
        pygame.draw.rect(self.screen, (120, 126, 145), bg, 1, border_radius=4)

    def _draw_context_prompts(self) -> None:
        prompt = None
        color = COLOR_UI_TEXT
        if self.npc.is_near_player(self.player.rect) and self.state == "playing" and not self.trade_open:
            prompt = "Press E to trade with the station trader."
        elif self._is_near_ship():
            if self.inventory.get("core") >= REQUIRED_CORES_TO_ESCAPE:
                prompt = "Press E at the ship to escape."
                color = COLOR_UI_OK
            else:
                missing = REQUIRED_CORES_TO_ESCAPE - self.inventory.get("core")
                prompt = f"Collect {missing} more core(s) to escape."
                color = COLOR_UI_WARN

        if prompt:
            text = self.font.render(prompt, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 28))
            self.screen.blit(text, rect)

        if self.message_time > 0 and self.message:
            msg = self.font.render(self.message, True, COLOR_UI_TEXT)
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 56))
            self.screen.blit(msg, msg_rect)

    def _draw_trade_panel(self) -> None:
        width = 620
        height = 300
        panel = pygame.Rect((SCREEN_WIDTH - width) // 2, 72, width, height)
        shade = pygame.Surface((width, height), pygame.SRCALPHA)
        shade.fill((10, 12, 24, 235))
        self.screen.blit(shade, panel.topleft)
        pygame.draw.rect(self.screen, (96, 104, 136), panel, 2, border_radius=8)

        title = self.font.render("Trader Console", True, COLOR_UI_OK)
        self.screen.blit(title, (panel.x + 16, panel.y + 12))
        hint = self.small_font.render("Press 1..7 to trade, E or ESC to close", True, COLOR_UI_TEXT)
        self.screen.blit(hint, (panel.x + 16, panel.y + 36))

        y = panel.y + 70
        for line in self.npc.get_trade_lines(self.player):
            txt = self.small_font.render(line, True, COLOR_UI_TEXT)
            self.screen.blit(txt, (panel.x + 20, y))
            y += 28

    def _draw_overlay(self, headline: str, subtitle: str) -> None:
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 165))
        self.screen.blit(shade, (0, 0))

        head = self.big_font.render(headline, True, COLOR_UI_TEXT)
        sub = self.font.render(subtitle, True, COLOR_UI_TEXT)
        self.screen.blit(head, head.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 16)))
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 26)))
