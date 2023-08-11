import time
import pygame
from pygame import Vector2 as vector
from classes.cooldown import Cooldown



class Player:
    def __init__(self, pos):
        # main setup
        self.pos = vector(pos)
        self.cooldown = Cooldown(10)

        # status
        self.status = "idle"
        self.direction = "right"

        # stats
        self.speed = 2
        self.health = 100
        self.damage = 10

        # hitbox
        self.hitbox = pygame.Rect(0, 0, 20, 20)
        self.hitbox.center = self.pos

    
    def move(self, inputs_dict):
        inputs = inputs_dict['inputs']
        
        if self.cooldown.active:
            return
        
        self.status = "run"


        if 'right' in inputs:
            self.pos.x += 1
            self.direction = "right"
        if 'left' in inputs:
            self.pos.x -= 1
            self.direction = "left"
        if 'up' in inputs:
            self.pos.y -= 1
        if 'down' in inputs:
            self.pos.y += 1
        if 'attack' in inputs:
            self.status = "attack"
        
        if not inputs:
            self.status = "idle"

        self.cooldown.activate()

    def hit(self, damage):
        self.health -= damage if self.health - damage >= 0 else 0

    def update(self, dt):
        self.cooldown.update()





