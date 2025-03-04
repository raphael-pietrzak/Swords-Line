
from game.player import Player


class PlayerManager:
    def __init__(self):
        self.players = {}
        self.next_player_id = 1
    
    def create_player(self, player_name):
        player = Player(self.next_player_id, player_name)
        self.players[self.next_player_id] = player
        player_id = self.next_player_id
        self.next_player_id += 1
        return player_id, player
    
    def get_player(self, player_id):
        return self.players.get(player_id)
    
    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
    
    def get_all_players(self):
        return self.players.values()