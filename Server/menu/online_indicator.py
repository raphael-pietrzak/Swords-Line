
import pygame
from pygame import Vector2 as vector

from classes.settings import *
from enum import Enum

class ConnectionState(Enum):
    OFFLINE = ("Rouge", "#b00909", '#7a1111')
    ONLINE = ("Vert", "#5ba63c", '#347319')
    WAITING = ("Orange", "#de4a0b", '#8a2d06')


class OnlineIndicator:
    def __init__(self, online=False):
        self.online = online
        self.display_surface = pygame.display.get_surface()
        self.current_state = ConnectionState.ONLINE if self.online else ConnectionState.OFFLINE
        self.create_box()
    

    def update_color(self):
        self.color = self.current_state.value[1]
        self.border_color = self.current_state.value[2]
    
    def change_state(self, state):
        self.current_state = state
        self.online = True if self.current_state == ConnectionState.ONLINE else False
        self.update_color()
    

    def create_box(self):
        margin = 10
        size = 64
        self.box = pygame.rect.Rect((WINDOW_WIDTH - size - margin, margin, size, size))
        self.image = pygame.Surface((size, size))
        self.box_color = '#21211f'
        self.border_box_color = '#131412'
        self.update_color()

    def draw(self):
        pygame.draw.rect(self.display_surface, self.box_color, self.box, border_radius=10)
        pygame.draw.rect(self.display_surface, self.border_box_color, self.box.inflate(2, 2), 4, border_radius=10)
        pygame.draw.circle(self.display_surface, self.color, self.box.center, 10) 
        pygame.draw.circle(self.display_surface, self.border_color, self.box.center, 12, 2)



