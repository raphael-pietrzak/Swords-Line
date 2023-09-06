import time
import uuid
import pygame
from pygame import Vector2 as vector
from classes.settings import *
from entities.hud import HealthBar
from entities.sprites import Animated, DeadHead
from classes.time import Cooldown


class Player(pygame.sprite.Sprite):

    unique_id = 0

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
        self.healthbar = HealthBar(self.rect.topleft, 'blue')
        self.damage = 10
        self.damage_cooldown = Cooldown(20)

        # time

        self.last_update_time = time.time()
        self.speed = 200
        self.uuid = str(uuid.uuid4())

        self.respawn_point = self.pos.copy()
        self.id = Player.unique_id
        Player.unique_id += 1

        self.client_update_required = False
        self.json_data = {}


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




    def move(self, inputs):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time
        
        self.status = "run" 

        if 'right' in inputs:
            self.pos.x += self.speed * time_elapsed
            self.direction = "right"
        if 'left' in inputs:
            self.pos.x -= self.speed * time_elapsed
            self.direction = "left"
        if 'up' in inputs:
            self.pos.y -= self.speed * time_elapsed
        if 'down' in inputs:
            self.pos.y += self.speed * time_elapsed
        if 'attack' in inputs:
            self.status = "attack"
        
        if not inputs:
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
            self.healthbar.update()
            self.player_surface.blit(self.healthbar.image, (30, 0))
        
        self.display_surface.blit(self.player_surface, pos + offset)
        sword_offset_rect = self.sword_hitbox.copy().move(offset)
        hitbox_offset_rect = self.hitbox.copy().move(offset)
        # pygame.draw.rect(self.display_surface, 'purple', sword_offset_rect)
        # pygame.draw.rect(self.display_surface, 'red', hitbox_offset_rect)
    
    def update_json(self):
        json_data = self.get_json_data()
        if json_data != self.json_data:
            self.client_update_required = True
            self.json_data = json_data
        

    def update(self, dt):
        self.rect.center = self.pos
        self.damage_cooldown.update()
        self.animate(dt)
        self.update_json()
        



class Gobelin(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Goblin'

    def attack_tree(self, tree):
        tree.burn()

class Knight(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Knight'
        self.healthbar.current_health = 20


