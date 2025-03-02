import socket
import threading
import json
import time
from config import ServerConfig
from room_manager import RoomManager
from player import Player
from network.connection import ConnectionHandler





class NetworkServer:
    def __init__(self, config=ServerConfig):
        self.config = config
        self.server_socket = None
        self.clients = {}
        self.room_manager = RoomManager()
        self.running = False
        self.next_client_id = 1
        self.connection_handler = ConnectionHandler(self)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.config.HOST, self.config.PORT))
            self.server_socket.listen(self.config.MAX_CONNECTIONS)
            self.running = True
            print(f"Serveur démarré sur le port {self.config.PORT}")
            
            self._start_threads()
            return True
        except Exception as e:
            print(f"Erreur lors du démarrage du serveur: {e}")
            return False

    def _start_threads(self):
        threading.Thread(target=self.accept_connections, daemon=True).start()
        threading.Thread(target=self.update_loop, daemon=True).start()

    def update_loop(self):
        while self.running:
            self.room_manager.update_rooms()
            self.room_manager.cleanup_rooms(self.config.ROOM_CLEANUP_DELAY)
            time.sleep(self.config.UPDATE_INTERVAL)

    def accept_connections(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                client_id = self.next_client_id
                self.next_client_id += 1
                
                self.clients[client_id] = (conn, addr)
                print(f"Nouveau client connecté: {addr}, ID: {client_id}")
                
                client_thread = threading.Thread(
                    target=self.connection_handler.handle_client,
                    args=(client_id, conn)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"Erreur lors de l'acceptation d'une connexion: {e}")

    def send_to_client(self, client_id, message):
        if client_id in self.clients:
            conn, _ = self.clients[client_id]
            try:
                data = json.dumps(message).encode('utf-8')
                conn.sendall(data)
            except Exception as e:
                print(f"Erreur lors de l'envoi au client {client_id}: {e}")

    def broadcast_to_room(self, room_id, message, exclude=None):
        if room_id in self.room_manager.rooms:
            room = self.room_manager.rooms[room_id]
            for player in room.players:
                if exclude is None or player.id != exclude:
                    self.send_to_client(player.id, message)

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        for client_id, (conn, _) in self.clients.items():
            conn.close()
        
        self.clients.clear()
        self.room_manager.rooms.clear()
        print("Serveur arrêté")
