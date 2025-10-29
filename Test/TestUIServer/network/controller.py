import time
from game.room import Room

class MessageHandler:
    def __init__(self, server):
        self.server = server

    def handle_message(self, client_id, player, message):
        self.server.add_log(f"Message received from {client_id}: {message}")

        handlers = {
            "CREATE_ROOM": self._handle_create_room,
            "JOIN_ROOM": self._handle_join_room,
            "START_GAME": self._handle_start_game,
            "GAME_ACTION": self._handle_game_action,
            "CHAT_MESSAGE": self._handle_chat_message,
            "PLAY1V1": self._handle_play1v1
        }
        
        handler = handlers.get(message.get("type"))
        data = message.get("data")
        if handler:
            handler(client_id, player, data)

    def _handle_create_room(self, client_id, player, message):
        room_name = message.get("room_name")
        room = self.server.room_manager.create_room(room_name)
        self.server.send_message(client_id, "ROOM_CREATED", {
            "room_id": room.id,
            "room_name": room.name
        })
        self.server.add_log(f"Room created by {player.name}: {room.name} ({room.id})")

    def _handle_join_room(self, client_id, player, message):
        if player.room:
            self.server.send_message(client_id, "ERROR", {
                "message": "Vous êtes déjà dans une room"
            })
            return
        room_id = message.get("room_id")
        room = self.server.room_manager.get_room(room_id)
        if room and room.add_player(player):
            self.server.send_message(client_id, "JOINED_ROOM", {
                "room_id": room_id,
                "room_info": room.get_status()
            })
            self.server.broadcast_to_room(room_id, "PLAYER_JOINED", {
                "player": player.get_info()
            }, exclude=client_id)
            self.server.add_log(f"Player {player.name} joined room {room_id}")
        else:
            self.server.send_message(client_id, "ERROR", {
                "message": "Impossible de rejoindre la room"
            })
            self.server.add_log(f"Player {player.name} failed to join room {room_id}")

    def _handle_start_game(self, client_id, player, message):
        room = player.room
        room_id = room.id
        if room:
            self.server.broadcast_to_room(room_id, "GAME_STARTED", {
                "game_info": {
                    "players": [p.get_info() for p in room.players],
                    "current_turn": 1,
                    "current_player": room.players[0].id
                }
            })
            self.server.add_log(f"Game started in room {room_id}")

    def _handle_game_action(self, client_id, player, message):
        self.server.add_log(message)
        action = message.get("action")
        room = player.room
        if room:
            if room.handle_player_action(player, message):
                self.server.broadcast_to_room(room.id, "GAME_UPDATE", {
                    "player_id": client_id,
                    "action": action,
                    "game_state": room.game_logic.get_game_state()
                })
                self.server.add_log(f"Game action from {player.name} in room {room.id}: {action}")

    def _handle_chat_message(self, client_id, player, message):
        room_id = message.get("room_id")
        text = message.get("text")
        room = self.server.room_manager.get_room(room_id)
        if room:
            if room.get_player_by_id(client_id):
                room.add_chat_message(client_id, text)
                self.server.broadcast_to_room(room_id, "CHAT_MESSAGE", {
                    "player_id": client_id,
                    "player_name": player.name,
                    "text": text,
                    "timestamp": time.time()
                })
                self.server.add_log(f"Chat message from {player.name} in room {room_id}: {text}")


    def _handle_play1v1(self, client_id, player, message):
        if player.room:
            self.server.send_message(client_id, "ERROR", {
                "message": "Vous êtes déjà dans une room"
            })
            return
        room = self.server.room_manager.find_random()
        room.add_player(player)
        self.server.send_message(client_id, "JOINED_ROOM", {
            "room_id": room.id,
            "room_info": room.get_status()
        })
        self.server.broadcast_to_room(room.id, "PLAYER_JOINED", {
            "player": player.get_info()
        }, exclude=client_id)
        self.server.add_log(f"Player {player.name} joined room {room.id}")

