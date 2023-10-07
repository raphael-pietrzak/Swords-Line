from settings import *

import sys, pygame

from network.server import Server
from classes.ping import FPSCounter





class Main:
    def __init__(self):
        
        # server
        self.server = Server()

        # display
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('SERVER')

        self.players = []

        # ping
        self.fps_counter = FPSCounter('MAIN')

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.server.close()
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('[ EVENT ] : Return pressed')
                    self.server.send('Server Pressed Return', 'TCP')

            
    def draw(self):

        self.update_players()
        for player in self.players:
            player.move(player.inputs)

            pygame.draw.rect(self.display_surface, player.color, (player.get_position()[0], player.get_position()[1], 40, 40))


    def update_players(self):
        clients = self.server.receive('UDP')
        self.players = []
        message = {}
        for adress, client in clients.items():
            self.players.append(client.player)
            message[client.uuid] = {'pos' : client.player.get_position(), 'color' : client.player.color}
        
        self.server.send(message, 'UDP')

        
    
    def run(self):
        # event
        self.event_loop()

        # drawing
        self.display_surface.fill('beige')
        self.draw()

        # update
        self.fps_counter.ping()
        pygame.display.update()


if __name__ == "__main__":
    main = Main()
    while True:
        main.run()
        