import pygame
from pygame import Vector2 as vector
from classes.settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector(0, 0)
        self.display_surface = pygame.display.get_surface()
        self.hitbox_active = False
    
    def custom_draw(self, position):
        position = vector(position)
        self.offset.x = WINDOW_WIDTH // 2 - position.x
        self.offset.y = WINDOW_HEIGHT // 2 - position.y


        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom + sprite.ground_offset.y + self.offset.y)

        for sprite in sorted_sprites:
            sprite.draw(self.offset)

            if self.hitbox_active:
                rect = sprite.rect.copy().move(self.offset.x, self.offset.y)
                pygame.draw.rect(self.display_surface, BLUE_CONTOUR, rect , 2)
                pygame.draw.circle(self.display_surface, BLUE_PLAYER, sprite.rect.midbottom + sprite.ground_offset + self.offset, 5)


        