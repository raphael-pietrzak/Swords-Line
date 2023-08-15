import pygame
from pygame import Vector2 as vector
from classes.settings import *
from player.healthbar import HealthBar
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, frames, group):
        super().__init__(group)
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=self.pos)
        self.attacking = False
        self.ground_offset = vector(0, -60)


        # status
        self.status = "idle"
        self.direction = "right"

        # animation
        self.index = 0
        self.frames = frames
        self.animation_frames = {
            'idle': self.frames[:6],
            'run': self.frames[6:12], 
            'attack': self.frames[12:],
        }

        # health
        self.healthbar = HealthBar(self.rect.topleft, 'blue')
        self.damage = 10


    def animate(self, dt):
        key = f'{self.status}' if f'{self.status}' in self.animation_frames else 'idle'
        if self.status == 'attack' and not self.attacking:
            self.index = 0
            self.attacking = True
        key = 'attack' if self.attacking else key
        current_animation = self.animation_frames[key] if self.direction == 'right' else [pygame.transform.flip(f, True, False) for f in self.animation_frames[key]]

        self.index += dt * ANIMATION_SPEED
        if self.index >= len(current_animation):
            self.index = 0
            self.attacking = False
        
        self.image = current_animation[int(self.index)]
        self.mask = pygame.mask.from_surface(self.image)



    def refresh_data(self, player_data):
        self.pos = vector(player_data['position'])
        self.status = player_data['status']
        self.direction = player_data['direction']
        self.healthbar.current_health = player_data['health']
        self.damage = player_data['damage']
    
    def draw(self, offset):
        self.display_surface.blit(self.image, self.pos + offset)
        self.healthbar.update(offset)
        self.healthbar.draw()


    def update(self, dt):
        self.rect.topleft = self.pos
        self.animate(dt)



class Gobelin(Player):
    def __init__(self, pos, frames):
        super().__init__(pos, frames)


class Knight(Player):
    def __init__(self, pos, frames):
        super().__init__(pos, frames)





