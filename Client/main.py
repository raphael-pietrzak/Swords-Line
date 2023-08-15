import pygame
from classes.menu import GameMenu
from classes.settings import *
from classes.client import Client

class Main:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        self.client = Client(self.switch_screen)
        self.menu = GameMenu(self.switch_screen)
        self.screen = self.menu

    def switch_screen(self, screen):
        match screen:
            case 'client': self.screen = self.client
            case 'menu': self.screen = self.menu

    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.screen.update(dt)
            pygame.display.update()



if __name__ == "__main__":
    main = Main()
    main.run()