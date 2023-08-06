import pygame
from classes.settings import *
from pygame import Vector2 as vector
from classes.timer import Cooldown




class Player(pygame.sprite.Sprite):
    def __init__(self, frames, pos, group):
        super().__init__(group)

        self.display_surface = pygame.display.get_surface()

        # main
        self.id = 0
        self.group = group
        self.pos = vector(pos)

        # attack
        self.cooldown = Cooldown(200)
        self.dammage = 10
        self.is_dead = False

        # animation
        self.frames = frames
        self.hitbox = pygame.Rect((0,0), (35, 60))
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.index = 0

        # movement
        self.orientation = 'right'
        self.direction = 'right'
        self.status = 'idle'
        self.animation_frames = {'idle' : self.frames}

    

    def move(self):
        if self.status == 'run':
            if self.orientation == 'left':
                self.pos.x -= PLAYER_SPEED
            elif self.orientation == 'right':
                self.pos.x += PLAYER_SPEED
            elif self.orientation == 'up':
                self.pos.y -= PLAYER_SPEED
            elif self.orientation == 'down':
                self.pos.y += PLAYER_SPEED
        self.rect.topleft = self.pos
    

    def attack(self):

        # sword
        self.sword = pygame.Rect((0,0), (45, 30))

        if self.direction == 'left':
            self.sword.midleft = self.rect.midleft 
        else:
            self.sword.midright = self.rect.midright



        # collision
        collided_players = [player for player in self.group[1] if player != self and pygame.sprite.collide_mask(self, player) and self.sword.colliderect(player.hitbox)]
        

        for player in collided_players:
            if not player.cooldown.active and self.status == 'attack':
                player.health_bar.hit(self.dammage)
                player.cooldown.activate()
                if player.health_bar.current_health <= 0:
                    player.is_dead = True

                    
    def animate(self, dt):
        key = f'{self.status}' if f'{self.status}' in self.animation_frames else 'idle'
        current_animation = self.animation_frames[key] if self.direction == 'right' else [pygame.transform.flip(f, True, False) for f in self.animation_frames[key]]

        self.index += dt * ANIMATION_SPEED
        if self.index >= len(current_animation):
            self.index = 0
        
        self.image = current_animation[int(self.index)]
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox.center = self.rect.center


    
    def update(self, dt):
        self.move()
        self.animate(dt)
        self.attack()
        self.cooldown.update()
