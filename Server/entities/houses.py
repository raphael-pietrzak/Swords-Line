
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
        self.ground_offset = vector(0, -20)


        # health
        self.healthbar =  HealthBar('red', (self.rect.width // 2, 10))
        self.healthbar.current_health = 30
        self.healing_amount = 5
        self.regeneration_cooldown = Cooldown(10)
        self.radius = 100


        self.faction = faction
        self.hitbox = self.rect
        self.is_visible = False

    
    def take_damage(self, damage):
        if self.is_visible:
            self.healthbar.current_health -= damage
            if self.healthbar.current_health <= 0:
                self.kill()

    
    def draw(self, offset):
        self.regeneration_cooldown.update()

        self.house_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.house_surface.blit(self.image, (0, 0))
        self.healthbar.draw(self.house_surface)
        self.house_surface.set_alpha(255) if self.is_visible else self.house_surface.set_alpha(80)

        self.display_surface.blit(self.house_surface, self.pos + offset)
