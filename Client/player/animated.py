
import pygame
from pygame import Vector2 as vector
from classes.settings import *

class Animated(pygame.sprite.Sprite):
    def __init__(self, pos, frames, group):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.index = 0
        self.frames = frames
        self.ground_offset = vector(0, -15)

        self.block_size = vector(30, 20)
        self.block = Block(self.rect.midbottom + self.ground_offset , self.block_size)

        self.log = pygame.image.load('graphics/Dead_and_Fire/Log.png').convert_alpha()



    def animate(self, dt):
        self.index += dt * ANIMATION_SPEED
        if self.index >= len(self.frames):
            self.index = 0
        
        self.image = self.frames[int(self.index)]
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, offset):
        self.display_surface.blit(self.image, self.pos + offset)
        # self.display_surface.blit(self.block.image, self.block.pos + offset)
        self.display_surface.blit(self.log, self.block.pos + offset)

    
    def update(self, dt):
        self.animate(dt)

class Block:
    def __init__(self, pos, size):
        self.pos = vector(pos)
        self.rect = pygame.Rect(self.pos, size)
        self.rect.midbottom = self.pos
        self.image = pygame.Surface(size)
        self.image.fill('black')
        self.pos = self.rect.topleft