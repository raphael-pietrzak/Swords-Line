import pygame
from typing import Optional
from src.core.events import Event
from src.settings import COLOR_BUTTON, COLOR_BUTTON_HOVER

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, callback: callable):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        
    def draw(self, surface: pygame.Surface):
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect)
        self.render_text(surface)

    def render_text(self, surface: pygame.Surface):
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event: pygame.event.Event) -> Optional[Event]:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            return self.callback()
        return None