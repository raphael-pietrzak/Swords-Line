
import pygame
from entities.player import HealthBar
from classes.time import Cooldown
from pygame import Vector2 as vector


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, group):
        super().__init__(group)
        self.group = group
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.ground_offset = vector(0, -20)

    def draw(self, offset):
        pos = self.rect.topleft
        self.display_surface.blit(self.image, pos + offset)


    
class House(Sprite):
    def __init__(self, pos, image, group, faction, player):
        super().__init__(pos, image, group)
        self.display_surface = pygame.display.get_surface()
        self.house_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        # self.house_surface.set_alpha(30)
        self.healing_amount = 5
        self.player = player
        self.radius = 100
        self.is_visible = True
        self.faction = faction
        self.healthbar =  HealthBar('red', (self.rect.width // 2, 10))
        self.hitbox = self.rect
        self.regeneration_cooldown = Cooldown(10)
        self.is_ghost = False
    
    def update_data(self, house_data):
        self.pos = vector(house_data['pos'])
        self.healthbar.current_health = house_data['health']
        self.is_ghost = house_data['faction']
        self.is_visible = house_data['visible']



    
    def draw(self, offset):

        self.house_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.house_surface.blit(self.image, (0, 0))
        self.healthbar.draw(self.house_surface) 
        self.house_surface.set_alpha(255) if self.is_visible else self.house_surface.set_alpha(80)

        if self.player.faction == self.faction or self.is_visible: 
            self.display_surface.blit(self.house_surface, self.pos + offset)