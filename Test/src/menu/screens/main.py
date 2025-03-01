import pygame
from src.menu.screens.base import Screen

class MainMenu(Screen):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Menu Principal"
        
    def draw(self):
        self.surface.fill((255, 0, 0))  # Fond rouge
        font = pygame.font.Font(None, 36)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        self.surface.blit(text, text_rect)
        return self.surface
    
