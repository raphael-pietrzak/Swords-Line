import pygame
from classes.settings import *
from screen.editor import Editor
from screen.mainClient import MainClient

class Main:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("SWORDS LINE")
        self.clock = pygame.time.Clock()
        # self.screen = Editor()
        self.screen = MainClient()

    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.screen.update(dt)
            pygame.display.update()



if __name__ == "__main__":
    main = Main()
    main.run()