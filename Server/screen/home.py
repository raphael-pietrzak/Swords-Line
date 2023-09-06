import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons
from classes.settings import *
from menu.menu import Button, ButtonGroup



class GameMenu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.buttons = ButtonGroup()
        self.create_buttons()
        self.switch_screen = switch

    # input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.menu_click(event)
        
    def menu_click(self, event):
        if self.buttons.hover:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
                for sprite in self.buttons:
                    if sprite.rect.collidepoint(mouse_pos()):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.switch_screen("client")


    # draw
    def create_buttons(self):
        first_pos_y = 300
        margin = 80
        Button((WINDOW_WIDTH/2, first_pos_y), (WINDOW_WIDTH/2, 50), 'Solo', self.buttons)
        # Button((WINDOW_WIDTH/2, first_pos_y + margin), (WINDOW_WIDTH/2, 50), 'Multi', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + margin), (WINDOW_WIDTH/2, 50), 'Settings', self.buttons)


    # update
    def update(self, dt):
        self.display_surface.fill(MENU_BG_COLOR)
        self.buttons.update()
        self.event_loop()

    
