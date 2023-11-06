import pygame

from pygame import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons

from classes.settings import *
from menu.menu import Button, ButtonGroup




class EndPartySurface:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((WINDOW_WIDTH/2, WINDOW_WIDTH/2), pygame.SRCALPHA)
        self.switch_screen = switch
        self.rect = self.surface.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.drawing_rect = self.surface.get_rect(topleft = (0, 0))
        self.surface.set_alpha(220)

        self.title_label = Label('Game Over', self.rect.midtop + vector(0, 50), 50)
        self.kill_stats = Stats('Kills: ', 0, self.rect.topleft + vector(30, 200), 30)
        self.death_stats = Stats('Deaths: ', 40, self.rect.topleft + vector(30, 270), 30)
        self.damage_stats = Stats('Damage: ', 8679, self.rect.topleft + vector(30, 340), 30)

        self.buttons = ButtonGroup()

        self.return_button = Button((self.rect.bottomleft + vector(120, -80)), (180, 80), 'Return', self.buttons)
        self.play_again_button = Button((self.rect.bottomright + vector(-180, -80)), (300, 80), 'Play Again', self.buttons)

    

    def event_loop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            if self.return_button.rect.collidepoint(mouse_pos()):
                self.switch_screen("home")
            if self.play_again_button.rect.collidepoint(mouse_pos()):
                self.switch_screen("client")
    
        

    def draw(self):
        # self.surface.fill(MENU_BG_COLOR)
        pygame.draw.rect(self.surface, MENU_BG_COLOR, self.drawing_rect, border_radius=10)
        self.display_surface.blit(self.surface, self.rect)
        self.title_label.draw()
        self.kill_stats.draw()
        self.death_stats.draw()
        self.damage_stats.draw()
        self.buttons.draw()


class Label:
    def __init__(self, text, pos, font_size):
        self.font = pygame.font.Font('graphics/Wood and Paper UI/Font/Supercell-Magic Regular.ttf', font_size)
        self.text_surf = self.font.render(text, True, 'white')
        self.text_rect = self.text_surf.get_rect(center = pos)
        self.display_surface = pygame.display.get_surface()
    
    def generic_draw(self, surface):
        surface.blit(self.text_surf, self.text_rect)
    
    def draw(self):
        self.display_surface.blit(self.text_surf, self.text_rect)


class Stats:
    def __init__(self, key, value, pos, font_size):
        self.display_surface = pygame.display.get_surface()

        self.key = key
        self.value = value

        # text
        self.font = pygame.font.Font('graphics/Wood and Paper UI/Font/Supercell-Magic Regular.ttf', font_size)

        self.text_surf_key = self.font.render(key, True, 'white')
        self.key_rect = pygame.Rect(pos, (300, 50))
        self.text_rect_key = self.text_surf_key.get_rect(midleft = self.key_rect.midleft + vector(10, 0))

        self.text_surf_value = self.font.render(str(value), True, 'white')
        self.value_rect = pygame.Rect(self.key_rect.topright + vector(90, 0), (150, 50))
        self.text_rect_value = self.text_surf_value.get_rect(center = self.value_rect.center)
        

    def draw(self):
        pygame.draw.rect(self.display_surface, END_GAME_SURFACE_COLOR, self.key_rect, border_radius=5)
        self.display_surface.blit(self.text_surf_key, self.text_rect_key)

        pygame.draw.rect(self.display_surface, END_GAME_SURFACE_COLOR, self.value_rect, border_radius=5)
        self.display_surface.blit(self.text_surf_value, self.text_rect_value)



