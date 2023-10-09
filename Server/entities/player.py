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
        self.display_surface = pygame.display.get_surface()
        self.player_surface = pygame.Surface(frames[0].get_size(), pygame.SRCALPHA)
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.ground_offset = vector(0, -60)

        self.color =  (randint(0, 255), randint(0, 255), randint(0, 255))
        self.attacking = False
        self.group = group

        # status
        self.status = "idle"
        self.direction = "right"

        # animation
        self.frames = frames
        self.index = 0
        self.animation_frames = {
            'idle_right': self.frames[:6],
            'run_right': self.frames[6:12], 
            'attack_right': self.frames[12:],
            'idle_left': [pygame.transform.flip(f, True, False) for f in self.frames[:6]],
            'run_left': [pygame.transform.flip(f, True, False) for f in self.frames[6:12]], 
            'attack_left': [pygame.transform.flip(f, True, False) for f in self.frames[12:]]
        }

        # health
        self.healthbar = HealthBar('blue', (self.rect.width // 2, 10))
        self.healthbar.current_health = 30
        self.damage = 10
        self.attack_cooldown = Cooldown(20)

        # time
        self.last_update_time = time.time()
        self.speed = 300
        self.respawn_point = self.pos.copy()
        self.inputs = []
    

    def get_position(self):
        return [int(self.pos.x), int(self.pos.y)]


    def animate(self, dt):
        key = f'{self.status}_{self.direction}'
        current_animation = self.animation_frames[key]

        self.index += dt * ANIMATION_SPEED
        if self.index >= len(current_animation):
            self.index = 0
        
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
            if not self.attacking:
                self.index = 0
                self.attacking = True
        else:
            self.attacking = False
        
        if not self.inputs:
            self.status = "idle"
        
        self.rect.center = self.pos

    
    def heal(self, amount):
        self.healthbar.current_health += amount
        self.healthbar.current_health = min(self.healthbar.current_health, self.healthbar.max_width)
    

    def take_damage(self, amount):
        self.healthbar.current_health -= amount
        self.healthbar.current_health = max(0, self.healthbar.current_health)
        if self.healthbar.current_health <= 0:
            DeadHead(self.pos, self.group[0])
            self.__init__(self.respawn_point, self.frames, self.group) if self.respawn_point else self.kill()


    def draw(self, offset):
        self.player_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.player_surface.blit(self.image, (0, 0))

        if self.healthbar.current_health < self.healthbar.max_width:
            self.healthbar.draw(self.player_surface)
        
        pos = self.rect.topleft + offset
        self.display_surface.blit(self.player_surface, pos)
    

    def update(self, dt):
        self.attack_cooldown.update()
        self.move()
        self.animate(dt)
        


class Goblin(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Goblin'

    def attack_tree(self, tree):
        tree.burn()

class Knight(Player):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        self.faction = 'Knight'
