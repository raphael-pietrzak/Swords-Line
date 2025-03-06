from ui.tabbed_server import TabbedServerUI
import pygame
from network.server import GameServer


class Main:
    def __init__(self):
        # Initialisation de pygame
        pygame.init()
        pygame.font.init()
       
       
        self.server = GameServer()
        self.ui = TabbedServerUI(self.server)

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    main = Main()
    main.run()
