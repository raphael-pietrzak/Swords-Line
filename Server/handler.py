
import threading, uuid, json, time
from random import randint
from settings import *
from player import Player


class ClientHandler(threading.Thread):
    def __init__(self, server, client_socket, client_addr):
        super().__init__()
        self.running = True
        self.server = server

        # client
        self.server_data = {}
        self.socket = client_socket
        self.adrr = client_addr

        # player
        self.uuid = str(uuid.uuid4())
        self.player = Player((randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        
        # send init
        data = self.server.init_client_data(self.uuid)
        self.send_to_client(data)
        


    def run(self):
        while self.running:
            client_data = self.get_client_data()

            if client_data:
                self.player.update(client_data)

            self.server_data = self.server.extract_server_data(self.player, self.uuid)

            self.send_to_client(self.server_data)

    


    def get_client_data(self):
        try:
            raw_data = self.socket.recv(BUFFER_SIZE)
            if not raw_data:
                return None  # No data received

            data = json.loads(raw_data.decode())
            return data
        
        except json.JSONDecodeError as json_error:
            print(f"Erreur de décodage JSON lors de la réception des données du client {self.adrr}: {json_error}")
            return None
        
        except ConnectionResetError:
            return None
        
    
    def send_to_client(self, data):
        try:
            data = json.dumps(data)
            self.socket.send(data.encode())

        except:
            self.disconnect()
        
    
    def disconnect(self):
        print(f"Connexion fermée avec {self.adrr[0]} : {self.adrr[1]}")
        self.socket.close()
        self.running = False
        self.server.remove_client(self)


        

