from room import GameRoom
from game import GameState
import time

class RoomManager:
    def __init__(self):
        self.rooms = {}
        self.next_room_id = 1
    
    def create_room(self, room_name=None):
        print(f"Creating room with name: {room_name}")
        room_name = room_name or f"Room {self.next_room_id}"
        room = GameRoom(self.next_room_id, room_name)
        self.rooms[self.next_room_id] = room
        room_id = self.next_room_id
        self.next_room_id += 1
        return room_id, room

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]

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
