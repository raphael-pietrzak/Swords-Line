import json, socket, threading, time
from classes.settings import *


class TCPServer(threading.Thread):
    def __init__(self, del_udp_client):
        super().__init__()
        self.del_udp_client = del_udp_client
        self.clients = []
        self.new_clients = []
        self.del_clients = []

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
                client_socket.settimeout(1.0)
                print("Nouvelle connexion établie :", adress)

                init_data = client_socket.recv(BUFFER_SIZE)
                init_data = json.loads(init_data.decode(ENCODING))
                print(init_data)
                uuid = init_data['uuid']

                client_handler = ClientHandler(client_socket, adress, self, uuid)
                client_handler.start()
                self.clients.append(client_handler)
                self.new_clients.append(uuid)

        except ConnectionAbortedError:
            self.close()
    
    def get_clients_data(self):
        clients_data = {}
        for client in self.clients:
            clients_data[client.uuid] = client.client_data
        return clients_data
    
    def send(self, message, uuid=None):
        if len(message) >= BUFFER_SIZE:
            print("Message trop long")
            return
        
        for client in self.clients:
            if client.uuid == uuid or uuid is None:
                client.waiting_data.append(message)



    def close(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()



class ClientHandler(threading.Thread):
    def __init__(self, client_socket, adress, server, uuid):
        super().__init__()
        self.client_socket = client_socket
        self.client_socket.settimeout(1.0)
        self.server = server
        self.adress = adress
        self.is_running = True

        self.uuid = uuid
        self.client_data = {}
        self.waiting_data = []

    def run(self):
        while self.is_running:

            if self.waiting_data:
                message = self.waiting_data.pop(0)
                self.send(message)

            try:
                data = self.client_socket.recv(BUFFER_SIZE)
                if not data: break 
                # DEBUG
                print(f"Reçu du client {self.adress}: {data.decode(ENCODING)}")
                self.client_data = json.loads(data.decode(ENCODING))


            except TimeoutError:
                continue
        
        print('Thread TCP server receive terminated')
        self.close()
        
    
    def send(self, message):
        data = json.dumps(message)
        self.client_socket.send(data.encode(ENCODING))
    
    def close(self):
        self.is_running = False
        self.server.clients.remove(self)
        self.server.del_clients.append(self.uuid)
        self.server.del_udp_client(self.uuid)
        self.client_socket.close()
        print(f"Client {self.adress} déconnecté")

