import time
from game.room import Room

class MessageHandler:
    def __init__(self, network, server_data):
        self.log_manager = server_data.log_manager
        self.room_manager = server_data.room_manager
        self.player_manager = server_data.player_manager
        self.network_handler = network

    def handle_message(self, client_id, player, message):
        self.log_manager.add_log(f"Message received from {client_id}: {message}")
        handlers = {
            "CREATE_ROOM": self._handle_create_room,
            "JOIN_ROOM": self._handle_join_room,
            "START_GAME": self._handle_start_game,
            "GAME_ACTION": self._handle_game_action,
            "CHAT_MESSAGE": self._handle_chat_message
        }
        
        handler = handlers.get(message.get("type"))
        data = message.get("data")
        if handler:
            handler(client_id, player, data)

    def _handle_create_room(self, client_id, player, message):
        room_name = message.get("room_name")
        room = Room(room_name, self.server_data)
        room_id = room.id
        room.add_player(player)
        self.network_handler.send_message(client_id, "ROOM_CREATED", {
            "room_id": room_id,
            "room_name": room.name
        })
        self.log_manager.add_log(f"Room created by {player.name}: {room_id}")

    def _handle_join_room(self, client_id, player, message):
        room_id = message.get("room_id")
        if room_id in self.room_manager.rooms:
            room = self.room_manager.rooms[room_id]
            if room.add_player(player):
                self.network_handler.send_message(client_id, "JOINED_ROOM", {
                    "room_id": room_id,
                    "room_info": room.get_status()
                })
                self.network_handler.broadcast_to_room(room_id, "PLAYER_JOINED", {
                    "player": player.get_info()
                }, exclude=client_id)
                self.log_manager.add_log(f"Player {player.name} joined room {room_id}")
            else:
                self.network_handler.send_message(client_id, "ERROR", {
                    "message": "Impossible de rejoindre la room"
                })
                self.log_manager.add_log(f"Player {player.name} tried to join full room {room_id}")
        else:
            self.network_handler.send_message(client_id, "ERROR", {
                "message": "Room inexistante"
            })
            self.log_manager.add_log(f"Player {player.name} tried to join non-existent room {room_id}")

    def _handle_start_game(self, client_id, player, message):
        room_id = message.get("room_id")
        if room_id in self.room_manager.rooms:
            room = self.room_manager.rooms[room_id]
            if room.get_player_by_id(client_id):
                player.is_ready = True
                all_ready = all(p.is_ready for p in room.players)
                if all_ready and len(room.players) >= 2:
                    room.start_game()
                    self.network_handler.broadcast_to_room(room_id, "GAME_STARTED", {
                        "game_info": {
                            "players": [p.get_info() for p in room.players],
                            "current_turn": 1,
                            "current_player": room.players[0].id
                        }
                    })
                    self.network_handler.add_log(f"Game started in room {room_id}")

    def _handle_game_action(self, client_id, player, message):
        room_id = message.get("room_id")
        action = message.get("action")
        
        if room_id in self.room_manager.rooms:
            room = self.room_manager.rooms[room_id]
            if room.handle_player_action(client_id, action):
                self.network_handler.broadcast_to_room(room_id, "GAME_UPDATE", {
                    "player_id": client_id,
                    "action": action,
                    "game_state": room.game_logic.get_game_state()
                })
                self.log_manager.add_log(f"Game action from {player.name} in room {room_id}: {action}")

    def _handle_chat_message(self, client_id, player, message):
        room_id = message.get("room_id")
        text = message.get("text")
        
        if room_id in self.room_manager.rooms:
            room = self.room_manager.rooms[room_id]
            if room.get_player_by_id(client_id):
                room.add_chat_message(client_id, text)
                self.network_handler.broadcast_to_room(room_id, "CHAT_MESSAGE", {
                    "player_id": client_id,
                    "player_name": player.name,
                    "text": text,
                    "timestamp": time.time()
                })
                self.log_manager.add_log(f"Chat message from {player.name} in room {room_id}: {text}")