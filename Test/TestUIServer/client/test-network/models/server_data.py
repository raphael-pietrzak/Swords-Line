import time
import random
from game.room import Room
from game.player import Player
from rooms.room_manager import RoomManager

class ServerData:
    def __init__(self):
        self.rooms = {}  # {room_id: Room}
        self.players = {}  # {player_id: Player}
        self.logs = [] # Liste des logs
        self.max_logs = 100
    
    # Rooms
    def add_room(self, room):
        self.rooms[room.id] = room
        return room.id, room
    
    def delete_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
        self.add_log(f"Room deleted: {room_id}")
    
    def create_room(self, max_players=8):
        room_id = f"room_{len(self.rooms)}"
        room = Room(room_id, f"Room {len(self.rooms) + 1}", max_players)
        self.add_room(room)
        self.add_log(f"Room created: {room_id}")
        return room
    
    def get_room(self, room_id):
        return self.rooms.get(room_id)
    
    def get_all_rooms(self):
        return list(self.rooms.values())
    

    # Players
    def add_player(self, player):
        if player.id not in self.players:
            self.players[player.id] = player

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
    
    def get_player(self, player_id):
        return self.players.get(player_id)
    
    def get_all_players(self):
        return list(self.players.values())
    
    def add_log(self, message, log_type="INFO"):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.logs.append({"time": timestamp, "type": log_type, "message": message})
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
    
    def clear_logs(self):
        self.logs = []
    
    def generate_demo_data(self):

        character_types = ["warrior", "mage", "archer", "healer"]

        for i in range(5):
            room = Room(f"Room {i}", f"room_{i}")
            self.add_room(room)
        
        for i in range(10):
            player = Player(f"player_{i}", f"Player {i}", random.choice(character_types))
            self.add_player(player)
    
