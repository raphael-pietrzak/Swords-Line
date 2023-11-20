import random
import sys
import pygame
from pygame.math import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons




class Caroussel:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface(self.display_surface.get_size())
        self.rect = self.display_surface.get_rect()
        self.screens = ["shop", "collection", "battle", "clan", "events"]
        self.screens_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
        self.current_screen_index = 0

        self.previous_surface = self.surface.copy()
        self.next_surface = self.surface.copy()

        self.sliding_active = False


        # pagination
        self.pagination_blocks = [Block((i * 100, 0), i) for i in range(len(self.screens))]
        self.pagination_blocks[self.current_screen_index].active = True
        self.pagination_surface = pygame.Surface((len(self.screens) * 100, 100))
        self.pagination_surface.fill('brown')
        self.pagination_rect = self.pagination_surface.get_rect()
        self.pagination_rect.midbottom = self.display_surface.get_rect().midbottom + vector(0, -100)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.previous_screen()
                if event.key == pygame.K_RIGHT:
                    self.next_screen()
            
            self.slide_screen_event(event)
            self.slider_click_event(event)
    

    def slider_click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            if self.pagination_rect.collidepoint(mouse_pos()):
                for block in self.pagination_blocks:
                    if block.rect.collidepoint(mouse_pos() - vector(self.pagination_rect.topleft)):
                        index = block.get_index()
                        self.change_index(index)
    
    def slide_screen_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            self.sliding_active = True
            self.offset = mouse_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            self.sliding_active = False
            self.rect.topleft = (0, 0)

            if self.offset[0] - mouse_pos()[0] > 100:
                self.next_screen()
            elif mouse_pos()[0] - self.offset[0] > 100:
                self.previous_screen()

        if self.sliding_active:
            self.rect.x = mouse_pos()[0] - self.offset[0]
            

    def next_screen(self):
        index = min((self.current_screen_index + 1), len(self.screens) - 1)
        self.change_index(index)

    def previous_screen(self):
        index = max((self.current_screen_index - 1), 0)
        self.change_index(index)

    def change_index(self, index):
        self.pagination_blocks[self.current_screen_index].active = False
        self.current_screen_index = index
        self.pagination_blocks[self.current_screen_index].active = True

    def display_pagination(self):
        pagination = " ".join(["●" if i == self.current_screen_index else "○" for i in range(len(self.screens))])
        print(f"{pagination}")

    def display_current_screen(self):
        current_screen = self.screens[self.current_screen_index]
        print(f"{current_screen}")

    def draw_pagination(self):
        for block in self.pagination_blocks:
            block.draw(self.pagination_surface)
        
        self.display_surface.blit(self.pagination_surface, self.pagination_rect)

    def draw_sides_screens(self):
        color = self.screens_colors[self.current_screen_index]
        self.surface.fill(color)

        previous_color = self.screens_colors[max((self.current_screen_index - 1), 0)] if self.current_screen_index > 0 else color
        self.previous_surface.fill(previous_color)
        previous_rect = self.previous_surface.get_rect(topright = self.rect.topleft)

        next_color = self.screens_colors[min((self.current_screen_index + 1), len(self.screens) - 1)] if self.current_screen_index < len(self.screens) - 1 else color
        self.next_surface.fill(next_color)
        next_rect = self.next_surface.get_rect(topleft = self.rect.topright)

        self.display_surface.blit(self.previous_surface, previous_rect)
        self.display_surface.blit(self.next_surface, next_rect)
    

    def update(self, dt):
        self.event_loop()

        # draw
        self.display_surface.fill('black')
        self.draw_sides_screens()
        
        self.display_surface.blit(self.surface, self.rect)
  
        self.draw_pagination()
        # self.display_current_screen()
        # self.display_pagination()


class Block:
    def __init__(self, pos, index):
        self.pos = pos
        self.index = index
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect.topleft = self.pos
        self.active = False
        # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def get_index(self):
        return self.index

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self.rect)
        color = (255, 255, 255) if self.active else (0, 0, 0)
        pygame.draw.circle(surface, color, self.rect.center, 10)

