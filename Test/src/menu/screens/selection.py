import pygame
import os
from src.menu.screens.base import Screen

class CharacterSelectionScreen:
    def __init__(self, screen, available_characters):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.characters = available_characters  # Liste des personnages disponibles
        self.selected_character = None
        
        # Dimensions et espacement des rectangles de personnage
        self.char_width = 120
        self.char_height = 160
        self.margin = 20
        self.chars_per_row = 3
        
        # Zone d'affichage des stats (à droite)
        self.stats_panel_width = 250
        self.stats_panel_x = self.screen_width - self.stats_panel_width - 20
        self.stats_panel_y = 120
        self.stats_panel_height = 350
        
        # Couleurs
        self.background_color = (30, 30, 50)
        self.rect_color = (80, 80, 100)
        self.selected_color = (120, 180, 120)
        self.text_color = (255, 255, 255)
        self.stats_bg_color = (50, 50, 70)
        self.stat_bar_bg_color = (60, 60, 80)
        self.stat_bar_color = (180, 140, 220)
        self.button_color = (100, 150, 200)
        self.button_hover_color = (120, 170, 220)
        
        # Initialisation de la police
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 40)
        self.char_font = pygame.font.SysFont('Arial', 20)
        self.stats_title_font = pygame.font.SysFont('Arial', 28)
        self.stats_font = pygame.font.SysFont('Arial', 22)
        self.button_font = pygame.font.SysFont('Arial', 24)
        
        # Bouton de confirmation
        self.confirm_button = pygame.Rect(
            self.screen_width // 2 - 100,
            self.screen_height - 80,
            200, 50
        )
        self.button_active = False
        
    def _calculate_char_position(self, index):
        """Calcule la position d'un personnage basé sur son index"""
        # Ajuster la largeur disponible pour tenir compte du panneau de stats
        available_width = self.screen_width - self.stats_panel_width - 40  # 20px de marge de chaque côté
        
        row = index // self.chars_per_row
        col = index % self.chars_per_row
        
        total_width = self.chars_per_row * self.char_width + (self.chars_per_row - 1) * self.margin
        start_x = (available_width - total_width) // 2
        
        x = start_x + col * (self.char_width + self.margin)
        y = 120 + row * (self.char_height + self.margin)
        
        return (x, y)
    
    def draw(self):
        """Dessine l'écran de sélection de personnage"""
        # Fond d'écran
        self.screen.fill(self.background_color)
        
        # Titre
        title_surface = self.title_font.render('Sélectionnez votre personnage', True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Dessiner chaque personnage
        for i, character in enumerate(self.characters):
            pos = self._calculate_char_position(i)
            char_rect = pygame.Rect(pos[0], pos[1], self.char_width, self.char_height)
            
            # Dessiner le rectangle (sera remplacé par l'image du personnage)
            color = self.selected_color if character == self.selected_character else self.rect_color
            pygame.draw.rect(self.screen, color, char_rect)
            
            # Nom du personnage
            name_surface = self.char_font.render(character['name'], True, self.text_color)
            name_rect = name_surface.get_rect(center=(pos[0] + self.char_width // 2, pos[1] + self.char_height + 15))
            self.screen.blit(name_surface, name_rect)
            
            # Ici vous pourriez ajouter du code pour dessiner l'image du personnage
            # Exemple: self.screen.blit(character['image'], char_rect)
        
        # Dessiner le panneau de stats si un personnage est sélectionné
        if self.selected_character:
            self._draw_stats_panel()
        
        # Dessiner le bouton de confirmation
        button_color = self.button_hover_color if self.button_active else self.button_color
        pygame.draw.rect(self.screen, button_color, self.confirm_button, border_radius=5)
        
        # Texte du bouton
        button_text = "Confirmer" if self.selected_character else "Sélectionnez un personnage"
        button_surface = self.button_font.render(button_text, True, self.text_color)
        button_rect = button_surface.get_rect(center=self.confirm_button.center)
        self.screen.blit(button_surface, button_rect)
        
        # Mettre à jour l'écran
        pygame.display.flip()
    
    def _draw_stats_panel(self):
        """Dessine le panneau de statistiques du personnage sélectionné"""
        # Panneau de fond
        stats_panel = pygame.Rect(
            self.stats_panel_x, 
            self.stats_panel_y, 
            self.stats_panel_width, 
            self.stats_panel_height
        )
        pygame.draw.rect(self.screen, self.stats_bg_color, stats_panel, border_radius=10)
        
        # Titre du panneau
        title_surface = self.stats_title_font.render(self.selected_character['name'], True, self.text_color)
        title_rect = title_surface.get_rect(center=(stats_panel.centerx, self.stats_panel_y + 30))
        self.screen.blit(title_surface, title_rect)
        
        # Grand rectangle pour l'image du personnage
        char_display_rect = pygame.Rect(
            self.stats_panel_x + 50, 
            self.stats_panel_y + 70,
            150, 
            150
        )
        pygame.draw.rect(self.screen, self.rect_color, char_display_rect)
        # Ici vous pourriez dessiner une version plus grande de l'image:
        # self.screen.blit(pygame.transform.scale(self.selected_character['image'], (150, 150)), char_display_rect)
        
        # Dessiner les barres de statistiques
        self._draw_stat_bars()
    
    def _draw_stat_bars(self):
        """Dessine les barres de statistiques du personnage sélectionné"""
        # Liste des statistiques à afficher
        stats_to_display = [
            ("Force", self.selected_character.get('strength', 0)),
            ("Vitesse", self.selected_character.get('speed', 0)),
            ("Intelligence", self.selected_character.get('intelligence', 0)),
            ("Défense", self.selected_character.get('defense', 0))
        ]
        
        # Paramètres des barres
        bar_width = 180
        bar_height = 20
        bar_spacing = 40
        start_y = self.stats_panel_y + 240
        
        # Dessiner chaque barre de statistique
        for i, (stat_name, stat_value) in enumerate(stats_to_display):
            # Position Y de la barre courante
            current_y = start_y + i * bar_spacing
            
            # Texte de la statistique
            stat_text = self.stats_font.render(stat_name, True, self.text_color)
            self.screen.blit(stat_text, (self.stats_panel_x + 20, current_y))
            
            # Valeur de la statistique
            value_text = self.stats_font.render(str(stat_value), True, self.text_color)
            value_rect = value_text.get_rect(midright=(self.stats_panel_x + self.stats_panel_width - 20, current_y + 10))
            self.screen.blit(value_text, value_rect)
            
            # Fond de la barre
            bar_bg_rect = pygame.Rect(
                self.stats_panel_x + 20,
                current_y + 25,
                bar_width,
                bar_height
            )
            pygame.draw.rect(self.screen, self.stat_bar_bg_color, bar_bg_rect, border_radius=5)
            
            # Barre de progression (maximum 10)
            max_stat = 10
            fill_width = min(stat_value / max_stat, 1.0) * bar_width
            if fill_width > 0:
                bar_fill_rect = pygame.Rect(
                    self.stats_panel_x + 20,
                    current_y + 25,
                    fill_width,
                    bar_height
                )
                pygame.draw.rect(self.screen, self.stat_bar_color, bar_fill_rect, border_radius=5)
    
    def handle_event(self, event):
        """Gère les événements de l'écran de sélection"""
        if event.type == pygame.MOUSEMOTION:
            # Vérifier si la souris survole le bouton
            self.button_active = self.confirm_button.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si un personnage est cliqué
            for i, character in enumerate(self.characters):
                pos = self._calculate_char_position(i)
                char_rect = pygame.Rect(pos[0], pos[1], self.char_width, self.char_height)
                
                if char_rect.collidepoint(event.pos):
                    self.selected_character = character
                    return None  # Personnage sélectionné mais pas encore confirmé
            
            # Vérifier si le bouton de confirmation est cliqué
            if self.confirm_button.collidepoint(event.pos) and self.selected_character:
                return self.selected_character  # Retourner le personnage sélectionné
        
        return None  # Aucune action définitive
    
    def run(self):
        """Boucle principale de l'écran de sélection"""
        running = True
        
        while running:
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                result = self.handle_event(event)
                if result:
                    return result  # Personnage sélectionné et confirmé
            
            pygame.time.delay(30)


class SelectionMenu(Screen):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Selection"
        
        # Exemple de personnages avec stats (à adapter selon vos besoins)
        self.characters = [
            {"name": "Guerrier", "speed": 5, "strength": 8, "intelligence": 4, "defense": 7},
            {"name": "Mage", "speed": 6, "strength": 3, "intelligence": 9, "defense": 4},
            {"name": "Archer", "speed": 8, "strength": 6, "intelligence": 6, "defense": 5},
            {"name": "Paladin", "speed": 4, "strength": 7, "intelligence": 5, "defense": 9},
            {"name": "Voleur", "speed": 9, "strength": 5, "intelligence": 7, "defense": 3},
        ]
        
        self.selected_character = None
        self._init_ui()

    def _init_ui(self):
        # Reprendre les constantes et configurations de CharacterSelectionScreen
        self.char_width = 120
        self.char_height = 160
        self.margin = 20
        self.chars_per_row = 3
        
        self.stats_panel_width = 250
        self.stats_panel_x = self.width - self.stats_panel_width - 20
        self.stats_panel_y = 120
        self.stats_panel_height = 350
        
        self.background_color = (30, 30, 50)
        self.rect_color = (80, 80, 100)
        self.selected_color = (120, 180, 120)
        self.text_color = (255, 255, 255)
        self.stats_bg_color = (50, 50, 70)
        self.stat_bar_bg_color = (60, 60, 80)
        self.stat_bar_color = (180, 140, 220)
        self.button_color = (100, 150, 200)
        self.button_hover_color = (120, 170, 220)
        
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 40)
        self.char_font = pygame.font.SysFont('Arial', 20)
        self.stats_title_font = pygame.font.SysFont('Arial', 28)
        self.stats_font = pygame.font.SysFont('Arial', 22)
        self.button_font = pygame.font.SysFont('Arial', 24)
        
        self.confirm_button = pygame.Rect(
            self.width // 2 - 100,
            self.height - 80,
            200, 50
        )
        self.button_active = False

    def update(self, dt):
        pass

    def draw(self):
        self.surface.fill(self.background_color)
        
        # Reprendre la logique de dessin de CharacterSelectionScreen
        title_surface = self.title_font.render('Sélectionnez votre personnage', True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.width // 2, 50))
        self.surface.blit(title_surface, title_rect)
        
        for i, character in enumerate(self.characters):
            pos = self._calculate_char_position(i)
            char_rect = pygame.Rect(pos[0], pos[1], self.char_width, self.char_height)
            
            color = self.selected_color if character == self.selected_character else self.rect_color
            pygame.draw.rect(self.surface, color, char_rect)
            
            name_surface = self.char_font.render(character['name'], True, self.text_color)
            name_rect = name_surface.get_rect(center=(pos[0] + self.char_width // 2, pos[1] + self.char_height + 15))
            self.surface.blit(name_surface, name_rect)
        
        if self.selected_character:
            self._draw_stats_panel()
        
        button_color = self.button_hover_color if self.button_active else self.button_color
        pygame.draw.rect(self.surface, button_color, self.confirm_button, border_radius=5)
        
        button_text = "Confirmer" if self.selected_character else "Sélectionnez un personnage"
        button_surface = self.button_font.render(button_text, True, self.text_color)
        button_rect = button_surface.get_rect(center=self.confirm_button.center)
        self.surface.blit(button_surface, button_rect)
        
        return self.surface

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.button_active = self.confirm_button.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, character in enumerate(self.characters):
                pos = self._calculate_char_position(i)
                char_rect = pygame.Rect(pos[0], pos[1], self.char_width, self.char_height)
                
                if char_rect.collidepoint(event.pos):
                    self.selected_character = character
                    return None
            
            if self.confirm_button.collidepoint(event.pos) and self.selected_character:
                return self.selected_character
        
        return None

    def _calculate_char_position(self, index):
        available_width = self.width - self.stats_panel_width - 40
        
        row = index // self.chars_per_row
        col = index % self.chars_per_row
        
        total_width = self.chars_per_row * self.char_width + (self.chars_per_row - 1) * self.margin
        start_x = (available_width - total_width) // 2
        
        x = start_x + col * (self.char_width + self.margin)
        y = 120 + row * (self.char_height + self.margin)
        
        return (x, y)

    def _draw_stats_panel(self):
        stats_panel = pygame.Rect(
            self.stats_panel_x, 
            self.stats_panel_y, 
            self.stats_panel_width, 
            self.stats_panel_height
        )
        pygame.draw.rect(self.surface, self.stats_bg_color, stats_panel, border_radius=10)
        
        title_surface = self.stats_title_font.render(self.selected_character['name'], True, self.text_color)
        title_rect = title_surface.get_rect(center=(stats_panel.centerx, self.stats_panel_y + 30))
        self.surface.blit(title_surface, title_rect)
        
        char_display_rect = pygame.Rect(
            self.stats_panel_x + 50, 
            self.stats_panel_y + 70,
            150, 
            150
        )
        pygame.draw.rect(self.surface, self.rect_color, char_display_rect)
        
        self._draw_stat_bars()

    def _draw_stat_bars(self):
        stats_to_display = [
            ("Force", self.selected_character.get('strength', 0)),
            ("Vitesse", self.selected_character.get('speed', 0)),
            ("Intelligence", self.selected_character.get('intelligence', 0)),
            ("Défense", self.selected_character.get('defense', 0))
        ]
        
        bar_width = 180
        bar_height = 20
        bar_spacing = 40
        start_y = self.stats_panel_y + 240
        
        for i, (stat_name, stat_value) in enumerate(stats_to_display):
            current_y = start_y + i * bar_spacing
            
            stat_text = self.stats_font.render(stat_name, True, self.text_color)
            self.surface.blit(stat_text, (self.stats_panel_x + 20, current_y))
            
            value_text = self.stats_font.render(str(stat_value), True, self.text_color)
            value_rect = value_text.get_rect(midright=(self.stats_panel_x + self.stats_panel_width - 20, current_y + 10))
            self.surface.blit(value_text, value_rect)
            
            bar_bg_rect = pygame.Rect(
                self.stats_panel_x + 20,
                current_y + 25,
                bar_width,
                bar_height
            )
            pygame.draw.rect(self.surface, self.stat_bar_bg_color, bar_bg_rect, border_radius=5)
            
            max_stat = 10
            fill_width = min(stat_value / max_stat, 1.0) * bar_width
            if fill_width > 0:
                bar_fill_rect = pygame.Rect(
                    self.stats_panel_x + 20,
                    current_y + 25,
                    fill_width,
                    bar_height
                )
                pygame.draw.rect(self.surface, self.stat_bar_color, bar_fill_rect, border_radius=5)


# Exemple d'utilisation
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((900, 650))
    pygame.display.set_caption("Sélection de Personnage")
    
    # Exemple de personnages avec stats (à remplacer par vos vrais personnages)
    characters = [
        {"name": "Guerrier", "speed": 5, "strength": 8, "intelligence": 4, "defense": 7},
        {"name": "Mage", "speed": 6, "strength": 3, "intelligence": 9, "defense": 4},
        {"name": "Archer", "speed": 8, "strength": 6, "intelligence": 6, "defense": 5},
        {"name": "Paladin", "speed": 4, "strength": 7, "intelligence": 5, "defense": 9},
        {"name": "Voleur", "speed": 9, "strength": 5, "intelligence": 7, "defense": 3},
        {"name": "Druide", "speed": 6, "strength": 5, "intelligence": 8, "defense": 6},
        {"name": "Barde", "speed": 7, "strength": 4, "intelligence": 7, "defense": 5}
    ]
    
    # Pour ajouter des images, vous pourriez faire:
    # for character in characters:
    #     img_path = os.path.join("assets", "characters", f"{character['name'].lower()}.png")
    #     character['image'] = pygame.image.load(img_path)
    
    selection_screen = CharacterSelectionScreen(screen, characters)
    selected_character = selection_screen.run()
    
    if selected_character:
        print(f"Personnage sélectionné: {selected_character['name']}")
    else:
        print("Aucun personnage sélectionné")
    
    pygame.quit()