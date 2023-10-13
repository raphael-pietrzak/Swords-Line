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

    def __init__(self, pos, frames, group, house, collision_sprites):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.player_surface = pygame.Surface(frames[0].get_size(), pygame.SRCALPHA)
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.ground_offset = vector(0, -60)

        self.color =  (randint(0, 255), randint(0, 255), randint(0, 255))
        self.is_attacking = False
        self.group = group
        self.house = house

        # status
        self.status = "idle"
        self.direction = "right"

        # animation
        self.frames = frames
        self.frame_index = 0
        self.animation_frames = {
            'idle_right': self.frames[:6],
            'run_right': self.frames[6:12], 
            'attack_right': self.frames[12:],
            'idle_left': [pygame.transform.flip(f, True, False) for f in self.frames[:6]],
            'run_left': [pygame.transform.flip(f, True, False) for f in self.frames[6:12]], 
            'attack_left': [pygame.transform.flip(f, True, False) for f in self.frames[12:]]
        }
        self.collision_sprites = collision_sprites

        # health
        self.healthbar = HealthBar('blue', (self.rect.width // 2, 10))
        self.heal_cooldown = Cooldown(30)
        self.damage = 10
        self.attack_cooldown = Cooldown(40)
        self.hit_success = False

        # time
        self.last_update_time = time.time()
        self.speed = 300
        self.respawn_point = self.house.rect.center
        self.inputs = []

        # hitbox
        self.hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, 40, 70)
        self.sword_hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, 30, 30)
    

    def get_position(self):
        return [int(self.pos.x), int(self.pos.y)]


    def move(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time


        self.status = "run" 

        # vertical
        if 'up' in self.inputs:
            self.pos.y -= self.speed * time_elapsed
        if 'down' in self.inputs:
            self.pos.y += self.speed * time_elapsed
        self.collision('vertical')

        # horizontal
        if 'left' in self.inputs:
            self.pos.x -= self.speed * time_elapsed
            self.direction = "left"
        if 'right' in self.inputs:
            self.pos.x += self.speed * time_elapsed
            self.direction = "right"
        self.collision('horizontal')



        if 'attack' in self.inputs:
            if not self.is_attacking:
                self.is_attacking = True
                self.frame_index = 0

        
        if not self.inputs:
            self.status = "idle"
        
        if self.is_attacking:
            self.status = "attack"


        # update rects pos
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        self.sword_hitbox.center = self.pos + vector(60, -10) if self.direction == "right" else self.pos + vector(-60, -10)


    def collision(self, direction):
        offset = vector(self.rect.midbottom) + self.ground_offset - self.rect.center

        if direction == 'vertical':
            for sprite in self.collision_sprites:
                if sprite.rect.collidepoint(self.pos + offset) :
                    if 'up' in self.inputs:
                        self.pos.y = sprite.rect.bottom - offset.y
                    if 'down' in self.inputs:
                        self.pos.y = sprite.rect.top - offset.y -1
                        

        if direction == 'horizontal':
            for sprite in self.collision_sprites:
                if sprite.rect.collidepoint(self.pos + offset) :
                    if 'left' in self.inputs:
                        self.pos.x = sprite.rect.right - offset.x
                    if 'right' in self.inputs:
                        self.pos.x = sprite.rect.left - offset.x -1


    def animate(self, dt):

        key = f'{self.status}_{self.direction}'
        current_animation = self.animation_frames[key]

        self.frame_index += dt * ANIMATION_SPEED
        if self.frame_index >= len(current_animation):
            self.is_attacking = False
            self.hit_success = False
            self.frame_index = 0
        

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
    


    def heal(self, amount):
        self.healthbar.current_health += amount
        self.healthbar.current_health = min(self.healthbar.current_health, self.healthbar.max_width)
    

    def take_damage(self, amount):
        self.healthbar.current_health -= amount
        self.healthbar.current_health = max(0, self.healthbar.current_health)
        if self.healthbar.current_health <= 0:
            DeadHead(self.pos, self.group[0])
            self.__init__(self.respawn_point, self.frames, self.group, self.house) if self.respawn_point else self.kill()
    

    def update_house_visibility(self):
        distance_to_house = vector(self.rect.center).distance_to(vector(self.house.rect.center))
        if distance_to_house < self.house.heal_radius:
            self.house.is_visible = True
    

    def update_healing(self):
        distance_to_house = vector(self.rect.center).distance_to(vector(self.house.rect.center))
        if distance_to_house < self.house.heal_radius and not self.heal_cooldown.active:
            self.heal(self.house.heal_amount)
            self.heal_cooldown.activate()



    def draw(self, offset):
        self.player_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.player_surface.blit(self.image, (0, 0))

        
        self.healthbar.draw(self.player_surface)
        
        pos = self.rect.topleft + offset
        self.display_surface.blit(self.player_surface, pos)

    

    def update(self, dt):
        self.attack_cooldown.update()
        self.heal_cooldown.update()
        self.move()
        self.update_house_visibility()
        self.update_healing()
        self.animate(dt)
        


class Goblin(Player):
    def __init__(self, pos, frames, group, house, collision_sprites):
        super().__init__(pos, frames, group, house, collision_sprites)
        self.faction = 'goblin'

    def attack_tree(self, tree):
        tree.burn()


class Knight(Player):
    def __init__(self, pos, frames, group, house, collision_sprites):
        super().__init__(pos, frames, group, house, collision_sprites)
        self.faction = 'knight'
