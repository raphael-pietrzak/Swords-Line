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
        self.players = []
        self.rooms = []
    
    def generate_demo_data(self):
        character_types = ["warrior", "mage", "archer", "healer"]
        
        for i in range(3):
            room = Room(f"room_{i}", f"Room {i+1}")
            self.rooms.append(room)
        
        for i in range(15):
            player = Player(f"player_{i}", f"Player{i}", random.choice(character_types))
            self.players.append(player)
            
            if i < 10:
                room_idx = random.randint(0, len(self.rooms) - 1)
                room = self.rooms[room_idx]
                player.room_id = room.id
                room.players.append(player)
