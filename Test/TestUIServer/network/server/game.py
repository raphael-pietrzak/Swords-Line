
from player import Deck, Board
from enum import Enum

class GameState(Enum):
    WAITING = 0
    STARTING = 1
    PLAYING = 2
    FINISHED = 3


class GameLogic:
    def __init__(self, game_room):
        self.game_room = game_room
        self.current_turn = 0
        self.current_player_index = 0
        self.board = None
        self.deck = None
        
    def initialize_game(self):
        # Initialiser le plateau, le deck, distribuer les cartes, etc.
        self.current_turn = 1
        self.current_player_index = 0
        self.board = Board()
        self.deck = Deck()
        
        # Distribuer les cartes initiales aux joueurs
        for player in self.game_room.players:
            player.hand = self.deck.draw_cards(5)  # Par exemple, 5 cartes par joueur
    
    def process_turn(self):
        # Logique pour traiter un tour de jeu
        # Vérifier si le jeu est terminé
        if self.check_game_over_condition():
            return True
            
        # Passer au joueur suivant
        self.current_player_index = (self.current_player_index + 1) % len(self.game_room.players)
        if self.current_player_index == 0:
            self.current_turn += 1
            
        return False
    
    def handle_player_action(self, player_id, action):
        # Vérifier si c'est le tour du joueur
        current_player = self.game_room.players[self.current_player_index]
        if current_player.id != player_id:
            return False
            
        # Traiter l'action en fonction de son type
        action_type = action.get('type')
        if action_type == 'PLAY_CARD':
            return self.handle_play_card(player_id, action.get('card_id'), action.get('target'))
        elif action_type == 'DRAW_CARD':
            return self.handle_draw_card(player_id)
        # Autres types d'actions...
        
        return False
    
    def handle_play_card(self, player_id, card_id, target=None):
        player = self.game_room.get_player_by_id(player_id)
        if not player:
            return False
            
        # Trouver la carte dans la main du joueur
        card = player.find_card_in_hand(card_id)
        if not card:
            return False
            
        # Vérifier si la carte peut être jouée
        if not self.is_valid_card_play(player, card, target):
            return False
            
        # Effet de la carte
        self.apply_card_effect(player, card, target)
        
        # Retirer la carte de la main du joueur
        player.remove_card_from_hand(card_id)
        
        return True
    
    def handle_draw_card(self, player_id):
        player = self.game_room.get_player_by_id(player_id)
        if not player:
            return False
            
        # Piocher une carte
        card = self.deck.draw_card()
        if card:
            player.add_card_to_hand(card)
            return True
        return False
    
    def is_valid_card_play(self, player, card, target):
        # Vérifier si la carte peut être jouée (coût, conditions, etc.)
        return True  # À implémenter selon les règles du jeu
    
    def apply_card_effect(self, player, card, target):
        # Appliquer l'effet de la carte
        # À implémenter selon les règles du jeu
        pass
    
    def check_game_over_condition(self):
        # Vérifier si les conditions de fin de partie sont remplies
        # Par exemple, un joueur n'a plus de points de vie
        for player in self.game_room.players:
            if player.health <= 0:
                return True
        return False