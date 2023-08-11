import time
import pygame
from pygame import Vector2 as vector
from classes.cooldown import Cooldown



class Square:
    def __init__(self, pos):
        self.pos = vector(pos)
        self.speed = 2
        self.cooldown = Cooldown(10)
        self.cooldown.activate()
        self.status = "idle"
        self.direction = "right"

    
    def move(self, inputs_dict):
        movement = inputs_dict['movement']
        
        if self.cooldown.active:
            return
        
        self.status = "run"


        if 'right' in movement:
            self.pos.x += 1
            self.direction = "right"
        if 'left' in movement:
            self.pos.x -= 1
            self.direction = "left"
        if 'up' in movement:
            self.pos.y -= 1
        if 'down' in movement:
            self.pos.y += 1
        if 'attack' in movement:
            self.status = "attack"
        
        if not movement:
            self.status = "idle"

        self.cooldown.activate()

    def update(self, dt):
        self.cooldown.update()





