import pygame
from pygame import Vector2 as vector
from classes.settings import *
from classes.healthbar import HealthBar

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, frames):
        super().__init__()
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=self.pos)

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
        current_animation = self.animation_frames[key] if self.direction == 'right' else [pygame.transform.flip(f, True, False) for f in self.animation_frames[key]]

        self.index += dt * ANIMATION_SPEED
        if self.index >= len(current_animation):
            self.index = 0
        
        self.image = current_animation[int(self.index)]
        self.mask = pygame.mask.from_surface(self.image)

    def refresh_data(self, player_data):
        x, y = player_data['position']
        self.pos = vector((x, y))

        self.status = player_data['status']
        self.direction = player_data['direction']
        self.healthbar.current_health = player_data['health']
        self.damage = player_data['damage']


    def update(self, dt):
        self.rect.center = self.pos
        self.animate(dt)
        self.healthbar.update(self.rect.midtop)
        self.healthbar.draw()
        self.display_surface.blit(self.image, self.rect)


class Gobelin(Player):
    def __init__(self, pos, frames):
        super().__init__(pos, frames)


class Knight(Player):
    def __init__(self, pos, frames):
        super().__init__(pos, frames)


class Animated(pygame.sprite.Sprite):
    def __init__(self, pos, frames):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=self.pos)


