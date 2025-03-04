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

    