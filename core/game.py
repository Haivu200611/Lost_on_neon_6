import pygame
from entities.player import Player
from entities.enemy import Enemy
from world.terrain import Terrain
from core.camera import Camera
from items.inventory import Inventory
from settings import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "MENU"

        self.terrain = Terrain()
        self.player = Player(200, 100)
        self.inventory = Inventory()

        self.enemies = [Enemy(400,100)]

        self.camera = Camera()

    def handle_event(self, event):
        if self.state == "MENU":
            if event.type == pygame.KEYDOWN:
                self.state = "PLAYING"

        elif self.state == "PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mine()

        elif self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                self.__init__(self.screen)

    def mine(self):
        for tile in self.terrain.tiles:
            if self.player.rect.colliderect(tile.rect):
                self.inventory.add(tile.type)
                self.terrain.tiles.remove(tile)
                break

    def update(self, dt):
        if self.state != "PLAYING":
            return

        self.player.update(dt, self.terrain)

        for e in self.enemies:
            e.update(self.player)

            if self.player.rect.colliderect(e.rect):
                self.player.health -= 0.3

        if self.player.oxygen <= 0 or self.player.health <= 0:
            self.state = "GAME_OVER"

        if self.inventory.items.get("core",0) >= REQUIRED_CORES:
            self.state = "WIN"

        self.camera.update(self.player)

    def draw(self):
        self.screen.fill((20,0,40))

        if self.state == "MENU":
            self.draw_text("Press any key to start", 300)
        elif self.state == "PLAYING":
            self.terrain.draw(self.screen, self.camera)

            for e in self.enemies:
                e.draw(self.screen, self.camera)

            self.player.draw(self.screen, self.camera)
            self.draw_ui()

        elif self.state == "GAME_OVER":
            self.draw_text("TIN HIEU THAT LAC...", 250)

        elif self.state == "WIN":
            self.draw_text("BAN DA ROI KHOI NEON-6!", 250)

        pygame.display.flip()

    def draw_ui(self):
        font = pygame.font.SysFont(None, 24)

        oxy = font.render(f"OXY: {int(self.player.oxygen)}", True,(255,255,255))
        hp = font.render(f"HP: {int(self.player.health)}", True,(255,100,100))
        core = font.render(f"CORE: {self.inventory.items.get('core',0)}",True,(255,255,0))

        self.screen.blit(oxy,(10,10))
        self.screen.blit(hp,(10,30))
        self.screen.blit(core,(10,50))

    def draw_text(self, text, y):
        font = pygame.font.SysFont(None, 48)
        t = font.render(text, True, (255,255,255))
        self.screen.blit(t,(200,y))