import pygame
from pygame import Vector2 as vector

class Square(pygame.sprite.Sprite):
    def __init__(self, pos, group, color='blue'):
        super().__init__(group)
        self.pos = vector(pos)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.pos)
    

        


    def update(self, dt):
        pass
