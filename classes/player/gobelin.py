import pygame
from classes.settings import *
from classes.sprites import HealthBar
from classes.player.player import Player



class Gobelin(Player):
    def __init__(self, frames, pos, group):
        super().__init__(frames, pos, group)
        self.id = 1
        self.pressed_keys = set()
        self.health_bar = HealthBar(self.rect.topleft, 'red')
        self.animation_frames = {
            'idle': self.frames[:7],
            'run': self.frames[7:13], 
            'attack': self.frames[13:],
        }

    def event_loop(self, event):
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)

        if pygame.K_LEFT in self.pressed_keys:
            self.orientation = 'left'
            self.direction = 'left'
            self.status = 'run'
        elif pygame.K_RIGHT in self.pressed_keys:
            self.orientation = 'right'
            self.direction = 'right'
            self.status = 'run'
        elif pygame.K_UP in self.pressed_keys:
            self.orientation = 'up'
            self.status = 'run'
        elif pygame.K_DOWN in self.pressed_keys:
            self.orientation = 'down'
            self.status = 'run'
        elif pygame.K_EQUALS in self.pressed_keys:
            self.status = 'attack'
        else:
            self.status = 'idle'
    
    def update(self, dt):
        super().update(dt)
        self.health_bar.update(self.rect.midtop)