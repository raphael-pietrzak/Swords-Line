import pygame
from settings import *
from ui_components import Button


class ConfigTab:
    def __init__(self, width, height, font_normal, font_small):
        self.width = width
        self.height = height
        self.font_normal = font_normal
        self.font_small = font_small
        
        # Paramètres de configuration
        self.config = {
            "port": 5555,
            "max_players": 50,
            "tick_rate": 20,
            "log_level": "INFO",
            "auto_restart": False
        }
        
        # Boutons spécifiques à cet onglet
        self.buttons = [
            Button(pygame.Rect(width - 250, 60, 200, 40), "Sauvegarder", self.save_config)
        ]
    
    def save_config(self):
        print("Configuration sauvegardée")
    
    def update(self, server_data):
        # Mettre à jour l'état des boutons
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
    
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
    
    def draw(self, screen):
        # Titre de l'onglet
        title = self.font_normal.render("Configuration du Serveur", True, TEXT_COLOR)
        screen.blit(title, (20, 60))
        
        # Dessiner les boutons
        for button in self.buttons:
            button.draw(screen, self.font_small)
        
        # Afficher les paramètres de configuration
        y_pos = 120
        for key, value in self.config.items():
            # Étiquette
            label = self.font_normal.render(f"{key}:", True, TEXT_COLOR)
            screen.blit(label, (50, y_pos))
            
            # Valeur
            value_text = self.font_normal.render(str(value), True, TEXT_COLOR)
            screen.blit(value_text, (300, y_pos))
            
            # Ligne de séparation
            pygame.draw.line(screen, TEXT_COLOR, (50, y_pos + 30), (self.width - 100, y_pos + 30), 1)
            
            y_pos += 60
