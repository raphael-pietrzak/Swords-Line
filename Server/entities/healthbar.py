
# MODULE Head-Up Display

from typing import Any
import pygame
from classes.settings import *
from pygame import Vector2 as vector

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((120, 30), pygame.SRCALPHA)
        self.pos = (18, 10)

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
        self.rect = pygame.Rect(self.pos, (self.max_width, 10))
        self.level_rect = pygame.Rect(self.rect.topleft, (18, 20))

        
    
    def draw_bar(self):
        self.image = pygame.Surface((120, 30), pygame.SRCALPHA)

        # support
        self.image.blit(self.black_bg, self.rect)
        pygame.draw.rect(self.image, self.border, self.rect, 2, 2)

        # health
        self.health_rect = pygame.Rect(self.rect.topleft, (self.current_health, 7)).move(0, 1)
        self.health_rect.left = self.rect.left -2
        pygame.draw.rect(self.image, self.color, self.health_rect, 8)

        # level square
        self.level_rect.midright = self.rect.midleft + vector(2, 0)
        pygame.draw.rect(self.image, self.border, self.level_rect, 2, 2)
        bg_level_rect = self.level_rect.copy().inflate(-4, -4)
        pygame.draw.rect(self.image, self.color, bg_level_rect, 20)

        # level text 
        level = str(15)
        offset = vector(0, -5)

        level_text = self.font.render(level, True, 'white')
        level_text_shadow = self.font.render(level, True, self.border)
        level_text_border = pygame.transform.scale(level_text_shadow, level_text_shadow.get_size() + vector(4, 4))
        
        self.level_rect = level_text.get_rect(center=self.level_rect.center + offset)
        level_text_border_rect = level_text_border.get_rect(center=self.level_rect.center)
        level_text_shadow_rect = level_text_shadow.get_rect(center=self.level_rect.center).move(0,3)

        self.image.blit(level_text_border, level_text_border_rect)
        self.image.blit(level_text_shadow, level_text_shadow_rect)
        self.image.blit(level_text, self.level_rect)
    
    def update(self):
        self.draw_bar()











class TreeBreakBar:
    def __init__(self, pos):
        self.progress = 0
        self.max_width = 100
        self.image = pygame.display.get_surface()
        self.rect = pygame.Rect(pos, (self.max_width, 10))
        self.rect.midtop = pos
        self.ended = False
    
    def hit(self, damage):
        self.progress += damage
        self.progress = min(self.progress, self.max_width)
        if self.progress >= self.max_width:
            self.ended = True

    def draw(self, offset):
        pos = self.rect.topleft + offset
        rect = self.rect.copy()
        rect.topleft = pos
        pygame.draw.rect(self.image, 'black', rect, 2)
        current_width = self.max_width * self.progress / self.max_width
        rect.width = current_width
        pygame.draw.rect(self.image, 'red', rect, 2)
    
