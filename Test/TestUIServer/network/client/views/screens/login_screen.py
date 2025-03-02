import pygame
from .base_screen import BaseScreen

class LoginScreen(BaseScreen):
    def __init__(self, surface, controller):
        super().__init__(surface, controller)
        self.username = ""
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        self.surface.fill((50, 50, 50))
        text = self.font.render("Enter username: " + self.username, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
        self.surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.username:
                self.controller.connect_to_server(self.username)
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif len(self.username) < 20 and event.unicode.isalnum():
                self.username += event.unicode
