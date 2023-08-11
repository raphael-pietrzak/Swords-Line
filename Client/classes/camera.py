import pygame
from pygame import Vector2 as vector
from classes.settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector(0, 0)
        self.display_surface = pygame.display.get_surface()
    
    def custom_draw(self, position):
        position = vector(position)
        self.offset.x = WINDOW_WIDTH // 2 - position.x
        self.offset.y = WINDOW_HEIGHT // 2 - position.y

        for sprite in self.sprites():
            sprite.pos += self.offset
            self.display_surface.blit(sprite.image, sprite.rect)