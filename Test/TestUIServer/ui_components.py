import pygame
from settings import *

class Button:
    def __init__(self, rect, text, action, enabled=True, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.rect = rect
        self.text = text
        self.action = action
        self.enabled = enabled
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos) and self.enabled
    
    def draw(self, screen, font):
        # Déterminer la couleur du bouton
        if not self.enabled:
            color = (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2)
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color
        
        # Dessiner le bouton
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 1)
        
        # Dessiner le texte
        button_text = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_x = self.rect.x + (self.rect.width - button_text.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - button_text.get_height()) // 2
        screen.blit(button_text, (text_x, text_y))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.enabled and self.action:
                self.action()
                return True
        return False

class TabButton(Button):
    def __init__(self, rect, text, tab_value, active=False):
        super().__init__(rect, text, None, True)
        self.tab_value = tab_value
        self.active = active
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.enabled:
                return self.tab_value
        return None

    def draw(self, screen, font):
        # Couleur basée sur l'état actif/inactif
        color = TAB_ACTIVE_COLOR if self.active else TAB_INACTIVE_COLOR
        
        # Dessiner le fond du tab
        pygame.draw.rect(screen, color, self.rect)
        
        # Dessiner la bordure (sauf en bas si actif)
        if self.active:
            # Dessiner uniquement les 3 côtés (gauche, haut, droite)
            pygame.draw.line(screen, TEXT_COLOR, self.rect.topleft, (self.rect.right, self.rect.top))
            pygame.draw.line(screen, TEXT_COLOR, self.rect.topleft, (self.rect.left, self.rect.bottom))
            pygame.draw.line(screen, TEXT_COLOR, (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom))
        else:
            pygame.draw.rect(screen, TEXT_COLOR, self.rect, 1)
        
        # Dessiner le texte
        button_text = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_x = self.rect.x + (self.rect.width - button_text.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - button_text.get_height()) // 2
        screen.blit(button_text, (text_x, text_y))
