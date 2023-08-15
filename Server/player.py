import time
import pygame
from pygame import Vector2 as vector



class Player:
    def __init__(self, pos):
        # main setup
        self.pos = vector(pos)

        # status
        self.status = "idle"
        self.direction = "right"

        # stats
        self.speed = 100
        self.health = 100
        self.damage = 10

        # hitbox
        self.hitbox = pygame.Rect(0, 0, 20, 20)
        self.hitbox.center = self.pos

        self.last_update_time = time.time()
    
    def move(self, client_data):
        inputs = client_data['inputs']
        
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time
        
        self.status = "run" 

        if 'right' in inputs:
            self.pos.x += self.speed * time_elapsed
            self.direction = "right"
        if 'left' in inputs:
            self.pos.x -= self.speed * time_elapsed
            self.direction = "left"
        if 'up' in inputs:
            self.pos.y -= self.speed * time_elapsed
        if 'down' in inputs:
            self.pos.y += self.speed * time_elapsed
        if 'attack' in inputs:
            self.status = "attack"
        
        if not inputs:
            self.status = "idle"


    def hit(self, damage):
        self.health -= damage if self.health - damage >= 0 else 0


    def update(self, client_data):
        self.move(client_data)




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

