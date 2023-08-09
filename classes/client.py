import socket
from classes.settings import *
import time

class Client:
    def __init__(self):
        self.connect()

    def connect(self):
        print("Connecting to Server...")
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))

        print("Connected to Server")

    def disconnect(self):
        self.client_socket.close()

        print("Disconnected from Server")

    def receive(self):
        # time.sleep(0.1)
        return self.client_socket.recv(1024).decode()

    def send(self, data):
        if data == '[DISCONNECT]':
            self.disconnect()
            return

        # Envoyez des données au serveur (par exemple, les mouvements du joueur)
        # data += ' ' * (1024 - len(data))
        data = data.encode()
        self.client_socket.send(data)

        # Reçois des données du serveur
        # print(self.receive())
