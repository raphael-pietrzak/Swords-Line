
import pygame
from pygame import Vector2 as vector
from classes.settings import *
from random import uniform, randint, choice
from classes.imports import get_frames_from_sprite_sheet
from entities.hud import TreeBreakBar

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
        self.block = Block(self.rect.midbottom + self.ground_offset , self.block_size)


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
    unique_id = 0

    def __init__(self, pos, frames, group):
        super().__init__(pos, frames, group)
        midtop = self.rect.midtop
        self.alive_frames = frames
        self.tree_break_bar = TreeBreakBar(midtop)
        self.status = 'idle'
        self.ressources = ['Pinecone', 'Twigs', 'Log']
        self.hitbox = pygame.Rect(0, 0, 20, 50)

    
    def burn(self):
        self.frames = get_frames_from_sprite_sheet('graphics/Terrain/Trees/Tree_on_Fire.png', 4, 1)
        self.status = 'burn'
    

    def animate(self, dt):
        super().animate(dt)
        self.hitbox.midbottom = self.rect.midbottom + self.ground_offset


    def death(self):
        # print("L'arbre est brûlé!!!")
        
        # Ajoutez ici le code pour traiter la fin de l'abattage de l'arbre
        self.kill()
        pos = self.pos + vector(randint(-100, 100), randint(-100, 100))
        Tree(pos, self.alive_frames, self.group)
    
    def update_data(self, player_data):
        self.pos = vector(player_data['position'])
        self.healthbar.current_health = player_data['health']
        self.status = player_data['status']
        self.direction = player_data['direction']

    def update(self, dt):
        self.animate(dt)
        if self.status == 'burn':
            self.tree_break_bar.hit(0.3)
        if self.tree_break_bar.ended:
            self.death()

    def draw(self, offset):
        pos = self.rect.topleft + offset
        self.display_surface.blit(self.image, pos)
        # self.tree_break_bar.draw(offset)

        tree_hitbox_rect = self.hitbox.copy().move(offset)
        # pygame.draw.rect(self.display_surface, 'yellow', tree_hitbox_rect)



class Resource(pygame.sprite.Sprite):
    def __init__(self, resource_type, pos, image, group):
        super().__init__(group)
        self.group = group
        self.resource_type = resource_type
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(pos)
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.ground_offset = vector(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
    
    def pick_up(self):
        self.kill()


    def draw(self, offset):
        pos = self.rect.topleft
        self.display_surface.blit(self.image, pos + offset)
        
    



class Block:
    def __init__(self, pos, size):
        self.pos = vector(pos)
        self.rect = pygame.Rect(self.pos, size)
        self.rect.midbottom = self.pos
        self.image = pygame.Surface(size)
        self.image.fill('black')
        self.pos = self.rect.center


class DeadHead(Animated):
    def __init__(self, pos, group):
        path = EDITOR_DATA[1]['path']
        col, row = EDITOR_DATA[1]['grid']
        frames = get_frames_from_sprite_sheet(path, col, row)
        super().__init__(pos, frames, group)
    
    def update(self, dt):
        self.animate(dt)


