import socket, json, pygame, sys, time
from classes.settings import *
from pygame import Vector2 as vector
from player.player import Player
from player.animated import Animated
from classes.imports import Imports
from classes.camera import CameraGroup
from random import randint

class Client:
    def __init__(self):
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.animations = Imports().animations
        self.all_sprites = CameraGroup()

        # players
        self.players = {}

        # client
        self.inputs = []

        # server
        self.server_data = {}
        self.players_data = {}
        self.uuid = 0
        self.trees = []


        # socket
        self.client_socket = None
        self.connect()

        self.init_data()



    def init_data(self):
        while not self.server_data:
            self.server_data = self.get_server_data()
            
        self.uuid = self.server_data["uuid"]
        for pos in self.server_data["trees"]:
            self.trees.append(Animated(pos, self.animations[5]['frames'], self.all_sprites))

        Animated((300, 200), self.animations[1]['frames'], self.all_sprites)
        Animated((200, 400), self.animations[2]['frames'], self.all_sprites)


    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"\nConnecté au serveur {SERVER_IP} sur le port {SERVER_PORT}\n")


    def disconnect(self):
        print("\nConnexion fermée\n")
        self.client_socket.close()
        pygame.quit()
        sys.exit()


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\nConnexion fermée\n")
                self.client_socket.close()
                pygame.quit()
                sys.exit()
            
            self.get_keyboard_inputs()
            

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
        if keys[pygame.K_SPACE]:
            self.inputs.append("attack")
        

    def handle_server_response(self):
        # send
        message = {"inputs" : self.inputs}
        self.send_to_server(message)

        # receive
        self.server_data = self.get_server_data()

        if not self.server_data:
            return

        # update
        self.players_data = self.server_data["players"]




    def update_players(self):
        players_to_remove = {player_id for player_id in self.players.keys() if player_id not in self.players_data}
        
        for player_id in players_to_remove:
            player = self.players.pop(player_id)
            self.all_sprites.remove(player)
            
        for player_id, player_data in self.players_data.items():
            if player_id in self.players:
                self.players[player_id].refresh_data(player_data)
            else:
                self._create_new_player(player_id, player_data)


    def _create_new_player(self, player_id, player_data):
        x, y = player_data['position']
        player = Player((x, y), self.animations[3]['frames'], self.all_sprites)
        self.players[player_id] = player



    def send_to_server(self, data):
        try:
            data = json.dumps(data)
            self.client_socket.send(data.encode())

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.disconnect()



    def get_server_data(self):
        try:
            raw_data = self.client_socket.recv(BUFFER_SIZE).decode()
            if not raw_data:
                return None  # No data received

            data = json.loads(raw_data)
            return data
        
        except json.JSONDecodeError as json_error:

            print(f"Erreur de décodage JSON lors de la réception des données du serveur : {raw_data}")
            return None




    def update(self, dt):
        self.event_loop() 
        self.handle_server_response()
        self.update_players()
        self.all_sprites.update(dt)
        
        # draw
        self.display_surface.fill('beige')
        self.all_sprites.custom_draw(self.players[self.uuid].rect.center, self.players.values())


