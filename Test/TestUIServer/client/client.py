import socket
import json
import time

class ClientMessageSender:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client_id = None
        self.room_id = None
        self.socket = None
        self.message_handler = MessageHandler(self)
    
    def connect(self):
        """Établit la connexion au serveur"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.send_message("JOIN", {"name": "TestPlayer"})
            print(f"Connecté au serveur {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion au serveur"""
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
        """Envoie un message formaté au serveur"""
        if not self.socket:
            print("Erreur: Non connecté au serveur")
            return False
        
        try:
            message = {
                "client_id": self.client_id,
                "room_id": self.room_id,
                "type": message_type,
                "data": data,
                "timestamp": time.time()
            }
            
            message_json = json.dumps(message)
            self.socket.sendall(message_json.encode('utf-8') + b'\n')
            
            # Gestion asynchrone de la réponse pour éviter le blocage de l'interface
            self.socket.setblocking(False)
            try:
                response = self.socket.recv(4096).decode('utf-8')
                if response:
                    print(f"Réponse reçue: {response}")
                    response = json.loads(response)
                    self.message_handler.handle_message(self.client_id, None, response)
            except:
                pass
            finally:
                self.socket.setblocking(True)
            
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
