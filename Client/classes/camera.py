import pygame
from pygame import Vector2 as vector
from classes.settings import *
from classes.player import Player

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector(0, 0)
        self.display_surface = pygame.display.get_surface()
    
    def custom_draw(self, position, players):
        position = vector(position)
        self.offset.x = WINDOW_WIDTH // 2 - position.x
        self.offset.y = WINDOW_HEIGHT // 2 - position.y

        for sprite in self.sprites():
            pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, pos)

        for player in players:
            player_pos = player.rect.midtop + self.offset
            player.healthbar.update(player_pos)
            player.healthbar.draw()

        