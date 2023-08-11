import socket, threading, json, time, uuid
from classes.settings import *
from classes.player import Player
from random import randint


class Server:
    def __init__(self):
        # main setup
        self.running = False
        self.server_socket = None
        self.accept_clients_thread = None
        self.start_server()

        # clients
        self.clients_data = {}
        self.clients = [] 
        self.players = {}

        # lock
        self.lock = threading.Lock()


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


    # clients
    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"Nouvelle connexion de {addr[0]} : {addr[1]}")

                client_handler_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_handler_thread.start()

            except OSError:
                pass
    
    def handle_client(self, client_socket, addr):
        try:
            player_id = str(uuid.uuid4())
            self.create_player(player_id)

            while self.running:
                data = self.receive_data(client_socket)

                if not data:
                    break  

                with self.lock:
                    self.process_client_data(data, player_id)

                response = self.load_player_data()
                client_socket.send(response.encode())

        finally:
            with self.lock:
                print(f"Connexion fermée avec {addr[0]} : {addr[1]}")
                client_socket.close()
                self.clients_data.pop(player_id)
                self.players.pop(player_id)

    def load_player_data(self):
        data_dict = {}
        for key, value in self.players.items():
            data_dict[key] = {
                "position" : [int(value.pos.x), int(value.pos.y)],
                "status" : value.status,
                "direction" : value.direction,
                "health" : value.health,
                "damage" : value.damage
           }

        return json.dumps(data_dict)

    # data
    def receive_data(self, client_socket):
        try:
            data = client_socket.recv(1024)
            return data
        except ConnectionResetError:
            return b''

    def process_client_data(self, data, player_id):
        data = data.decode()
        try:
            data = json.loads(data)
            self.clients_data[player_id] = data
        except json.JSONDecodeError:
            print("Erreur de format JSON : ", data)
            pass
        
        
    # players
    def create_player(self, player_id):
        x = randint(0, WINDOW_WIDTH)
        y = randint(0, WINDOW_HEIGHT)

        self.players[player_id] = Player((x, y))

    

    def update(self, dt):
        with self.lock:
            for client_id, data in self.clients_data.items():
                self.players[client_id].move(data)
                self.players[client_id].update(dt)
    
