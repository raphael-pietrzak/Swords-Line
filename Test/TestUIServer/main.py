from ui.tabbed_server import TabbedServerUI
import pygame
from settings import WIDTH, HEIGHT
from management.server_data import ServerData


class Main:
    def __init__(self):
        # Initialisation de pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Swords Line - Serveur")
        self.clock = pygame.time.Clock()
        self.running = True


        # Données du serveur (simulation)
        self.server_data = ServerData() # Contient les logs, les salles, les joueurs
        self.server_data.generate_demo_data()
    
        self.ui = TabbedServerUI(self.server_data)

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    main = Main()
    main.run()
