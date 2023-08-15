# menus
import pygame, sys
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons
from classes.settings import *



class GameMenu:
    def __init__(self, switch):
        self.display_surface = pygame.display.get_surface()
        self.buttons = ButtonGroup()
        self.create_buttons()
        self.switch_screen = switch

    # input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.menu_click(event)
        
    def menu_click(self, event):
        if self.buttons.hover:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
                for sprite in self.buttons:
                    if sprite.rect.collidepoint(mouse_pos()):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.switch_screen("client")


    # draw
    def create_buttons(self):
        first_pos_y = 300
        margin = 80
        Button((WINDOW_WIDTH/2, first_pos_y), (WINDOW_WIDTH/2, 50), 'Solo', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + margin), (WINDOW_WIDTH/2, 50), 'Multi', self.buttons)
        Button((WINDOW_WIDTH/2, first_pos_y + 2*margin), (WINDOW_WIDTH/2, 50), 'Settings', self.buttons)


    # update
    def update(self, dt):
        self.display_surface.fill(MENU_BG_COLOR)
        self.buttons.update()
        self.event_loop()

    
# groups
class ButtonGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.hover = False

    def is_hovering(self):
        hover = False
        for sprite in self:
            if sprite.rect.collidepoint(mouse_pos()):
                sprite.is_hovering = True
                hover = True
            else:
                sprite.is_hovering = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) if hover else pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.hover = hover
    
    def update(self):
        for sprite in self:
            sprite.draw()
        self.is_hovering()


# components    
class Button(pygame.sprite.Sprite):
    def __init__(self, pos, size, text, group):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.pos = pos
        self.text = text
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(center = self.pos)
        self.is_hovering = False
    
    def draw_text(self):
        self.image.fill(BUTTON_BG_COLOR)
        self.font = pygame.font.Font('graphics/Wood and Paper UI/Font/Supercell-Magic Regular.ttf',30)

        self.text_surf = self.font.render(self.text, True, 'white')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)
        self.display_surface.blit(self.text_surf, self.text_rect)

    def hover(self):
        if self.is_hovering:
            outline = self.rect.copy().inflate(10, 10)
            pygame.draw.rect(self.display_surface, 'white', outline, 4, 5)
    
    def draw(self):
        pos = self.rect.topleft
        self.display_surface.blit(self.image, pos)
        self.draw_text()
        self.hover()
    

class Sign(pygame.sprite.Sprite):
    def __init__(self, pos, size, text, group):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.pos = pos
        self.text = text
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(center = self.pos)
        self.font = pygame.font.Font('graphics/Wood and Paper UI/Font/Supercell-Magic Regular.ttf', 30)

    
    def draw_text(self):
        self.image.fill(BUTTON_BG_COLOR)
        self.text_surf = self.font.render(self.text, True, 'white')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)
        self.display_surface.blit(self.text_surf, self.text_rect)
    
    def toggle(self):
        self.text = 'On' if self.text == 'Off' else 'Off'

    def draw(self):
        pos = self.rect.topleft
        self.display_surface.blit(self.image, pos)
        self.draw_text()



