import pygame
from src.main import Game

class Main:
    def __init__(self):
        self.game = Game()

    def run(self):
        self.game.run()


if __name__ == '__main__':
    main = Main()
    main.run()
    pygame.quit()