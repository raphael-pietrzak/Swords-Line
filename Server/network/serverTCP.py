import json
import socket
import threading
import time
from Network.Server.client import Client

from settings import *


class TCPServer(threading.Thread):
    def __init__(self, clients):
        super().__init__()
        self.client_handlers = [] 
        self.clients = clients

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    
    def start(self):
        self.bind()
        print(f"Serveur TCP en écoute sur {HOST}:{TCP_PORT} ...")
        self.server_socket.listen(5)  # Permet jusqu'à 5 connexions simultanées
        super().start()
    

    def bind(self):
        while True:
            try:
                self.server_socket.bind((HOST, TCP_PORT))
                break
            except OSError:
                time.sleep(1)


    def run(self):
        try:
            while True:
                client_socket, adress = self.server_socket.accept()
                print("Nouvelle connexion établie :", adress)

                client_handler = ClientHandler(client_socket, adress, self)
                client_handler.start()
                self.client_handlers.append(client_handler)
        except ConnectionAbortedError:
            self.close()
    
    def send(self, message):
        for client in self.client_handlers:
            client.send(message)

    def remove_client(self, client):
        if client in self.client_handlers:
            self.client_handlers.remove(client)
            self.clients.pop(client.uuid)
            print(f"Client {client.adress} déconnecté")


    def close(self):
        for client in self.client_handlers:
            client.close()
        self.server_socket.close()



class ClientHandler(threading.Thread):
    def __init__(self, client_socket, adress, server):
        super().__init__()
        self.is_running = True
        self.uuid = None
        self.client_data = {}
        self.client_socket = client_socket
        self.client_socket.settimeout(1.0)
        self.adress = adress
        self.server = server

    def run(self):
            while self.is_running:
                try:
                    data = self.client_socket.recv(1024)
                    if not data: break 
                    # DEBUG
                    print(f"Reçu du client {self.adress}: {data.decode(ENCODING)}")
                    self.client_data = json.loads(data.decode(ENCODING))


                    self.update_client()
                       

                except TimeoutError:
                    if self.uuid in self.server.clients:
                        timeout = self.server.clients[self.uuid].check_timout()
                        if timeout:
                            self.close()
                    continue

            self.close()

    def update_client(self):
        self.uuid = list(self.client_data.keys())[0]
        client = self.server.clients.get(self.uuid)

        if not client:
            print("Création TCP client")
            client = Client()
            self.server.clients[self.uuid] = client
        
        if self.client_data:
            client.update_player(self.client_data[self.uuid], 'TCP')


    
    def send(self, message):
        data = json.dumps(message)
        self.client_socket.send(data.encode(ENCODING))
    
    def close(self):
        self.is_running = False
        self.client_socket.close()
        self.server.remove_client(self)


