import pygame
from classes.settings import *
from pygame import Vector2 as vector


class Animated(pygame.sprite.Sprite):
    def __init__(self, frames, pos, group):
        super().__init__(group)

        self.display_surface = pygame.display.get_surface()

        self.image = frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.frames = frames
        self.index = 0
        self.pos = vector(pos)


    def animate(self, dt):
        self.index += dt * ANIMATION_SPEED
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
        self.rect.center = self.pos
        


    def update(self, dt):
        self.animate(dt)

