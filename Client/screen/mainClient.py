import json, socket, sys, threading, time, pygame
from network.client import Client
from classes.ping import FPSCounter
from classes.settings import *
from entities.player import Gobelin, Knight
from classes.imports import Graphics
        


class MainClient:
    def __init__(self):

        self.fps_counter = FPSCounter('MAIN')

        pygame.init()
        self.client = Client()
        self.players = {}

        self.animations = Graphics().animations
        self.players_sprites = pygame.sprite.Group()

        self.inputs = []

        
        self.display_surface = pygame.display.get_surface()
        pygame.display.set_caption('CLIENT')


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.client.close()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('[ EVENT ] : Return pressed')
                    self.client.send('Client Pressed Return', 'TCP')
                    if not self.client.is_online():
                        self.client.start()
                        


    def get_keyboard_inputs(self):
        keys = pygame.key.get_pressed()

        self.inputs = []

        if keys[pygame.K_LEFT]:
            self.inputs.append("left")
        if keys[pygame.K_RIGHT]:
            self.inputs.append("right")
        if keys[pygame.K_UP]:
            self.inputs.append("up")
        if keys[pygame.K_DOWN]:
            self.inputs.append("down")
        if keys[pygame.K_RMETA] and not self.inputs:
            self.inputs.append("attack")

    


    def draw(self):
        players = self.client.receive('UDP')

        for uuid, player_data in players.items():
            if uuid not in self.players:
                new_player = None
                match player_data['faction']:
                    case 'goblin': new_player = Gobelin(player_data['pos'], self.animations['goblin'], self.players_sprites)
                    case 'knight': new_player = Knight(player_data['pos'], self.animations['knight'], self.players_sprites)
                    case _: new_player = Gobelin(player_data['pos'], self.animations['goblin'], self.players_sprites)
                self.players[uuid] = new_player
            else:
                self.players[uuid].update_data(player_data)






    def update(self, dt):
        # Ping

        self.event_loop()
        self.display_surface.fill('aquamarine3')

        self.get_keyboard_inputs()
        self.client.send({'inputs': self.inputs}, 'UDP')

        self.draw()
        
        self.players_sprites.update(dt)
        self.players_sprites.draw(self.display_surface)

        self.fps_counter.ping()




