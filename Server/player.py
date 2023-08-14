import time
import pygame
from pygame import Vector2 as vector



class Player:
    def __init__(self, pos):
        # main setup
        self.pos = vector(pos)
        self.cooldown = Cooldown(1)

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

    
    def move(self, client_data):
        inputs = client_data['inputs']
        
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


    def update(self, client_data):
        self.move(client_data)
        self.cooldown.update()




class Cooldown:
    def __init__(self, duration):
        self.active = False
        self.duration = duration
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.active:
            if current_time - self.start_time >= self.duration:
                self.deactivate()
                self.active = False

