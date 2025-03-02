import pygame
from network.client import NetworkClient
from controllers.game_controller import GameController

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Swords Line")
    clock = pygame.time.Clock()

    network_client = NetworkClient()
    game_controller = GameController(network_client, screen)

    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_controller.handle_event(event)

        game_controller.update()
        game_controller.draw()
        pygame.display.flip()

    network_client.disconnect()
    pygame.quit()

if __name__ == "__main__":
    main()