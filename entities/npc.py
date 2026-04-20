import pygame

from settings import NPC_INTERACT_RANGE


class TraderNPC:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 30, 52)

    def is_near_player(self, player_rect: pygame.Rect) -> bool:
        delta_x = player_rect.centerx - self.rect.centerx
        delta_y = player_rect.centery - self.rect.centery
        return delta_x * delta_x + delta_y * delta_y <= NPC_INTERACT_RANGE**2

    def get_trade_lines(self, player) -> list[str]:
        return [
            "1) oxygen tank (2 iron) -> +30 oxygen",
            "2) health pack (2 copper) -> +30 health",
            "3) stone drill (3 stone) -> drill lv1",
            "4) copper drill (3 copper) -> drill lv2",
            "5) iron drill (3 iron) -> drill lv3",
            "6) basic laser (2 iron) -> +10 ammo",
            "7) advanced laser (2 iron + 1 core) -> +50 ammo",
            f"current drill level: {player.drill_level}",
        ]

    def try_trade(self, key: str, player, inventory) -> tuple[bool, str]:
        if key == "1":
            return self._buy(inventory, {"iron": 2}, lambda: player.add_oxygen(30), "Oxygen +30.")
        if key == "2":
            return self._buy(inventory, {"copper": 2}, lambda: player.heal(30), "Health +30.")
        if key == "3":
            return self._upgrade_drill(player, inventory, 1, {"stone": 3}, "Stone drill online.")
        if key == "4":
            return self._upgrade_drill(player, inventory, 2, {"copper": 3}, "Copper drill online.")
        if key == "5":
            return self._upgrade_drill(player, inventory, 3, {"iron": 3}, "Iron drill online.")
        if key == "6":
            return self._buy(inventory, {"iron": 2}, lambda: self._grant_basic_laser(player), "Basic laser ammo +10.")
        if key == "7":
            return self._buy(
                inventory,
                {"iron": 2, "core": 1},
                lambda: self._grant_advanced_laser(player),
                "Advanced laser ammo +50.",
            )
        return False, "Unknown trade code."

    def _buy(self, inventory, cost: dict[str, int], on_success, success_msg: str) -> tuple[bool, str]:
        if not inventory.spend(cost):
            return False, "Not enough resources."
        on_success()
        return True, success_msg

    def _upgrade_drill(
        self, player, inventory, target_level: int, cost: dict[str, int], success_msg: str
    ) -> tuple[bool, str]:
        if player.drill_level >= target_level:
            return False, "Drill already at this level or higher."
        if target_level > 1 and player.drill_level < target_level - 1:
            return False, "Upgrade drill step by step."
        if not inventory.spend(cost):
            return False, "Not enough resources."
        player.upgrade_drill(target_level)
        return True, success_msg

    def _grant_basic_laser(self, player) -> None:
        if player.weapon == "none":
            player.weapon = "basic"
        player.add_ammo(10)

    def _grant_advanced_laser(self, player) -> None:
        player.weapon = "advanced"
        player.add_ammo(50)

    def draw(self, screen: pygame.Surface, camera) -> None:
        body = pygame.Rect(
            self.rect.x - int(camera.x),
            self.rect.y - int(camera.y),
            self.rect.width,
            self.rect.height,
        )
        helmet = pygame.Rect(body.x + 5, body.y + 6, body.width - 10, 10)
        pygame.draw.rect(screen, (245, 188, 92), body, border_radius=6)
        pygame.draw.rect(screen, (92, 65, 20), helmet, border_radius=4)
