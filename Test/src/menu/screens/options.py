
import pygame
from src.menu.screens.base import Screen

class OptionsMenu(Screen):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Options"
        
    def draw(self):
        self.surface.fill((0, 255, 0))  # Fond vert
        font = pygame.font.Font(None, 36)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        self.surface.blit(text, text_rect)
        return self.surface


