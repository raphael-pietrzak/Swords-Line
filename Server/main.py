import pygame
from screen.home import GameMenu
from classes.settings import *
from screen.editor import Editor

class Main:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("SERVER")

        self.clock = pygame.time.Clock()
        self.menu = GameMenu(self.switch_screen)
        self.screen = self.menu

    def switch_screen(self, screen):
        match screen:
            case 'client': self.screen = Editor(self.switch_screen)
            case 'menu': self.screen = self.menu

    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.screen.update(dt)
            pygame.display.update()



if __name__ == "__main__":
    main = Main()
    main.run()