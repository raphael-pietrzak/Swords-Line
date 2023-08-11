import socket, json, pygame, threading, sys, time
from classes.settings import *
from pygame import Vector2 as vector
from classes.player import Player, Animated
from classes.imports import Imports
from classes.camera import CameraGroup

class Client:
    def __init__(self):
        # main setup
        self.display_surface = pygame.display.get_surface()

        # players
        self.players = {}
        self.uuid = 0
        self.all_sprites = CameraGroup()

        # server
        self.client_socket = None
        self.running = False
        self.server_data = {}
        self.connect()

        # thread
        self.lock = threading.Lock()

        # animations
        self.animations = Imports().animations
        Animated((200, 200), self.animations[5]['frames'], self.all_sprites)
        Animated((300, 200), self.animations[1]['frames'], self.all_sprites)
        Animated((200, 400), self.animations[2]['frames'], self.all_sprites)




    def connect(self):
        self.running = True
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"\nConnecté au serveur {SERVER_IP} sur le port {SERVER_PORT}\n")

        self.server_handler_thread = threading.Thread(target=self.handle_server_response)
        self.server_handler_thread.start()

    def disconnect(self):
        self.client_socket.close()
        self.running = False
        print("\nConnexion fermée\n")


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            

    def get_keyboard_inputs(self):
        keys = pygame.key.get_pressed()

        inputs = []

        if keys[pygame.K_LEFT]:
            inputs.append("left")
        if keys[pygame.K_RIGHT]:
            inputs.append("right")
        if keys[pygame.K_UP]:
            inputs.append("up")
        if keys[pygame.K_DOWN]:
            inputs.append("down")
        if keys[pygame.K_SPACE]:
            inputs.append("attack")
        
        return inputs       

    def handle_server_response(self):
        try:
            while self.running:

                message = {
                    "inputs" : self.get_keyboard_inputs(),
                }
                message = json.dumps(message)

                self.send_data(self.client_socket, message)

                response = self.receive_data(self.client_socket)
                self.server_data = response["players"]
                self.uuid = response["uuid"]

                with self.lock:
                    self.update_server_data()


        finally:
            self.disconnect()
        
    def update_server_data(self):
        players_to_remove = [player_id for player_id, player in self.players.items() if player_id not in self.server_data]
        for player_id in players_to_remove:
            del self.players[player_id]

        for player_id, player_data in self.server_data.items():
            if player_id in self.players:
                self.players[player_id].refresh_data(player_data)
            else:
                x, y = player_data['position']
                player = Player((x, y), self.animations[3]['frames'], self.all_sprites)
                self.players[player_id] = player
        


    def send_data(self, socket, data):
        try:
            socket.send(data.encode())
        except:
            print("Erreur d'envoi")
            pass  


    def receive_data(self, socket):
        try:
            data = socket.recv(1024).decode()
            return json.loads(data)
        except:
            print("Erreur de réception")
            return "" 


    def update(self, dt):
        self.display_surface.fill('beige')
        self.event_loop() 
        with self.lock:
            self.all_sprites.update(dt)
        
            # self.all_sprites.custom_draw(self.players[self.uuid].rect.center)
        self.all_sprites.draw(self.display_surface)
