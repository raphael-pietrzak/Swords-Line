
import pygame
from pygame import Vector2 as vector
from pygame.image import load

class MenuItemsGroup:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.pos = vector(30, 40)
        self.image = pygame.Surface((200, 300))
        self.rect = self.image.get_rect(topleft = self.pos)
        self.bg_color = '#1C1E21'
        self.border_radius = 5
        self.create_buttons()
    
    def create_buttons(self):
        buttons_nb = 3
        size = (self.rect.width, self.rect.height//buttons_nb)
        pos = self.rect.topleft
        self.generic_wallet_rect = pygame.Rect(pos, size)
        self.log_wallet_rect = self.generic_wallet_rect.copy().inflate(-10, -10)
        self.gold_wallet_rect = self.generic_wallet_rect.copy().inflate(-10, -10).move(0, size[1])
        self.pinecone_wallet_rect = self.generic_wallet_rect.copy().inflate(-10, -10).move(0, 2 * size[1])

        log = load('graphics/Ressources/Log.png')
        gold = load('graphics/Ressources/Gold.png')
        pinecone = load('graphics/Ressources/Pinecone.png')

        self.buttons = []

        MenuItem(self.log_wallet_rect, log, self.buttons)
        MenuItem(self.gold_wallet_rect, gold, self.buttons)
        MenuItem(self.pinecone_wallet_rect, pinecone, self.buttons)
    
    def update(self, data):
        self.buttons[0].count = data['log']
        self.buttons[1].count = data['gold']
        self.buttons[2].count = data['pinecone']

    def draw(self):
        pygame.draw.rect(self.display_surface, self.bg_color, self.rect, border_radius=self.border_radius)
        for button in self.buttons:
            button.draw()




class MenuItem:
    def __init__(self, rect, image, group):
        self.display_surface = pygame.display.get_surface()
        self.rect = rect
        self.image = image
        group.append(self)
        self.count = 0
    
    def draw_text(self):
        text = str(self.count)
        self.font = pygame.font.Font('graphics/Wood and Paper UI/Font/Supercell-Magic Regular.ttf', 30)
        self.text_surf = self.font.render(text, True, 'white')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)
        self.display_surface.blit(self.text_surf, self.text_rect)

    def draw(self):
        pygame.draw.rect(self.display_surface, 'grey', self.rect)
        self.display_surface.blit(self.image, self.rect)
        self.draw_text()


