import random
import time

class Player:
    def __init__(self, player_id, name, character_type=None):
        self.id = player_id
        self.name = name
        self.character_type = character_type
        self.position = (random.randint(50, 350), random.randint(50, 250))
        self.room = None
        self.connected_at = time.time()
        self.level = random.randint(1, 10)
    
    def move_to(self, x, y):
        self.position = (x, y)

    def move(self, direction):
        x, y = self.position
        if direction == 'UP':
            y -= 10
        elif direction == 'DOWN':
            y += 10
        elif direction == 'LEFT':
            x -= 10
        elif direction == 'RIGHT':
            x += 10
        self.position = (x, y)


    def get_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'character_type': self.character_type,
            'position': self.position,
            'room_id': self.room.id,
            'connected_at': self.connected_at,
            'level': self.level
        }
