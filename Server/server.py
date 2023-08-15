
import socket, threading
from settings import *
from random import randint
from handler import ClientHandler
import pygame
from pygame import Vector2 as vector

from player import Gold

class Server:
    def __init__(self):
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.server_socket = None
        self.lock = threading.Lock()

        # groups
        self.gold_sprites = CameraGroup()

        # clients
        self.clients = [] 
        self.server_data = {}
        self.gold_collected = []
        self.server_data["players"] = {}


        self.generate_map()
        self.start_server()

    
    def generate_map(self):
        self.trees = []
        self.gold = []
        for _ in range(100):
            self.trees.append([randint(-900, 900), randint(-900, 900)])
            pos = [randint(-900, 900), randint(-900, 900)]
            Gold(pos, self.gold_sprites)
            self.gold.append(pos)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_server()

    # start - stop
    def start_server(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()
        print(f"\nServeur en ligne sur le port {PORT}\n")

        self.accept_clients_thread = threading.Thread(target=self.accept_clients)
        self.accept_clients_thread.start()

    
    def stop_server(self):
        if self.server_socket:
            self.running = False
            self.server_socket.close()

            print("Serveur fermé")


    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"Nouvelle connexion de {addr[0]} : {addr[1]}")

                client_handler_thread = ClientHandler(self, client_socket, addr)
                client_handler_thread.start()

                self.clients.append(client_handler_thread)

            except OSError:
                pass
    

    def extract_server_data(self, player, uuid, ):
        self.server_data['type'] = "player"
        self.server_data["players"][uuid] = {
            "position" : [int(player.pos.x), int(player.pos.y)],
            "status" : player.status,
            "direction" : player.direction,
            "health" : player.health,
            "damage" : player.damage,
            "gold" : player.gold_count
        }
        self.server_data["gold"] = {
            "collected" : self.gold_collected
        }

        return self.server_data
    

    def init_client_data(self, uuid):
        data = {}

        data['type'] = "init"
        data["trees"] = self.trees
        data["gold"] = self.gold
        data["uuid"] = uuid
        return data


    
    def remove_client(self, client):
        self.clients.remove(client)
        self.server_data["players"].pop(client.uuid)
    
    def update(self):
        self.display_surface.fill('beige')
        with self.lock:
            for client in self.clients:
                client.player.image.fill('red')
                self.display_surface.blit(client.player.image, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))


        if self.server_data["players"]:
            for player in self.server_data["players"].values():
                pos = player["position"]
        else:
            pos = (0, 0)

        self.gold_sprites.custom_draw(pos)
        
        self.event_loop()
        
    
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector(0, 0)
        self.display_surface = pygame.display.get_surface()
    
    def custom_draw(self, position):
        position = vector(position)
        self.offset.x = WINDOW_WIDTH // 2 - position.x
        self.offset.y = WINDOW_HEIGHT // 2 - position.y

        for sprite in self.sprites():
            pos = sprite.pos + self.offset
            self.display_surface.blit(sprite.image, pos)


    



