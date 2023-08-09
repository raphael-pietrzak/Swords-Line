import pygame
from classes.settings import *
from classes.player.healthbar import HealthBar
from classes.player.player import Player



class Knight(Player):
    def __init__(self, frames, pos, group):
        super().__init__(frames, pos, group)
        self.id = 2
        self.pressed_keys = set()
        self.dammage = 10
        self.health_bar = HealthBar(self.rect.topleft, 'blue')
        self.animation_frames = {
            'idle': self.frames[:6],
            'run': self.frames[6:12], 
            'attack': self.frames[12:],
        }

    def event_loop(self, event):
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)

        if pygame.K_q in self.pressed_keys:
            self.orientation = 'left'
            self.direction = 'left'
            self.status = 'run'
        elif pygame.K_d in self.pressed_keys:
            self.orientation = 'right'
            self.direction = 'right'
            self.status = 'run'
        elif pygame.K_z in self.pressed_keys:
            self.orientation = 'up'
            self.status = 'run'
        elif pygame.K_s in self.pressed_keys:
            self.orientation = 'down'
            self.status = 'run'
        elif pygame.K_a in self.pressed_keys:
            self.status = 'attack'
        else:
            self.status = 'idle'
    
    def update(self, dt):
        super().update(dt)
        self.health_bar.update(self.rect.midtop)
