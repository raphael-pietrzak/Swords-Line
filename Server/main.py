from server import Server
import pygame
from settings import *

class Main:
    def __init__(self):
        pygame.init()
        self.server = Server()

    
    def run(self):
        self.server.start_server()



if __name__ == '__main__':
    main = Main()
    main.run()