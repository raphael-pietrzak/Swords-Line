import socket
import threading
import json
import time
from settings import ServerConfig
from network.connection import ConnectionHandler
from network.controller import MessageHandler
from management.log_manager import LogManager
from management.player_manager import PlayerManager
from management.room_manager import RoomManager



class GameServer:
    def __init__(self, config=ServerConfig):

        # Initialisation des composants
        self.log_manager = LogManager()
        self.player_manager = PlayerManager(self.log_manager)
        self.room_manager = RoomManager(self.log_manager)

        # Configuration
        self.config = config
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.next_client_id = 1

        # Messages
        self.message_handler = MessageHandler(self)

        # Gestion des connexions
        self.connection_handler = ConnectionHandler(self)


    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.config.HOST, self.config.PORT))
            self.server_socket.listen(self.config.MAX_CONNECTIONS)
            self.running = True
            self.log_manager.add_log(f"Serveur démarré sur le port {self.config.PORT}")
            
            self._start_threads()
            return True
        except Exception as e:
            self.log_manager.add_log(f"Erreur lors du démarrage du serveur: {e}")
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
                self.log_manager.add_log(f"Nouveau client connecté: {addr}, ID: {client_id}")
                
                client_thread = threading.Thread(
                    target=self.connection_handler.handle_client,
                    args=(client_id, conn)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    self.log_manager.add_log(f"Erreur lors de l'acceptation d'une connexion: {e}")

    def send_message(self, client_id, message_type, data):
         # Création du message formaté
        message = {
            "client_id": client_id,
            "type": message_type,
            "data": data,
            "timestamp": time.time()
        }

        try:
            # Conversion en JSON et envoi
            message_json = json.dumps(message)
            conn, _ = self.clients[client_id]
            conn.sendall(message_json.encode('utf-8') + b'\n')  # Ajout délimiteur
            self.log_manager.add_log(f"Message envoyé à {client_id}: {message}")
        except Exception as e:
            self.log_manager.add_log(f"Erreur d'envoi à {client_id}: {e}")

    def broadcast_to_room(self, room_id, message_type, data, exclude=None):
        message = {
            "type": message_type,
            "data": data
        }
        self.log_manager.add_log(f"Broadcast à la room {room_id}: {message}")

        if room_id in self.room_manager.rooms:
            room = self.room_manager.rooms[room_id]
            for player in room.players:
                if exclude is None or player.id != exclude:
                    self.send_to_client(player.id, message)

    def add_log(self, message):
        self.log_manager.add_log(message)

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        for client_id, (conn, _) in self.clients.items():
            conn.close()
        
        self.clients.clear()
        # self.room_manager.rooms.clear()
        self.log_manager.add_log("Serveur arrêté")
