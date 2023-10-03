import json
import socket
import threading
import time
from Network.Server.client import Client
from ping import FPSCounter
from settings import *



class UDPServer(threading.Thread):
    def __init__(self, clients):
        super().__init__()
        self.clients = clients
        self.is_running = True

        self.client_data = {}
        self.server_data = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((HOST, UDP_PORT))
        print(f"Serveur UDP en écoute sur {HOST}:{UDP_PORT} ...")

        self.network_fps_counter = FPSCounter('SERVER UDP')



    def run(self):
        while self.is_running:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                self.client_data = json.loads(data.decode(ENCODING)) 
                if not self.client_data: continue

                self.update_client()
                self.server_socket.sendto(json.dumps(self.server_data).encode(ENCODING), addr)


                self.network_fps_counter.ping()

            except Exception as e:
                print(f'Error UDP server send/receive : {e}')
                print(data.decode(ENCODING))
                continue
            

    def update_client(self):
        uuid = list(self.client_data.keys())[0]
        client = self.clients.get(uuid)
        if not client:
            return

        if self.client_data:
            client.update_player(self.client_data[uuid], 'UDP')
    

    def close(self):
        self.is_running = False
        self.server_socket.close()


