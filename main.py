import pygame
from classes.editor import Editor
from classes.settings import *
from classes.client import Client


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        self.editor = Editor()
        self.client1 = Client()
        self.client2 = Client()
        self.client3 = Client()
        self.data_1 = 'Client 1 : 1111'
        self.data_2 = 'Client 2 : 2222'
        self.data_3 = 'Client 3 : 3333'

    
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.editor.update(dt)
            pygame.display.update()
            self.client1.send(self.data_1)
            self.client2.send(self.data_2)
            self.client3.send(self.data_3)




if __name__ == '__main__':
    main = Main()
    main.run()