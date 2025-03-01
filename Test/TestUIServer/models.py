import time
import random

class Room:
    def __init__(self, room_id, name, max_players=8):
        self.id = room_id
        self.name = name
        self.max_players = max_players
        self.players = []  # Liste des joueurs dans cette room
        self.created_at = time.time()
    
    @property
    def player_count(self):
        return len(self.players)

class Player:
    def __init__(self, player_id, name, character_type=None):
        self.id = player_id
        self.name = name
        self.character_type = character_type
        self.position = (random.randint(50, 350), random.randint(50, 250))
        self.room_id = None
        self.connected_at = time.time()
        self.level = random.randint(1, 10)
    
    def move_to(self, x, y):
        self.position = (x, y)


class ServerData:
    def __init__(self):
        self.rooms = {}  # {room_id: Room}
        self.players = {}  # {player_id: Player}
    
    def add_room(self, room):
        self.rooms[room.id] = room
    
    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
    
    def create_room(self, max_players=8):
        room_id = f"room_{len(self.rooms)}"
        room = Room(room_id, f"Room {len(self.rooms) + 1}", max_players)
        self.add_room(room)
        return room
    
    def get_room(self, room_id):
        return self.rooms.get(room_id)
    
    def add_player(self, player):
        self.players[player.id] = player
    
    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
    
    def get_player(self, player_id):
        return self.players.get(player_id)
    
    def get_all_rooms(self):
        return list(self.rooms.values())

    def get_all_players(self):
        return list(self.players.values())
    
    def generate_demo_data(self):

        character_types = ["warrior", "mage", "archer", "healer"]

        for i in range(5):
            room = Room(f"Room {i}", f"room_{i}")
            self.add_room(room)
        
        for i in range(10):
            player = Player(f"player_{i}", f"Player {i}", random.choice(character_types))
            self.add_player(player)
    