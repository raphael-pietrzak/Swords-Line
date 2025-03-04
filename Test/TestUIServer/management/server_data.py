
from management.room_manager import RoomManager
from management.player_manager import PlayerManager
from management.log_manager import LogManager

class ServerData:
    def __init__(self):
        self.room_manager = RoomManager()
        self.player_manager = PlayerManager()
        self.log_manager = LogManager()