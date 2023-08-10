from classes.server import Server
import pygame
from classes.settings import *

class Main:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.server = Server()


    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.server.update(dt)



if __name__ == '__main__':
    main = Main()
    main.run()