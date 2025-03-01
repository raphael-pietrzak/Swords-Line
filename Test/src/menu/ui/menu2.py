
import pygame
from src.core.events import EventType
from src.core.menu_events import MenuEvent

class Menu:
    def __init__(self, menu_id: str, event_manager):
        self.menu_id = menu_id
        self.event_manager = event_manager
        self.buttons = []
        self.submenus = {}
        
    def add_button(self, text: str, action: str, position: tuple):
        self.buttons.append({
            'text': text,
            'action': action,
            'rect': pygame.Rect(position[0], position[1], 200, 50)
        })
    
    def add_submenu(self, submenu):
        self.submenus[submenu.menu_id] = submenu
    
    def handle_click(self, pos):
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                if button['action'] in self.submenus:
                    # Navigation vers un sous-menu
                    event = MenuEvent(
                        type=EventType.MENU_SELECTION,
                        menu_id=self.menu_id,
                        action='open_submenu',
                        data={'submenu_id': button['action']}
                    )
                else:
                    # Action normale du bouton
                    event = MenuEvent(
                        type=EventType.MENU_BUTTON_CLICK,
                        menu_id=self.menu_id,
                        action=button['action']
                    )
                self.event_manager.post(event)
                return True
        return False
    
    def render_button_text(self, screen):
        font = pygame.font.Font(None, 36)
        for button in self.buttons:
            text = font.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)

    def draw(self, screen):
        for button in self.buttons:
            pygame.draw.rect(screen, (200, 200, 200), button['rect'])
        self.render_button_text(screen)