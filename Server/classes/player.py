import pygame
from pygame import Vector2 as vector


class Square:
    def __init__(self, pos):
        self.pos = vector(pos)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(center=self.pos)

    
    def move(self, inputs_dict):
        movement = inputs_dict['movement']
        if 'right' in movement:
            self.pos.x += 5
        if 'left' in movement:
            self.pos.x -= 5
        if 'up' in movement:
            self.pos.y -= 5
        if 'down' in movement:
            self.pos.y += 5


