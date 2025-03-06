
from game.player import Player


class PlayerManager:
    def __init__(self, log_manager):
        self.log_manager = log_manager
        self.players = {}
    
    def create_player(self, client_id, player_name):
        player = Player(client_id, player_name)
        self.players[client_id] = player
        self.log_manager.add_log(f"Player created: {player_name} ({client_id})")
        return player
    
    def get_player(self, player_id):
        return self.players.get(player_id)
    
    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            self.log_manager.add_log(f"Player removed: {player_id}")
    
    def get_all_players(self):
        return self.players.values()
    
        