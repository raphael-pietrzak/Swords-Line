import json, socket, threading
import time
from classes.settings import *

# DATA must be formated as JSON



class Client:
    def __init__(self, address, client_id):
        self.address = address
        self.id = client_id
        self.last_signal_time = time.time()
        self.message = {}

    def update_signal(self):
        self.last_signal_time = time.time()

    

class Server:
    def __init__(self):
        self.clients_data = {}
        self.clients = {}


        self.lock = threading.Lock()
        self.start()


    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((HOST, PORT))
        print(f"\nServeur en ligne sur le port {PORT}\n")

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    

    def receive(self):
        while self.running:
            data, address = self.server_socket.recvfrom(1024)
            message = data.decode()
            message = json.loads(message)
            
            
            client_id = message['id']
            with self.lock:
                if client_id not in self.clients:
                    self.clients[client_id] = Client(address, client_id)
                self.clients[client_id].update_signal()
                self.clients[client_id].message = message
    

    # def get_active_clients_data(self):
    #     with self.lock:
    #         active_clients = { address: client for address, client in self.clients.items() if time.time() - client.last_signal_time <= 5}
    #         return active_clients
    
    # def get_clients_data(self):
    #     with self.lock:
    #         return self.clients
    
    def get_clients(self):
        with self.lock:
            return self.clients



    def send(self, message, address):
        message = json.dumps(message)
        self.server_socket.sendto(message.encode(), address)
        


    def stop(self):
        self.running = False
        self.server_socket.close()
        print("Serveur fermé")


        
            
        
