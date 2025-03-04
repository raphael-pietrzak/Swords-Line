import pygame
import time
from settings import *
from ui.components import Button


class LogsTab:
    def __init__(self, ui_context, server_data):
        self.width = ui_context.width
        self.height = ui_context.height
        self.font_normal = ui_context.font_normal
        self.font_small = ui_context.font_small

        # Données du serveur
        self.server_data = server_data
        
        self.logs = server_data.logs
        self.max_logs = 100
        self.scroll_position = 0
        
        # Boutons spécifiques à cet onglet
        self.buttons = [
            Button(pygame.Rect(self.width - 250, 60, 200, 40), "Effacer les logs", self.server_data.clear_logs)
        ]
    

    
    def update(self):
        # Mettre à jour l'état des boutons
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
    
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return True
        
        # Gestion du défilement
        if event.type == pygame.MOUSEWHEEL:
            max_scroll = max(0, len(self.logs) - 20)
            self.scroll_position = max(0, min(self.scroll_position - event.y, max_scroll))
            return True
        
        return False
    
    def draw(self, screen):
        # Titre de l'onglet
        title = self.font_normal.render("Logs du Serveur", True, TEXT_COLOR)
        screen.blit(title, (20, 60))
        
        # Dessiner les boutons
        for button in self.buttons:
            button.draw(screen, self.font_small)
        
        # Cadre pour les logs
        log_rect = pygame.Rect(50, 120, self.width - 100, self.height - 200)
        pygame.draw.rect(screen, (20, 20, 30), log_rect)
        pygame.draw.rect(screen, TEXT_COLOR, log_rect, 1)
        
        # Afficher les logs
        if not self.logs:
            no_logs = self.font_normal.render("Aucun log disponible", True, TEXT_COLOR)
            screen.blit(no_logs, (log_rect.centerx - no_logs.get_width() // 2, 
                                 log_rect.centery - no_logs.get_height() // 2))
        else:
            visible_logs = self.logs[self.scroll_position:self.scroll_position + 20]
            for i, log in enumerate(visible_logs):
                # Couleur basée sur le type de log
                color = TEXT_COLOR
                if log["type"] == "ERROR":
                    color = ERROR_COLOR
                elif log["type"] == "WARNING":
                    color = WARNING_COLOR
                elif log["type"] == "SUCCESS":
                    color = SUCCESS_COLOR
                
                log_text = self.font_small.render(f"[{log['time']}] [{log['type']}] {log['message']}", True, color)
                screen.blit(log_text, (60, 130 + i * 25))
        
        # Indicateur de défilement si nécessaire
        if len(self.logs) > 20:
            scroll_height = log_rect.height * min(1, 20 / len(self.logs))
            scroll_pos = log_rect.height * (self.scroll_position / len(self.logs))
            scroll_rect = pygame.Rect(log_rect.right + 10, log_rect.top + scroll_pos, 10, scroll_height)
            pygame.draw.rect(screen, TEXT_COLOR, scroll_rect)
