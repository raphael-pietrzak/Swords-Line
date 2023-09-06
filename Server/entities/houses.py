
import pygame
from entities.sprites import Sprite
from entities.player import HealthBar
from classes.time import Cooldown

class House(Sprite):
    unique_id = 0
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
        self.id = House.unique_id
        House.unique_id += 1
    
    def take_damage(self, damage):
        if self.is_visible:
            self.healthbar.current_health -= damage
            if self.healthbar.current_health <= 0:
                self.kill()
    
    def get_json_data(self):
        # { "id": 1, "faction": "goblin", "position": [250, 180], "health": 100 }
        json_data = {}
        json_data['id'] = self.id
        json_data['faction'] = self.faction
        json_data['position'] = [int(self.pos.x), int(self.pos.y)]
        json_data['health'] = self.healthbar.current_health
        return json_data

    
    def draw(self, offset):
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
        
      
        self.house_surface.set_alpha(255) if self.is_visible else self.house_surface.set_alpha(80)

        self.display_surface.blit(self.house_surface, pos)
