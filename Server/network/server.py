import json, socket, threading
from classes.settings import *


class Server:
    def __init__(self):
        self.clients_data = {}
        self.clients = []

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
            
            with self.lock:
                self.clients_data[address] = message
    
    def get_clients_data(self):
        with self.lock:
            return self.clients_data



    def send(self, message, address):
        message = json.dumps(message)
        self.server_socket.sendto(message.encode(), address)
        


    def stop(self):
        self.running = False
        self.server_socket.close()
        print("Serveur fermé")


        
            
        
