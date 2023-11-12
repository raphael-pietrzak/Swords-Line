
import pygame
from pygame import Vector2 as vector
from classes.settings import *
from random import uniform, randint, choice
from classes.imports import get_frames_from_sprite_sheet
from entities.healthbar import TreeBreakBar




class Animated(pygame.sprite.Sprite):
    def __init__(self, pos, frames, group):
        super().__init__(group)
        self.group = group
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=self.pos)
        self.index = uniform(0, len(frames) - 1)
        self.frames = frames
        self.ground_offset = vector(0, -15)

        self.block_size = vector(30, 20)


    def animate(self, dt):
        self.index += dt * ANIMATION_SPEED
        if self.index >= len(self.frames):
            self.index = 0
        
        self.image = self.frames[int(self.index)]
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, offset):
        pos = self.rect.topleft
        self.display_surface.blit(self.image, pos + offset)
        # self.display_surface.blit(self.block.image, self.block.pos + offset)
        # self.display_surface.blit(self.log, self.block.pos + offset)

    def update(self, dt):
        self.animate(dt)



class Tree(Animated):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        # animation
        self.alive_frames = frames
        tree_fire = EDITOR_DATA[6]
        self.frames_fire = get_frames_from_sprite_sheet(tree_fire['path'], tree_fire['grid'][0], tree_fire['grid'][1])

        midtop = self.rect.midtop
        self.tree_break_bar = TreeBreakBar(midtop)
        self.status = 'idle'
        self.ressources = ['Pinecone', 'Twigs', 'Log']
        self.hitbox = pygame.Rect(0, 0, 20, 50)

    
    def animate(self, dt):
        super().animate(dt)
        self.hitbox.midbottom = self.rect.midbottom + self.ground_offset


    def update_data(self, player_data):
        self.pos = vector(player_data['position'])
        self.status = player_data['status']
        self.frames = self.frames_fire if self.status == 'burn' else self.frames


    def update(self, dt):
        self.animate(dt)

    def draw(self, offset):
        pos = self.rect.topleft + offset
        self.display_surface.blit(self.image, pos)


class Flame(Animated):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
    
    def update(self, dt):
        self.animate(dt)
