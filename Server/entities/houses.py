
import uuid
import pygame
from entities.sprites import Sprite
from entities.player import HealthBar
from classes.time import Cooldown
from pygame import Vector2 as vector




class House(pygame.sprite.Sprite):
    def __init__(self, pos, image, group, faction):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.house_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

        self.pos = vector(pos)
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.ground_offset = vector(0, -25)


        # health
        self.healthbar =  HealthBar('red', (self.rect.width // 2, 10))
        self.healthbar.current_health = 30
        self.heal_radius = 100
        self.heal_amount = 5


        self.faction = faction
        self.hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, 100, 120)
        self.hitbox.midbottom = self.rect.midbottom + self.ground_offset
        self.is_visible = False

        self.uuid = str(uuid.uuid4()).split('-')[0]

    
    def take_damage(self, damage):
        if self.is_visible:
            self.healthbar.current_health -= damage
            if self.healthbar.current_health <= 0:
                self.kill()
    

    def get_data(self):
        return {
            'pos': [int(self.pos[0]), int(self.pos[1])],
            'faction': self.faction,
            'health': self.healthbar.current_health,
            'visible': self.is_visible,
            
        }

    
    def draw(self, offset):

        self.house_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.house_surface.blit(self.image, (0, 0))
        self.healthbar.draw(self.house_surface)
        self.house_surface.set_alpha(255) if self.is_visible else self.house_surface.set_alpha(80)

        self.display_surface.blit(self.house_surface, self.pos + offset)
