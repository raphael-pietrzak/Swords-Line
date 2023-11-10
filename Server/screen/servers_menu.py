import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons
from classes.settings import *
from menu.menu import Button, ButtonGroup
from screen.editor import Editor
from pygame import Vector2 as vector



class ServersMenu:
    def __init__(self, switch, servers):
        self.display_surface = pygame.display.get_surface()
        self.buttons = ButtonGroup()
        self.others_buttons = ButtonGroup()
        self.servers = servers
        self.offset_y = 300
        self.switch_screen = switch
        self.create_buttons()

    # input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_screen("home")

            if event.type == pygame.MOUSEWHEEL:
                self.buttons.update_sprite_pos(vector(0, event.y*10))
                self.offset_y += event.y *10

            self.menu_click(event)
        
    def menu_click(self, event):
        if self.buttons.hover:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
                if self.server1_button.rect.collidepoint(mouse_pos()):
                    self.switch_screen("client")
                if self.server1_on_off_button.rect.collidepoint(mouse_pos()):
                    self.server1.toggle()
                if self.server1_delete_button.rect.collidepoint(mouse_pos()):
                    self.server1.close()
                    self.servers.remove(self.editor1)
                    self.buttons.remove(self.server1_button, self.server1_on_off_button, self.server1_delete_button)
        if self.others_buttons.hover:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
                if self.server1_new_button.rect.collidepoint(mouse_pos()):
                    self.new_room()
                    

    def new_room(self):
        # self.editor1 = Editor(self.switch_screen)
        # self.server1 = self.editor1.server
        # self.server1_indicator = self.server1.online_indicator
        margin = 80
        first_pos_y = self.offset_y + len(self.servers) * margin
        # self.servers.append(self.editor1)
        self.server1_button = Button((WINDOW_WIDTH/2, first_pos_y), (WINDOW_WIDTH/2, 50), f'Room {len(self.servers)}', self.buttons)
        self.server1_on_off_button = Button((self.server1_button.rect.right + margin, first_pos_y), (50, 50), 'O', self.buttons)
        self.server1_delete_button = Button((self.server1_on_off_button.rect.right + margin, first_pos_y), (50, 50), 'D', self.buttons)



    # draw
    def create_buttons(self):
        self.new_room()

        self.server1_new_button = Button((80, WINDOW_HEIGHT - 80), (100, 50), 'New', self.others_buttons)



    # update
    def update(self, dt):
        self.display_surface.fill(MENU_BG_COLOR)
        # self.server1.update_indicator()
        self.server1_indicator.draw()
        self.buttons.draw()
        self.others_buttons.draw()
        self.event_loop()

    
