from typing import Any
import pygame
from classes.settings import *
from pygame import Vector2 as vector
from classes.timer import Cooldown
from random import randint

class Animated(pygame.sprite.Sprite):
    def __init__(self, frames, pos, group):
        self.display_surface = pygame.display.get_surface()
        super().__init__(group)
        self.image = frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.frames = frames
        self.index = 0

    def animate(self, dt):
        self.index += dt * ANIMATION_SPEED
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]


    def update(self, dt):
        self.animate(dt)








class Player(pygame.sprite.Sprite):
    def __init__(self, frames, pos, group):
        super().__init__(group)

        self.display_surface = pygame.display.get_surface()

        # main
        self.id = 0
        self.group = group

        # attack
        self.cooldown = Cooldown(200)
        self.dammage = 10
        self.is_dead = False
        # self.dead_sprites = pygame.sprite.Group()
        # self.dead_frames = dead_frames

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
                self.rect.x -= PLAYER_SPEED
            elif self.orientation == 'right':
                self.rect.x += PLAYER_SPEED
            elif self.orientation == 'up':
                self.rect.y -= PLAYER_SPEED
            elif self.orientation == 'down':
                self.rect.y += PLAYER_SPEED
    

    def attack(self):
        self.sword = pygame.Rect((0,0), (45, 30)) 
        if self.direction == 'left':
            self.sword.midleft = self.rect.midleft 
        else:
            self.sword.midright = self.rect.midright

        # pygame.draw.rect(self.display_surface, 'red', self.sword)

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
        # pygame.draw.rect(self.display_surface, 'green', self.rect)        
        self.attack()
        self.cooldown.update()



class Gobelin(Player):
    def __init__(self, frames, pos, group):
        super().__init__(frames, pos, group)
        self.id = 1
        self.pressed_keys = set()
        self.health_bar = HealthBar(self.rect.topleft, 'red')
        self.animation_frames = {
            'idle': self.frames[:7],
            'run': self.frames[7:13], 
            'attack': self.frames[13:],
        }

    def event_loop(self, event):
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)

        if pygame.K_LEFT in self.pressed_keys:
            self.orientation = 'left'
            self.direction = 'left'
            self.status = 'run'
        elif pygame.K_RIGHT in self.pressed_keys:
            self.orientation = 'right'
            self.direction = 'right'
            self.status = 'run'
        elif pygame.K_UP in self.pressed_keys:
            self.orientation = 'up'
            self.status = 'run'
        elif pygame.K_DOWN in self.pressed_keys:
            self.orientation = 'down'
            self.status = 'run'
        elif pygame.K_EQUALS in self.pressed_keys:
            self.status = 'attack'
        else:
            self.status = 'idle'
    
    def update(self, dt):
        super().update(dt)
        self.health_bar.update(self.rect.midtop)


class Knight(Player):
    def __init__(self, frames, pos, group):
        super().__init__(frames, pos, group)
        self.id = 2
        self.pressed_keys = set()
        self.dammage = 10
        self.health_bar = HealthBar(self.rect.topleft, 'blue')
        self.animation_frames = {
            'idle': self.frames[:6],
            'run': self.frames[6:12], 
            'attack': self.frames[12:],
        }

    def event_loop(self, event):
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)

        if pygame.K_q in self.pressed_keys:
            self.orientation = 'left'
            self.direction = 'left'
            self.status = 'run'
        elif pygame.K_d in self.pressed_keys:
            self.orientation = 'right'
            self.direction = 'right'
            self.status = 'run'
        elif pygame.K_z in self.pressed_keys:
            self.orientation = 'up'
            self.status = 'run'
        elif pygame.K_s in self.pressed_keys:
            self.orientation = 'down'
            self.status = 'run'
        elif pygame.K_a in self.pressed_keys:
            self.status = 'attack'
        else:
            self.status = 'idle'
    
    def update(self, dt):
        super().update(dt)
        self.health_bar.update(self.rect.midtop)

    

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        self.display_surface = pygame.display.get_surface()
        super().__init__()

        # health
        self.max_health = 100
        self.current_health = 100
        self.max_width = 100
        self.current_width = self.max_width * self.current_health / self.max_health 

        # color
        self.font = pygame.font.Font('graphics/Wood and Paper UI/Font/Supercell-Magic Regular.ttf', 15)
        self.border = BLUE_CONTOUR if color == 'blue' else RED_CONTOUR
        self.color = BLUE_PLAYER if color == 'blue' else RED_PLAYER

        # black bg
        self.black_bg = pygame.Surface((self.max_width, 10))
        self.black_bg.fill('black')
        self.black_bg.set_alpha(80)

        # rect
        self.rect = pygame.Rect(pos, (self.max_width, 10))
        self.level_rect = pygame.Rect(self.rect.topleft, (18, 20))


    def hit(self, damage):
        self.current_health -= damage if self.current_health - damage >= 0 else 0
    
    def draw(self):
        # support
        self.display_surface.blit(self.black_bg, self.rect)
        pygame.draw.rect(self.display_surface, self.border, self.rect, 2, 2)

        # health
        self.health_rect = pygame.Rect(self.rect.topleft, (self.current_health, 7)).move(0, 1)
        self.health_rect.left = self.rect.left -2
        pygame.draw.rect(self.display_surface, self.color, self.health_rect, 8)

        # level square
        self.level_rect.midright = self.rect.midleft + vector(2, 0)
        pygame.draw.rect(self.display_surface, self.border, self.level_rect, 2, 2)
        bg_level_rect = self.level_rect.copy().inflate(-4, -4)
        pygame.draw.rect(self.display_surface, self.color, bg_level_rect, 20)

        # level text 
        level = str(15)
        offset = vector(0, -5)

        level_text = self.font.render(level, True, 'white')
        level_text_shadow = self.font.render(level, True, self.border)
        level_text_border = pygame.transform.scale(level_text_shadow, level_text_shadow.get_size() + vector(4, 4))
        
        self.level_rect = level_text.get_rect(center=self.level_rect.center + offset)
        level_text_border_rect = level_text_border.get_rect(center=self.level_rect.center)
        level_text_shadow_rect = level_text_shadow.get_rect(center=self.level_rect.center).move(0,3)

        self.display_surface.blit(level_text_border, level_text_border_rect)
        self.display_surface.blit(level_text_shadow, level_text_shadow_rect)
        self.display_surface.blit(level_text, self.level_rect)

    def update(self, pos):
        self.rect.midtop = pos
        if self.current_health < self.max_health:
            self.draw()

        
        

