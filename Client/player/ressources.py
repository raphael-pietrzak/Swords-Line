import pygame
from pygame import Vector2 as vector

class Ressource(pygame.sprite.Sprite):
    def __init__(self, pos, image, group):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.ground_offset = vector(0, 0)

    def draw(self, offset):
        self.display_surface.blit(self.image, self.pos + offset)
        