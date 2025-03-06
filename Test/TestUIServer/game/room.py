from settings import GameState
import time
import random
import uuid

class Room:
    def __init__(self, room_name , max_players=8):
        self.id = str(uuid.uuid4())[:5].upper()
        self.name = room_name
        self.max_players = max_players
        self.players = []
        self.game_state = GameState.WAITING  # Enum: WAITING, STARTING, PLAYING, FINISHED
        # self.game_logic = GameLogic(self)
        self.chat_messages = []
        self.created_at = time.time()
        self.started_at = None
        self.finished_at = None

        
    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        return False
    
    def remove_player(self, player_id):
        for i, player in enumerate(self.players):
            if player.id == player_id:
                self.players.pop(i)
                return True
        return False
    
    def start_game(self):
        if len(self.players) >= 2 and self.game_state == GameState.WAITING:
            self.game_state = GameState.STARTING
            self.started_at = time.time()
            # self.game_logic.initialize_game()
            self.game_state = GameState.PLAYING
            return True
        return False
    
    def end_game(self):
        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.FINISHED
            self.finished_at = time.time()
            # Déterminer le gagnant, distribuer les récompenses, etc.
            return True
        return False
    
    def process_turn(self):
        if self.game_state == GameState.PLAYING:
            # game_over = self.game_logic.process_turn()
            game_over = False
            if game_over:
                self.end_game()
    
    def handle_player_action(self, player_id, data):
        # if self.game_state == GameState.PLAYING:
        direction = data.get('direction')
        player = self.get_player_by_id(player_id)
        if player:
            player.move(direction)
            return True
            
        return False
    
    def add_chat_message(self, player_id, message):
        player = self.get_player_by_id(player_id)
        if player:
            self.chat_messages.append({
                'player': player.name,
                'message': message,
                'timestamp': time.time()
            })
    
    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def get_status(self):
        return {
            'id': self.id,
            'name': self.name,
            'players': [p.get_info() for p in self.players],
            'state': self.game_state.name,
            'player_count': len(self.players),
            'max_players': self.max_players,
            'created_at': self.created_at
        }

    @property
    def player_count(self):
        return len(self.players)

    
