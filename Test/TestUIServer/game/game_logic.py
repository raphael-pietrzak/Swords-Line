import random

class GameLogic:
    def __init__(self, room):
        self.room = room
        self.player_positions = {}
        self.game_board = []
        self.board_size = 1000
        
    def initialize_game(self):
        """Initialise le jeu et les positions des joueurs"""
        self.game_board = []
        self.player_positions = {}
        
        # Positionne chaque joueur aléatoirement sur le plateau
        for player in self.room.players:
            x = random.randint(0, self.board_size)
            y = random.randint(0, self.board_size)
            self.player_positions[player.id] = {'x': x, 'y': y}
            player.position = {'x': x, 'y': y}
    
    def process_turn(self):
        """Traite un tour de jeu"""
        # Vérifie les collisions entre joueurs
        self.check_collisions()
        
        # Vérifie les conditions de fin de partie
        if self.check_game_over():
            return True
        return False
    
    def update_player_position(self, player_id, new_position):
        """Met à jour la position d'un joueur"""
        if player_id in self.player_positions:
            self.player_positions[player_id] = new_position
            return True
        return False
    
    def check_collisions(self):
        """Vérifie les collisions entre les joueurs"""
        players = list(self.player_positions.keys())
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                pos1 = self.player_positions[players[i]]
                pos2 = self.player_positions[players[j]]
                if self.is_collision(pos1, pos2):
                    self.handle_collision(players[i], players[j])
    
    def is_collision(self, pos1, pos2, threshold=10):
        """Détermine si deux positions sont en collision"""
        dx = pos1['x'] - pos2['x']
        dy = pos1['y'] - pos2['y']
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < threshold
    
    def handle_collision(self, player1_id, player2_id):
        """Gère la collision entre deux joueurs"""
        # À implémenter selon les règles du jeu
        pass
    
    def check_game_over(self):
        """Vérifie si le jeu est terminé"""
        # À implémenter selon les conditions de fin de partie
        return False
