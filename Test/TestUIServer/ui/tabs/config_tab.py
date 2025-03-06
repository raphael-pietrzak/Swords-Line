import pygame
from settings import *
from ui.components import Button


class ConfigTab:
    def __init__(self, ui_context, server):
        self.width = ui_context.width
        self.height = ui_context.height
        self.font_normal = ui_context.font_normal
        self.font_small = ui_context.font_small

        # Données du serveur
        self.server = server
        
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
            Button(pygame.Rect(self.width - 250, 60, 200, 40), "Sauvegarder", self.save_config)
        ]
    
    def save_config(self):
        print("Configuration sauvegardée")
    
    def update(self):
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
