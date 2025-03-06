from game.room import Room
import time
from settings import GameState



class RoomManager:
    def __init__(self, log_manager):
        self.log_manager = log_manager
        self.rooms = {}
        self.next_room_id = 1

    def add_room(self, room):
        self.rooms[room.id] = room
        return room.id, room
    
    def create_room(self, room_name=None, max_players=8):
        room_name = room_name or f"Room {self.next_room_id}"
        room = Room(room_name, max_players)
        self.rooms[room.id] = room
        self.next_room_id += 1
        self.log_manager.add_log(f"Room created: {room_name} ({room.id})")
        return room

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def remove_room(self, room_id):
        if room_id in self.rooms:
            room_name = self.rooms[room_id].name
            del self.rooms[room_id]
            self.log_manager.add_log(f"Room removed: {room_name} ({room_id})")

    def cleanup_rooms(self, cleanup_delay):
        current_time = time.time()
        for room_id in list(self.rooms.keys()):
            room = self.rooms[room_id]
            if (len(room.players) == 0 or 
                (room.game_state == GameState.FINISHED and 
                 room.finished_at + cleanup_delay < current_time)):
                self.remove_room(room_id)

    def update_rooms(self):
        for room in self.rooms.values():
            if room.game_state == GameState.PLAYING:
                room.process_turn()

    def generate_demo_data(self):
        self.log_manager.add_log("Generating demo data...")
        for i in range(3):
            self.create_room(f"Room {i + 1}")
        for room in self.rooms.values():
            for i in range(4):
                room.add_player(f"Player {i + 1}")