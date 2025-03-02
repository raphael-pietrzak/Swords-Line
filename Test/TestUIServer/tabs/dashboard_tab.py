import pygame
import time
from settings import *
from ui_components import Button

class DashboardTab:
    def __init__(self, ui_context, server_data):
        self.width = ui_context.width
        self.height = ui_context.height
        self.font_normal = ui_context.font_normal
        self.font_small = ui_context.font_small

        # Données du serveur
        self.server_data = server_data
        
        # Boutons spécifiques à cet onglet
        self.buttons = [
            Button(pygame.Rect(50, 120, 200, 40), "Démarrer Serveur", self.start_server, True),
            Button(pygame.Rect(260, 120, 200, 40), "Arrêter Serveur", self.stop_server, False),
            Button(pygame.Rect(470, 120, 200, 40), "Message Global", self.broadcast_message, False),
        ]
        
        # État du serveur
        self.server_running = False
        self.uptime_start = 0
        
        # Statistiques pour affichage
        self.stats = {
            'total_players': 0,
            'total_rooms': 0,
            'messages_sent': 0,
            'uptime': 0
        }
    
    def start_server(self):
        self.server_running = True
        self.uptime_start = time.time()
        self.buttons[0].enabled = False  # Désactiver "Démarrer"
        self.buttons[1].enabled = True   # Activer "Arrêter"
        self.buttons[2].enabled = True   # Activer "Message"

        self.server_data.add_log("Serveur démarré")
        print("Serveur démarré")
    
    def stop_server(self):
        self.server_running = False
        self.stats['uptime'] = 0
        self.buttons[0].enabled = True   # Activer "Démarrer"
        self.buttons[1].enabled = False  # Désactiver "Arrêter"
        self.buttons[2].enabled = False  # Désactiver "Message"

        self.server_data.add_log("Serveur arrêté")
        print("Serveur arrêté")
    
    def format_time(self, seconds):
        # Convertir les secondes en heures:minutes:secondes
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02}:{m:02}:{s:02}"
    
    def broadcast_message(self):
        if self.server_running:
            print("Message global envoyé")
    
    def update(self):
        # Mettre à jour les statistiques à partir des données du serveur
        self.stats['total_players'] = len(self.server_data.players)
        self.stats['total_rooms'] = len(self.server_data.rooms)
        
        if self.server_running:
            self.stats['uptime'] = int(time.time() - self.uptime_start)
        
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
        title = self.font_normal.render("Tableau de bord", True, TEXT_COLOR)
        screen.blit(title, (20, 60))
        
        # Dessiner les boutons
        for button in self.buttons:
            button.draw(screen, self.font_small)
        
        # Afficher le statut du serveur
        status_text = "En ligne" if self.server_running else "Hors ligne"
        status_color = SUCCESS_COLOR if self.server_running else ERROR_COLOR
        status = self.font_normal.render(f"Statut: {status_text}", True, status_color)
        screen.blit(status, (700, 130))
        
        # Afficher les statistiques générales
        stats_y = 200
        stats_texts = [
            f"Joueurs connectés: {self.stats['total_players']}",
            f"Rooms actives: {self.stats['total_rooms']}",
            f"Messages échangés: {self.stats['messages_sent']}",
            f"Temps d'activité: {self.format_time(self.stats['uptime'])}"
        ]
        
        for text in stats_texts:
            stat_text = self.font_normal.render(text, True, TEXT_COLOR)
            screen.blit(stat_text, (50, stats_y))
            stats_y += 40
        
        # Dessiner un aperçu des rooms (version simplifiée)
        room_preview_y = 400
        title = self.font_normal.render("Aperçu des rooms:", True, TEXT_COLOR)
        screen.blit(title, (50, room_preview_y - 40))
        
        # Rectangle pour l'aperçu
        preview_rect = pygame.Rect(50, room_preview_y, self.width - 100, 250)
        pygame.draw.rect(screen, (40, 40, 50), preview_rect)
        pygame.draw.rect(screen, TEXT_COLOR, preview_rect, 1)
        
        # Si pas de rooms actives
        if self.stats['total_rooms'] == 0:
            no_rooms = self.font_normal.render("Aucune room active", True, TEXT_COLOR)
            screen.blit(no_rooms, (preview_rect.centerx - no_rooms.get_width() // 2, 
                                 preview_rect.centery - no_rooms.get_height() // 2))