
import socket, json, pygame, sys, time
from classes.settings import *
from pygame import Vector2 as vector
from player.player import Player
from player.animated import Animated
from classes.imports import Imports
from classes.camera import CameraGroup
from random import randint, choice
from player.ressources import Ressource

class Client:
    def __init__(self):
        self.client_socket = None
        self.connect()


    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"\nConnecté au serveur {SERVER_IP} sur le port {SERVER_PORT}\n")


    def disconnect(self):
        print("\nConnexion fermée\n")
        self.client_socket.close()
        pygame.quit()
        sys.exit()


    def send_to_server(self, data):
        try:
            data = json.dumps(data)
            self.client_socket.send(data.encode())

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.disconnect()


    def get_server_data(self):
        try:
            raw_data = ""
            size = 0
            while raw_data[-1:] != '}' and size < 10:
                raw_data += self.client_socket.recv(BUFFER_SIZE).decode()
                size += 1
            if not raw_data:
                return None  # No data received

            data = json.loads(raw_data)
            return data
        
        except json.JSONDecodeError as json_error:

            print(f"Erreur de décodage JSON lors de la réception des données du serveur : {raw_data}")
            return None
        


