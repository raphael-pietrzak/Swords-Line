
from dataclasses import dataclass
from src.core.events import Event, EventType
import pygame
from src.settings import COLOR_BACKGROUND
from src.core.events import GameState


@dataclass
class MenuEvent(Event):
    menu_id: str = ""
    action: str = ""


class MenuState:
    def __init__(self):
        self.menu_stack = []  # Pile des menus
        self.current_menu = None
    
    def push_menu(self, menu):
        """Ajoute un menu sur la pile"""
        self.menu_stack.append(menu)
        self.current_menu = menu
        
    def pop_menu(self):
        """Retire le menu courant et retourne au précédent"""
        if self.menu_stack:
            self.menu_stack.pop()
            self.current_menu = self.menu_stack[-1] if self.menu_stack else None
            return True
        return False
    


class GameMenuManager:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.menu_state = MenuState()
        
        # S'abonner aux événements pertinents
        self.event_manager.subscribe(EventType.MENU_SELECTION, self.handle_menu_selection)
        self.event_manager.subscribe(EventType.MENU_BUTTON_CLICK, self.handle_button_click)
        
    def handle_menu_selection(self, event: MenuEvent):
        if event.action == 'open_submenu':
            submenu_id = event.data['submenu_id']
            if submenu := self.menu_state.current_menu.submenus.get(submenu_id):
                self.menu_state.push_menu(submenu)
        elif event.action == 'back':
            self.menu_state.pop_menu()
            
    def handle_button_click(self, event: MenuEvent):
        if event.action == 'quit':
            self.event_manager.post(Event(EventType.QUIT))
        elif event.action == 'play':
            self.event_manager.post(Event(EventType.STATE_CHANGE, {'new_state': GameState.PLAYING}))
        elif event.action == 'options':
            self.menu_state.push_menu(self.menu_state.current_menu.submenus['options'])
        elif event.action == 'sound':
            self.menu_state.push_menu(self.menu_state.current_menu.submenus['sound'])
        elif event.action == 'graphics':
            self.menu_state.push_menu(self.menu_state.current_menu.submenus['graphics'])
        elif event.action == 'controls':
            self.menu_state.push_menu(self.menu_state.current_menu.submenus['controls'])
        elif event.action == 'back':
            self.menu_state.pop

        
    def handle_event(self, pygame_event):
        if pygame_event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_state.current_menu:
                self.menu_state.current_menu.handle_click(pygame_event.pos)
        elif pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_ESCAPE:
                # Retour au menu précédent avec la touche Échap
                if self.menu_state.pop_menu():
                    self.event_manager.post(MenuEvent(
                        type=EventType.MENU_SELECTION,
                        menu_id='',
                        action='back'
                    ))

    def draw(self, screen):
        screen.fill(COLOR_BACKGROUND)

        if self.menu_state.current_menu:
            self.menu_state.current_menu.draw(screen)