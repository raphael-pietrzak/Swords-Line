import socket
import json
import time
import threading

class ClientMessageSender:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client_id = None
        self.room_id = None
        self.socket = None
        self.message_handler = MessageHandler(self)
        self.running = False
        self.receive_thread = None
        self.message_callback = None
    
    def start_receiving(self):
        """Démarre le thread d'écoute des messages"""
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.daemon = True
        self.receive_thread.start()
    
    def stop_receiving(self):
        """Arrête le thread d'écoute des messages"""
        self.running = False
        if self.receive_thread:
            self.receive_thread.join()
    
    def _receive_loop(self):
        """Boucle d'écoute des messages du serveur"""
        self.socket.setblocking(False)
        while self.running:
            try:
                response = self.socket.recv(4096).decode('utf-8')
                if response:
                    response = json.loads(response)
                    self.message_handler.handle_message(self.client_id, None, response)
            except socket.error:
                time.sleep(0.1)  # Évite de surcharger le CPU
            except json.JSONDecodeError:
                print("Erreur de décodage JSON")
            except Exception as e:
                print(f"Erreur de réception: {e}")
    
    def connect(self):
        """Établit la connexion au serveur"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.start_receiving()  # Démarre le thread d'écoute
            self.send_message("JOIN", {"name": "TestPlayer"})
            print(f"Connecté au serveur {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion au serveur"""
        self.stop_receiving()  # Arrête le thread d'écoute
        if self.socket:
            self.socket.close()
            print("Déconnecté du serveur")
    
    def set_client_id(self, client_id):
        """Définit l'ID client pour les messages"""
        self.client_id = client_id
        print(f"ID client défini: {client_id}")
    
    def set_room_id(self, room_id):
        """Définit l'ID de la room pour les messages"""
        self.room_id = room_id
        print(f"ID room défini: {room_id}")
    
    def send_message(self, message_type, data):
        """Envoie un message formaté au serveur sans attendre de réponse"""
        if not self.socket:
            print("Erreur: Non connecté au serveur")
            return False
        
        try:
            message = {
                "client_id": self.client_id,
                "type": message_type,
                "data": data,
                "timestamp": time.time()
            }
            
            message_json = json.dumps(message)
            self.socket.sendall(message_json.encode('utf-8') + b'\n')
            return True
        except Exception as e:
            print(f"Erreur d'envoi: {e}")
            return False
        
class MessageHandler:
    def __init__(self, server):
        self.server = server
    
    def handle_message(self, client_id, player, message):
        """Traite un message reçu du serveur"""
        message_type = message["type"]
        data = message["data"]

        print(f"Message reçu: {message}")
        
        # Appeler le callback s'il existe
        if self.server.message_callback:
            self.server.message_callback(message)
        
        if message_type == "CONNECTED":
            print(f"Connecté en tant que {data['name']}")
        elif message_type == "ROOM_CREATED":
            print(f"Room créée: {data['room_name']}")
        elif message_type == "JOINED_ROOM":
            print(f"Rejoins la room {data['room_id']}")
            self.server.set_room_id(data['room_id'])
        elif message_type == "ERROR":
            print(f"Erreur: {data['message']}")
        elif message_type == "PLAYER_JOINED":
            print(f"Joueur rejoint: {data['name']}")
        elif message_type == "PLAYER_LEFT":
            print(f"Joueur parti: {data['player_id']}")
        elif message_type == "CHAT_MESSAGE":
            print(f"{data['author']}: {data['message']}")
        else:
            print(f"Message inconnu: {message}")

def move_player_in_loop(client):
    client.send_message("MOVE", {"direction": "UP"})
    time.sleep(1)
    client.send_message("MOVE", {"direction": "DOWN"})
    time.sleep(1)
    client.send_message("MOVE", {"direction": "LEFT"})
    time.sleep(1)
    client.send_message("MOVE", {"direction": "RIGHT"})
    time.sleep(1)
    for i in range(100):
        client.send_message("MOVE", {"direction": "DOWN"})
        time.sleep(0.1)

# Exemples d'utilisation
if __name__ == "__main__":
    client = ClientMessageSender()
    
    if client.connect():

        # Simulation d'une session
        client.set_client_id("player123")
        print("JOIN")
        client.send_message("JOIN", {"name": "Raphael"})
        input()
        print("CREATE_ROOM")
        client.send_message("CREATE_ROOM", {"room_name": "Ma Room", "max_players": 4})
        input()
        print("JOIN_ROOM")
        print(client.room_id)
        client.send_message("JOIN_ROOM", {"room_id": client.room_id})
        
        move_player_in_loop(client)
