



import pygame
from pygame import Vector2 as vector
from classes.settings import *

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        super().__init__()
        # main setup
        self.image = pygame.Surface((150, 70), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.midtop = pos
        self.pos = pos

        # health
        self.max_health = 100
        self.current_health = 100
        self.max_width = 100
        self.current_width = self.max_width * self.current_health / self.max_health 

        # color
        self.font = pygame.font.Font('graphics/Wood and Paper UI/Font/Supercell-Magic Regular.ttf', 15)
        self.border = BLUE_CONTOUR if color == 'blue' else RED_CONTOUR
        self.color = BLUE_PLAYER if color == 'blue' else RED_PLAYER

        # level square
        self.level_rect = pygame.Rect((0, 0), (18, 20))
        self.level_rect.midleft = self.rect.midleft + vector(10, 0)
        self.bg_level_rect = self.level_rect.copy().inflate(-4, -4)


        # black bg
        self.black_bg = pygame.Surface((self.max_width, 10))
        self.black_bg_rect = self.black_bg.get_rect(midleft=self.level_rect.midright + vector(-1, 0))
        self.black_bg.fill('black')
        self.black_bg.set_alpha(80)

        # health rect
        self.health_rect = pygame.Rect((0, 0), (self.current_width, 7))
        self.health_rect.midleft = self.level_rect.midright + vector(-3, -1)

        # level number
        self.level_number = self.font.render(str(15), True, 'white')
        self.level_number_shadow = self.font.render(str(15), True, self.border)
        self.level_text_border = pygame.transform.scale(self.level_number_shadow, self.level_number_shadow.get_size() + vector(4, 4))
        self.level_number_rect = self.level_number.get_rect(center=self.level_rect.center + vector(0, -5))



    

    def draw(self, surface):
        surface.blit(self.black_bg, self.black_bg_rect)
        pygame.draw.rect(surface, self.border, self.black_bg_rect, 2, 2)
        pygame.draw.rect(surface, self.color, self.health_rect)

        pygame.draw.rect(surface, self.border, self.level_rect, 2, 2)
        pygame.draw.rect(surface, self.color, self.bg_level_rect)

        surface.blit(self.level_number_shadow, self.level_number_rect.move(0,3))
        surface.blit(self.level_text_border, self.level_number_rect.move(-2,-2))
        surface.blit(self.level_number, self.level_number_rect)

        # pygame.draw.rect(surface, 'purple', self.rect, 2)
    



class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.healthbar = HealthBar('blue', (400,400))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            
            self.display_surface.fill('beige')

            # axes
            pygame.draw.line(self.display_surface, 'purple', (400, 0), (400, WINDOW_HEIGHT))
            pygame.draw.line(self.display_surface, 'purple', (0, 400), (WINDOW_WIDTH, 400))
            
            # healthbar
            self.healthbar.draw(self.display_surface)


            pygame.display.update()














if __name__ == '__main__':
    game = Main()
    game.run()