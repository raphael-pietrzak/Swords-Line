import random

class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.hand = []  # Cartes en main
        self.health = 100  # Points de vie
        self.energy = 10   # Énergie/mana
        self.is_ready = False
        self.position = None  # Position sur le plateau
        
    def add_card_to_hand(self, card):
        self.hand.append(card)
    
    def remove_card_from_hand(self, card_id):
        for i, card in enumerate(self.hand):
            if card.id == card_id:
                return self.hand.pop(i)
        return None
    
    def find_card_in_hand(self, card_id):
        for card in self.hand:
            if card.id == card_id:
                return card
        return None
    
    def get_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'health': self.health,
            'energy': self.energy,
            'card_count': len(self.hand),
            'is_ready': self.is_ready
        }


class Card:
    def __init__(self, card_id, name, card_type, cost, effects):
        self.id = card_id
        self.name = name
        self.type = card_type  # ATTACK, DEFENSE, SPELL, etc.
        self.cost = cost  # Coût en énergie
        self.effects = effects  # Liste des effets de la carte
    
    def apply_effects(self, source_player, target=None, game_logic=None):
        # Appliquer les effets de la carte
        for effect in self.effects:
            effect.apply(source_player, target, game_logic)


class CardEffect:
    def __init__(self, effect_type, value):
        self.type = effect_type  # DAMAGE, HEAL, DRAW, etc.
        self.value = value  # Valeur de l'effet
    
    def apply(self, source_player, target=None, game_logic=None):
        if self.type == 'DAMAGE' and target:
            target.health -= self.value
        elif self.type == 'HEAL' and target:
            target.health += self.value
        elif self.type == 'DRAW' and source_player:
            for _ in range(self.value):
                card = game_logic.deck.draw_card()
                if card:
                    source_player.add_card_to_hand(card)


class Board:
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.entities = []  # Liste des entités sur le plateau
    
    def place_entity(self, entity, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = entity
            entity.position = (x, y)
            self.entities.append(entity)
            return True
        return False
    
    def move_entity(self, entity, new_x, new_y):
        if entity in self.entities and 0 <= new_x < self.width and 0 <= new_y < self.height:
            old_x, old_y = entity.position
            self.grid[old_y][old_x] = None
            self.grid[new_y][new_x] = entity
            entity.position = (new_x, new_y)
            return True
        return False
    
    def remove_entity(self, entity):
        if entity in self.entities:
            x, y = entity.position
            self.grid[y][x] = None
            self.entities.remove(entity)
            return True
        return False
    
    def get_entity_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None


class Deck:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)
        return None
    
    def draw_cards(self, count):
        drawn_cards = []
        for _ in range(min(count, len(self.cards))):
            drawn_cards.append(self.draw_card())
        return drawn_cards

