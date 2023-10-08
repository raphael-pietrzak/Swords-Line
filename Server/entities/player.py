from random import randint
import time
import uuid
import pygame
from pygame import Vector2 as vector
from classes.settings import *
from entities.healthbar import HealthBar
from entities.sprites import Animated, DeadHead
from classes.time import Cooldown


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, frames, group):
        super().__init__(group)
        # main setup

        self.display_surface = pygame.display.get_surface()
        self.player_surface = pygame.Surface(frames[0].get_size(), pygame.SRCALPHA)
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=self.pos)
        self.attacking = False
        self.ground_offset = vector(0, -60)
        self.mask = pygame.mask.from_surface(self.image)
        self.gold_count = 0
        self.group = group
        self.color =  (randint(0, 255), randint(0, 255), randint(0, 255))


        self.hitbox = pygame.Rect(0, 0, 40, 64)
        self.hitbox_offset = vector(0, 0)

        self.sword_hitbox = pygame.Rect(0, 0, 20, 20)
        self.sword_offset = vector(77, 0)

        # status
        self.status = "idle"
        self.direction = "right"

        # animation
        self.index = 0
        self.frames = frames
        self.animation_frames = {
            'idle': self.frames[:6],
            'run': self.frames[6:12], 
            'attack': self.frames[12:],
        }

        # health
        self.healthbar = HealthBar('blue', (self.rect.width // 2, 10))
        self.healthbar.current_health = 30
        self.damage = 10
        self.damage_cooldown = Cooldown(20)

        # time

        self.last_update_time = time.time()
        self.speed = 400
        self.uuid = str(uuid.uuid4())

        self.respawn_point = self.pos.copy()

        self.client_update_required = False
        self.json_data = {}
        self.inputs = []
    
    def get_position(self):
        return [int(self.pos.x), int(self.pos.y)]


    def animate(self, dt):
        key = f'{self.status}' if f'{self.status}' in self.animation_frames else 'idle'
        if self.status == 'attack' and not self.attacking:
            self.index = 0
            self.attacking = True
        key = 'attack' if self.attacking else key
        # key = 'attack'

        current_animation = self.animation_frames[key] if self.direction == 'right' else [pygame.transform.flip(f, True, False) for f in self.animation_frames[key]]

        self.index += dt * ANIMATION_SPEED
        if self.index >= len(current_animation):
            self.index = 0
            self.attacking = False
        
        self.sword_hitbox.center = self.pos + self.sword_offset if self.direction == 'right' else self.pos - self.sword_offset
        self.hitbox.center = self.pos

        self.image = current_animation[int(self.index)]
        self.mask = pygame.mask.from_surface(self.image)



    def move(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        self.status = "run" 


        if 'up' in self.inputs:
            self.pos.y -= self.speed * time_elapsed
        if 'down' in self.inputs:
            self.pos.y += self.speed * time_elapsed
        if 'left' in self.inputs:
            self.pos.x -= self.speed * time_elapsed
            self.direction = "left"
        if 'right' in self.inputs:
            self.pos.x += self.speed * time_elapsed
            self.direction = "right"
        if 'attack' in self.inputs:
            self.status = "attack"
        
        if not self.inputs:
            self.status = "idle"
        
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)

    
    def regenerate(self, health):
        self.healthbar.current_health += health
        self.healthbar.current_health = min(self.healthbar.current_health, self.healthbar.max_width)
    
    def take_damage(self, damage):
        self.healthbar.current_health -= damage
        if self.healthbar.current_health <= 0:
            DeadHead(self.pos, self.group[0])
            self.__init__(self.respawn_point, self.frames, self.group) if self.respawn_point else self.kill()

    def get_json_data(self):
        # { "id": 1, "faction": "knight", "position": [200, 300], "health": 100, status": "idle", direction": "right" }
        json_data = {}
        json_data['id'] = self.id
        json_data['faction'] = self.faction
        json_data['position'] = [int(self.pos.x), int(self.pos.y)]
        json_data['health'] = self.healthbar.current_health
        json_data['status'] = self.status
        json_data['direction'] = self.direction
        return json_data

    def draw(self, offset):
        self.player_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        pos = self.rect.topleft
        self.player_surface.blit(self.image, (0, 0))
        if self.healthbar.current_health < self.healthbar.max_width:
            self.healthbar.draw(self.player_surface)
        
        self.display_surface.blit(self.player_surface, pos + offset)
        sword_offset_rect = self.sword_hitbox.copy().move(offset)
        hitbox_offset_rect = self.hitbox.copy().move(offset)
        # pygame.draw.rect(self.display_surface, 'purple', sword_offset_rect)
        # pygame.draw.rect(self.display_surface, 'red', hitbox_offset_rect)
    

        

    def update(self, dt):
        self.move()
        self.rect.center = self.pos
        self.damage_cooldown.update()
        self.animate(dt)
        







# from random import randint
# import time, pygame

# from pygame import Vector2 as vector

# from  classes.settings import *



# class Player(pygame.sprite.Sprite):
#     def __init__(self, group, frames):
#         super().__init__()
#         self.display_surface = pygame.display.get_surface()
#         self.ground_offset = vector(0, 0)
#         self.image = pygame.Surface((40, 40))
#         self.rect = self.image.get_rect()

#         self.index = 0
#         self.frames = frames


#         self.color =  (randint(0, 255), randint(0, 255), randint(0, 255))
#         self.image.fill(self.color)
#         self.pos = vector((randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
#         self.speed = 400
#         self.last_update_time = time.time()
#         self.inputs = []
    
#     def animate(self, dt):
#         self.index += dt * ANIMATION_SPEED
#         if self.index >= len(self.frames):
#             self.index = 0

#         self.image = self.frames[int(self.index)]
#         self.mask = pygame.mask.from_surface(self.image)


#     def move(self):
#         current_time = time.time()
#         time_elapsed = current_time - self.last_update_time
#         self.last_update_time = current_time

#         if 'up' in self.inputs:
#             self.pos.y -= self.speed * time_elapsed
#         if 'down' in self.inputs:
#             self.pos.y += self.speed * time_elapsed
#         if 'left' in self.inputs:
#             self.pos.x -= self.speed * time_elapsed
#         if 'right' in self.inputs:
#             self.pos.x += self.speed * time_elapsed


#     def regenerate(self, health):
#         self.healthbar.current_health += health
#         self.healthbar.current_health = min(self.healthbar.current_health, self.healthbar.max_width)
    
#     def take_damage(self, damage):
#         self.healthbar.current_health -= damage
#         if self.healthbar.current_health <= 0:
#             DeadHead(self.pos, self.group[0])
#             self.__init__(self.respawn_point, self.frames, self.group) if self.respawn_point else self.kill()
    
#     def get_position(self):
#         return [int(self.pos.x), int(self.pos.y)]


#     def draw(self, offset):
        
#         pygame.draw.rect(self.display_surface, self.color, (self.pos.x, self.pos.y, 40, 40))



#     def update(self, dt):
#         self.move()





class Goblin(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Goblin'
        self.healthbar.current_health = 20

    def attack_tree(self, tree):
        tree.burn()

class Knight(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Knight'
