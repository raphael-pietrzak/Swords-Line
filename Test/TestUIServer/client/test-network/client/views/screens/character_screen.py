import pygame
from .base_screen import BaseScreen

class CharacterScreen(BaseScreen):
    def __init__(self, surface, controller):
        super().__init__(surface, controller)
        self.font = pygame.font.Font(None, 36)
        self.selected_character = 0
        self.characters = ["Warrior", "Mage", "Archer"]

    def draw(self):
        self.surface.fill((50, 50, 50))
        title = self.font.render("Select your character:", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.surface.get_width()/2, 100))
        self.surface.blit(title, title_rect)

        for i, char in enumerate(self.characters):
            color = (255, 255, 0) if i == self.selected_character else (255, 255, 255)
            text = self.font.render(char, True, color)
            text_rect = text.get_rect(center=(self.surface.get_width()/2, 200 + i * 50))
            self.surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_character = (self.selected_character - 1) % len(self.characters)
            elif event.key == pygame.K_DOWN:
                self.selected_character = (self.selected_character + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                self.controller.network.send({
                    "type": "SELECT_CHARACTER",
                    "character": self.characters[self.selected_character]
                })
