import pygame
from .base_screen import BaseScreen

class GameScreen(BaseScreen):
    def __init__(self, surface, controller):
        super().__init__(surface, controller)
        self.font = pygame.font.Font(None, 36)
        self.player_positions = {}

    def update(self):
        game_state = self.controller.game_state
        if game_state:
            self.player_positions = game_state.get("player_positions", {})

    def draw(self):
        self.surface.fill((0, 0, 0))
        
        # Dessiner la grille de jeu
        for x in range(0, self.surface.get_width(), 50):
            pygame.draw.line(self.surface, (50, 50, 50), (x, 0), (x, self.surface.get_height()))
        for y in range(0, self.surface.get_height(), 50):
            pygame.draw.line(self.surface, (50, 50, 50), (0, y), (self.surface.get_width(), y))

        # Dessiner les joueurs
        for player_id, pos in self.player_positions.items():
            color = (255, 255, 0) if player_id == self.controller.player.id else (255, 255, 255)
            pygame.draw.circle(self.surface, color, (pos["x"], pos["y"]), 20)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                self.controller.network.send({
                    "type": "MOVE",
                    "direction": event.key
                })
