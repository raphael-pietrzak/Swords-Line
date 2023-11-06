import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons
from classes.settings import *
from menu.menu import Button, ButtonGroup



class SettingsMenu:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_screen("home")
            self.menu_click(event)
        
    def menu_click(self, event):
        if self.buttons.hover:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
                pass



    # draw
    def create_buttons(self):
        first_pos_y = 300
        margin = 80
        Button((WINDOW_WIDTH/2, first_pos_y), (WINDOW_WIDTH/2, 50), 'Width', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + margin), (WINDOW_WIDTH/2, 50), 'Height', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + 2 * margin), (WINDOW_WIDTH/2, 50), 'Host', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + 3 * margin), (WINDOW_WIDTH/2, 50), 'Port', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + 4 * margin), (WINDOW_WIDTH/2, 50), 'Colors', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + 5 * margin), (WINDOW_WIDTH/2, 50), 'Animation Speed', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + 6 * margin), (WINDOW_WIDTH/2, 50), 'Back', self.buttons)



    # update
    def update(self, dt):
        self.display_surface.fill(MENU_BG_COLOR)
        self.buttons.draw()
        self.event_loop()

    
