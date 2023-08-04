import pygame
from classes.editor import Editor
from classes.settings import *


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        self.editor = Editor()

    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.editor.update(dt)
            pygame.display.update()




if __name__ == '__main__':
    main = Main()
    main.run()