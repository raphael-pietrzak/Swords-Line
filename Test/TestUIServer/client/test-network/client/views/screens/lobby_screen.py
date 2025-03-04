import pygame
from .base_screen import BaseScreen

class LobbyScreen(BaseScreen):
    def __init__(self, surface, controller):
        super().__init__(surface, controller)
        self.font = pygame.font.Font(None, 36)
        self.players = []

    def update(self):
        # Mettre à jour la liste des joueurs depuis le contrôleur
        pass

    def draw(self):
        self.surface.fill((50, 50, 50))
        title = self.font.render("Waiting for players...", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.surface.get_width()/2, 100))
        self.surface.blit(title, title_rect)

        for i, player in enumerate(self.players):
            text = self.font.render(f"Player: {player}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.surface.get_width()/2, 200 + i * 40))
            self.surface.blit(text, text_rect)

        ready_text = self.font.render("Press SPACE when ready", True, (255, 255, 0))
        ready_rect = ready_text.get_rect(center=(self.surface.get_width()/2, 500))
        self.surface.blit(ready_text, ready_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.controller.network.send({"type": "PLAYER_READY"})
