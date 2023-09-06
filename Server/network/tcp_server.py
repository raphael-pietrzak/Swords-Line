
import socket
import threading
from classes.settings import *
from network.handler import ClientHandler



class ServerTCP:
    def __init__(self):
        # main setup
        self.server_socket = None
        self.server_data = {}
        self.start_server()

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