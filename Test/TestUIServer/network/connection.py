import json
from network.controller import MessageHandler
from game.player import Player

class ConnectionHandler:
    def __init__(self, server):
        self.server = server
        self.message_handler = MessageHandler(server)

    def handle_client(self, client_id, conn):
        player_name = None
        room_id = None
        
        try:
            data = conn.recv(4096).decode('utf-8')
            message = json.loads(data)

            if message["type"] == "JOIN":
                player_name = message["data"]["name"]
                player = self.server.player_manager.create_player(client_id, player_name)
                
                # Send connected message
                data = { "client_id": client_id, "name": player_name }
                self.server.send_message(client_id, "CONNECTED", data)
                self.server.add_log(f"Player connected: {player_name} ({client_id})")
                
                while self.server.running:
                    data = conn.recv(4096).decode('utf-8')
                    if not data:
                        break
                    
                    message = json.loads(data)
                    self.message_handler.handle_message(client_id, player, message)
        except Exception as e:
            self.server.add_log(f"Error with client {client_id}: {e}")
        finally:
            self._cleanup_client(client_id, conn, room_id)

    def _cleanup_client(self, client_id, conn, room_id):
        if room_id and room_id in self.server.rooms:
            self.server.remove_player(client_id)
            self.server.broadcast_to_room(room_id, {
                "type": "PLAYER_LEFT",
                "player_id": client_id
            })
        
        if client_id in self.server.clients:
            conn.close()
            del self.server.clients[client_id]
            print(self.server.clients)
            self.server.player_manager.remove_player(client_id)
            print(self.server.player_manager.players)
            self.server.add_log(f"Client disconnected: {client_id}")