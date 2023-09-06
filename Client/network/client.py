

import socket, json, pygame, sys, threading
import time
from classes.settings import *

class Client:
    def __init__(self):
        self.start()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def send(self, message):
        self.socket.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))    
    

    def receive(self):
        return json.loads(self.socket.recv(BUFFER_SIZE).decode())


    def stop(self):
        self.socket.close()
