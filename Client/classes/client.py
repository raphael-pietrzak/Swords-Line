import socket, json, pygame, threading, sys, time
from classes.settings import *
from pygame import Vector2 as vector
from classes.player import Square, Player
from classes.imports import Imports

class Client:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.client_socket = None
        self.running = False
        self.server_data = {}
        self.players = {}
        self.animations = Imports().animations
        self.connect()

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))
        self.running = True
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
            

    def movement(self):
        keys = pygame.key.get_pressed()

        movement = []

        if keys[pygame.K_LEFT]:
            movement.append("left")
        if keys[pygame.K_RIGHT]:
            movement.append("right")
        if keys[pygame.K_UP]:
            movement.append("up")
        if keys[pygame.K_DOWN]:
            movement.append("down")
        
        return movement       

    def handle_server_response(self):
        try:
            while self.running:

                message = {"movement" : self.movement()}
                message = json.dumps(message)

                self.send_data(self.client_socket, message)
                print(f"Message envoyé : {message}")


                response = self.receive_data(self.client_socket)
                self.server_data = response
                print(f"Message recu : {response}")
                self.update_server_data()

                # time.sleep(1)

        finally:
            self.disconnect()
        
    def update_server_data(self):
        for player_id, position in self.server_data.items():
            x, y = position
            if player_id in self.players:
                self.players[player_id].pos = vector((x, y))
            else:
                print(self.animations[3]['frames'])
                player = Player((x, y), self.animations[3]['frames'])
                # player  = Square((x, y))
                self.players[player_id] = player
        


    def send_data(self, socket, data):
        try:
            socket.send(data.encode())
        except:
            print("Erreur d'envoi")
            pass  # Gérer les erreurs d'envoi


    def receive_data(self, socket):
        try:
            data = socket.recv(1024).decode()
            return json.loads(data)
        except:
            print("Erreur de réception")
            return ""  # Gérer les erreurs de réception
    
    def draw(self, dt):
        for player_id, player in self.players.items():
            player.update(dt)


    def update(self, dt):
        print("Update")
        self.display_surface.fill('beige')
        self.event_loop() 
        self.draw(dt)

        # time.sleep(1)
        
