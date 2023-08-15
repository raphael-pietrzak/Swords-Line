from server import Server
import pygame
from settings import *

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.server = Server()

    
    def run(self):
        pass
        while True:
            
            self.server.update()
            pygame.display.update()
        



if __name__ == '__main__':
    main = Main()
    main.run()