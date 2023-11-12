import time
import uuid
import pygame
from pygame import Vector2 as vector
from classes.settings import *
from entities.healthbar import HealthBar
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



    
    def update_data(self, player_data):
        self.pos = vector(player_data['pos'])
        self.color = player_data['color']
        self.lifes = player_data['lifes']
        self.direction = player_data['direction']
        self.status = player_data['status']
        self.healthbar.current_health = player_data['health']
    


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
        

    def update(self, dt):
        self.rect.center = self.pos
        self.animate(dt)





class Gobelin(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Goblin'


class Knight(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Knight'


