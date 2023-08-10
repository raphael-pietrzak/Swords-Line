import socket, json, pygame, threading, sys, time
from classes.settings import *
from pygame import Vector2 as vector

class Client:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.client_socket = None
        self.running = False
        self.server_data = {}
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
                self.server_data = json.loads(response)
                print(f"Message recu : {response}")

                # time.sleep(1)

        finally:
            self.disconnect()
        


    def send_data(self, socket, data):
        try:
            socket.send(data.encode())
        except:
            print("Erreur d'envoi")
            pass  # Gérer les erreurs d'envoi


    def receive_data(self, socket):
        try:
            data = socket.recv(1024).decode()
            return data
        except:
            print("Erreur de réception")
            return ""  # Gérer les erreurs de réception
    
    def draw(self):

        for key, value in self.server_data.items():

            pos = vector(value)
            rect = pygame.Rect(pos.x, pos.y, 50, 50)
            pygame.draw.rect(self.display_surface, BLUE_CONTOUR, rect)


    def update(self, dt):
        # time.sleep(1)
        self.display_surface.fill('beige')
        self.event_loop() 
        self.draw()

        
