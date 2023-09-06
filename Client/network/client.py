

import socket, json, pygame, sys, threading
import time
from classes.settings import *

# DATA must be formated as JSON

class Client:
    def __init__(self):
        self.server_data = None
        self.lock = threading.Lock()
        self.start()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()


    def send(self, message):
        self.socket.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))    
    

    def receive(self):
        with self.lock:
            self.server_data = json.loads(self.socket.recv(BUFFER_SIZE).decode())

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def get_server_data(self):
        with self.lock:
            return self.server_data


    def stop(self):
        self.socket.close()
