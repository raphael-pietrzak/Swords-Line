import pygame
from pygame import Vector2 as vector
from classes.settings import *

class Square(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE_CONTOUR)
        self.rect = self.image.get_rect(center=self.pos)
    

    def update(self, dt):
        self.rect.center = self.pos
        self.display_surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, frames):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE_CONTOUR)
        self.rect = self.image.get_rect(center=self.pos)
        self.status = "idle"
        self.direction = "right"
        self.index = 0
        self.frames = frames
        self.animation_frames = {
            'idle': self.frames[:6],
            'run': self.frames[6:12], 
            'attack': self.frames[12:],
        }


    def animate(self, dt):
        key = f'{self.status}' if f'{self.status}' in self.animation_frames else 'idle'
        current_animation = self.animation_frames[key] if self.direction == 'right' else [pygame.transform.flip(f, True, False) for f in self.animation_frames[key]]

        self.index += dt * ANIMATION_SPEED
        if self.index >= len(current_animation):
            self.index = 0
        
        self.image = current_animation[int(self.index)]
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.rect.center = self.pos
        self.animate(dt)
        self.display_surface.blit(self.image, self.rect)
