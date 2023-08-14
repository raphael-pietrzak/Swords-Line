
import threading, uuid, json
from random import randint
from settings import *
from player import Player


class ClientHandler(threading.Thread):
    def __init__(self, remove_client, extract_server_data, client_socket, client_addr):
        super().__init__()
        self.running = True

        # client
        self.server_data = {}
        self.socket = client_socket
        self.adrr = client_addr

        # player
        self.uuid = str(uuid.uuid4())
        self.player = Player((randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        
        # extract
        self.extract_server_data = extract_server_data
        self.remove_client = remove_client


    def run(self):
        while self.running:
            client_data = self.get_client_data()

            if client_data:
                    
                self.player.update(client_data)

                self.server_data = self.extract_server_data(self.uuid)

            self.send_to_client()

    


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
        
    
    def send_to_client(self):
        try:
            data = json.dumps(self.server_data)
            self.socket.send(data.encode())

        except:
            self.disconnect()
        
    
    def disconnect(self):
        print(f"Connexion fermée avec {self.adrr[0]} : {self.adrr[1]}")
        self.socket.close()
        self.running = False
        self.remove_client(self)


        

