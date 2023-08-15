
import socket, threading
from settings import *
from random import randint
from handler import ClientHandler

class Server:
    def __init__(self):
        # main setup
        self.running = False
        self.server_socket = None

        # clients
        self.clients = [] 
        self.server_data = {}
        self.server_data["players"] = {}


        # trees
        self.trees = []
        self.gold = []
        for _ in range(100):
            self.trees.append([randint(-900, 900), randint(-900, 900)])
            self.gold.append([randint(-900, 900), randint(-900, 900)])
        
        self.start_server()



    # start - stop
    def start_server(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()
        print(f"\nServeur en ligne sur le port {PORT}\n")

        self.accept_clients_thread = threading.Thread(target=self.accept_clients)
        self.accept_clients_thread.start()

    
    def stop_server(self):
        if self.server_socket:
            self.running = False
            self.server_socket.close()

        print("Serveur fermé")


    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"Nouvelle connexion de {addr[0]} : {addr[1]}")

                client_handler_thread = ClientHandler(self, client_socket, addr)
                client_handler_thread.start()

                self.clients.append(client_handler_thread)

            except OSError:
                pass
    


    def extract_server_data(self, player, uuid):
        self.server_data['type'] = "player"
        self.server_data["players"][uuid] = {
            "position" : [int(player.pos.x), int(player.pos.y)],
            "status" : player.status,
            "direction" : player.direction,
            "health" : player.health,
            "damage" : player.damage
        }

        return self.server_data
    

    def init_client_data(self, uuid):
        data = {}
        data['type'] = "init"
        data["trees"] = self.trees
        data["gold"] = self.gold
        data["uuid"] = uuid
        return data

    
    def remove_client(self, client):
        self.clients.remove(client)
        self.server_data["players"].pop(client.uuid)
    
        

    



