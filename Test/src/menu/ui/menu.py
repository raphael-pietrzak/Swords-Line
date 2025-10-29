import pygame
from src.core.events import EventManager, Event, EventType, GameState
from src.ui.button import Button
from src.settings import WINDOW_WIDTH, BUTTON_WIDTH, BUTTON_HEIGHT, COLOR_BACKGROUND

class Menu:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        button_x = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
        self.buttons = [
            Button(button_x, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Play", 
                  lambda: Event(EventType.STATE_CHANGE, {'new_state': GameState.PLAYING})),
            Button(button_x, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "Settings", 
                  lambda: Event(EventType.STATE_CHANGE, {'new_state': GameState.SETTINGS})),
            Button(button_x, 400, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", 
                  lambda: Event(EventType.QUIT))
        ]
    
    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            menu_event = button.handle_event(event)
            if menu_event:
                self.event_manager.post(menu_event)
                
    def draw(self, surface: pygame.Surface):
        surface.fill(COLOR_BACKGROUND)
        for button in self.buttons:
            button.draw(surface)