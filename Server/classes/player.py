import time
import pygame
from pygame import Vector2 as vector


class Square:
    def __init__(self, pos):
        self.pos = vector(pos)
        self.speed = 2

    
    def move(self, inputs_dict):
        movement = inputs_dict['movement']

        if 'right' in movement:
            self.pos.x += 1
        if 'left' in movement:
            self.pos.x -= 1
        if 'up' in movement:
            self.pos.y -= 1
        if 'down' in movement:
            self.pos.y += 1





