
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
    def __init__(self, pos, image, group, faction):
        super().__init__(pos, image, group)
        self.display_surface = pygame.display.get_surface()
        self.house_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        # self.house_surface.set_alpha(30)
        self.healing_amount = 5
        self.radius = 100
        self.is_visible = True
        self.faction = faction
        self.healthbar =  HealthBar(pos, 'red')
        self.hitbox = self.rect
        self.regeneration_cooldown = Cooldown(10)
    
    def update_data(self, house_data):
        # { "id": 1, "faction": "goblin", "position": [250, 180], "health": 100, visible": True }
        self.pos = vector(house_data['position'])
        self.healthbar.current_health = house_data['health']
        self.is_ghost = house_data['ghost']
        self.is_visible = house_data['visible']



    
    def draw(self, offset):
        if not self.is_visible and not self.is_ghost: return

        self.regeneration_cooldown.update()
        pos = self.pos + offset
        self.house_surface.blit(self.image, (0, 0))  
        self.healthbar.update()
        self.house_surface.blit(self.healthbar.image, (5, 0))


        # if not self.is_visible :
        #     self.ghost_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        #     self.ghost_surface.fill('white')
        #     self.ghost_surface.set_alpha(100)
        #     self.house_surface.blit(self.ghost_surface, (0, 0))
        #     self.house_surface.set_colorkey('white')
        
      
        self.house_surface.set_alpha(255) if self.is_ghost else self.house_surface.set_alpha(80)

        self.display_surface.blit(self.house_surface, pos)
