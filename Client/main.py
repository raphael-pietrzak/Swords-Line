import pygame
from classes.settings import *
from classes.client import Client

class Main:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        self.client = Client()
    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.client.update(dt)
            pygame.display.update()



if __name__ == "__main__":
    main = Main()
    main.run()