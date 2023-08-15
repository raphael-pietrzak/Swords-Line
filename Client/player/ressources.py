import pygame
from pygame import Vector2 as vector

class Ressource(pygame.sprite.Sprite):
    def __init__(self, pos, image, group):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.ground_offset = vector(0, 0)
        self.mask = pygame.mask.from_surface(self.image)


    def draw(self, offset):
        pos = self.rect.topleft
        self.display_surface.blit(self.image, pos + offset)
        