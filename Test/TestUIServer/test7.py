import pygame
import time
import random  # Pour les données de démonstration
from enum import Enum

# Configuration de base
WIDTH, HEIGHT = 1024, 768
FPS = 60
BACKGROUND_COLOR = (30, 30, 40)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (70, 70, 100)
BUTTON_HOVER_COLOR = (90, 90, 120)
BUTTON_TEXT_COLOR = (240, 240, 240)
TAB_INACTIVE_COLOR = (50, 50, 70)
TAB_ACTIVE_COLOR = (70, 70, 100)
SUCCESS_COLOR = (0, 200, 0)
WARNING_COLOR = (200, 200, 0)
ERROR_COLOR = (200, 0, 0)

# Énumération des onglets
class Tab(Enum):
    DASHBOARD = 0
    ROOMS = 1
    LOGS = 2
    CONFIG = 3

class Button:
    def __init__(self, rect, text, action, enabled=True, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.rect = rect
        self.text = text
        self.action = action
        self.enabled = enabled
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos) and self.enabled
    
    def draw(self, screen, font):
        # Déterminer la couleur du bouton
        if not self.enabled:
            color = (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2)
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color
        
        # Dessiner le bouton
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 1)
        
        # Dessiner le texte
        button_text = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_x = self.rect.x + (self.rect.width - button_text.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - button_text.get_height()) // 2
        screen.blit(button_text, (text_x, text_y))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.enabled and self.action:
                self.action()
                return True
        return False

class TabButton(Button):
    def __init__(self, rect, text, tab_value, active=False):
        super().__init__(rect, text, None, True)
        self.tab_value = tab_value
        self.active = active
    
    def draw(self, screen, font):
        # Couleur basée sur l'état actif/inactif
        color = TAB_ACTIVE_COLOR if self.active else TAB_INACTIVE_COLOR
        
        # Dessiner le fond du tab
        pygame.draw.rect(screen, color, self.rect)
        
        # Dessiner la bordure (sauf en bas si actif)
        if self.active:
            # Dessiner uniquement les 3 côtés (gauche, haut, droite)
            pygame.draw.line(screen, TEXT_COLOR, self.rect.topleft, (self.rect.right, self.rect.top))
            pygame.draw.line(screen, TEXT_COLOR, self.rect.topleft, (self.rect.left, self.rect.bottom))
            pygame.draw.line(screen, TEXT_COLOR, (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom))
        else:
            pygame.draw.rect(screen, TEXT_COLOR, self.rect, 1)
        
        # Dessiner le texte
        button_text = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_x = self.rect.x + (self.rect.width - button_text.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - button_text.get_height()) // 2
        screen.blit(button_text, (text_x, text_y))

class Room:
    def __init__(self, room_id, name, max_players=8):
        self.id = room_id
        self.name = name
        self.max_players = max_players
        self.players = []  # Liste des joueurs dans cette room
        self.created_at = time.time()
    
    @property
    def player_count(self):
        return len(self.players)

class Player:
    def __init__(self, player_id, name, character_type=None):
        self.id = player_id
        self.name = name
        self.character_type = character_type
        self.position = (random.randint(50, 350), random.randint(50, 250))  # Position aléatoire pour la démonstration
        self.room_id = None
        self.connected_at = time.time()
        self.level = random.randint(1, 10)  # Niveau aléatoire pour la démonstration
    
    def move_to(self, x, y):
        self.position = (x, y)

class DashboardTab:
    def __init__(self, width, height, font_normal, font_small):
        self.width = width
        self.height = height
        self.font_normal = font_normal
        self.font_small = font_small
        
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
        
        print("Serveur démarré")
    
    def stop_server(self):
        self.server_running = False
        self.stats['uptime'] = 0
        self.buttons[0].enabled = True   # Activer "Démarrer"
        self.buttons[1].enabled = False  # Désactiver "Arrêter"
        self.buttons[2].enabled = False  # Désactiver "Message"
        
        print("Serveur arrêté")
    
    def format_time(self, seconds):
        # Convertir les secondes en heures:minutes:secondes
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02}:{m:02}:{s:02}"
    
    def broadcast_message(self):
        if self.server_running:
            print("Message global envoyé")
    
    def update(self, server_data):
        # Mettre à jour les statistiques à partir des données du serveur
        self.stats['total_players'] = len(server_data.players)
        self.stats['total_rooms'] = len(server_data.rooms)
        
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

class RoomsTab:
    def __init__(self, width, height, font_normal, font_small, font_title):
        self.width = width
        self.height = height
        self.font_normal = font_normal
        self.font_small = font_small
        self.font_title = font_title
        
        # Boutons spécifiques à cet onglet
        self.buttons = [
            Button(pygame.Rect(width - 250, 60, 200, 40), "Nouvelle Room", self.create_room)
        ]
        
        # État interne
        self.rooms = []  # Référence aux rooms du serveur
        self.selected_room = None
        self.viewing_room_details = False
        
        # Boutons dynamiques pour les rooms (initialisés dans update)
        self.room_buttons = []
        
        # Boutons pour la vue détaillée
        self.detail_buttons = [
            Button(pygame.Rect(50, height - 80, 150, 40), "Retour", self.back_to_rooms),
            Button(pygame.Rect(220, height - 80, 200, 40), "Message à la room", self.message_room),
            Button(pygame.Rect(440, height - 80, 150, 40), "Supprimer room", self.delete_room, color=ERROR_COLOR)
        ]
    
    def create_room(self):
        print("Nouvelle room créée")
    
    def view_room(self, room):
        self.selected_room = room
        self.viewing_room_details = True
        print(f"Affichage des détails de la room: {room.name}")
    
    def back_to_rooms(self):
        self.viewing_room_details = False
        self.selected_room = None
    
    def message_room(self):
        if self.selected_room:
            print(f"Message envoyé à la room: {self.selected_room.name}")
    
    def delete_room(self):
        if self.selected_room:
            print(f"Room supprimée: {self.selected_room.name}")
            self.viewing_room_details = False
            self.selected_room = None
    
    def expel_player(self, player):
        if self.selected_room and player:
            print(f"Joueur {player.name} expulsé de la room {self.selected_room.name}")
    
    def update(self, server_data):
        self.rooms = server_data.rooms
        
        # Mettre à jour l'état des boutons
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
        
        # Si on est dans la vue détaillée, mettre à jour ces boutons également
        if self.viewing_room_details:
            for button in self.detail_buttons:
                button.update(pygame.mouse.get_pos())
        
        # Créer les boutons dynamiques pour chaque room
        self.room_buttons = []
        for i, room in enumerate(self.rooms):
            y_pos = 120 + i * 60
            
            # Bouton "Voir"
            view_btn = Button(
                pygame.Rect(self.width - 350, y_pos + 10, 100, 40), 
                "Voir", 
                lambda r=room: self.view_room(r)
            )
            
            # Bouton "Supprimer"
            delete_btn = Button(
                pygame.Rect(self.width - 230, y_pos + 10, 150, 40), 
                "Supprimer", 
                lambda r=room: self.delete_room(),
                color=ERROR_COLOR
            )
            
            self.room_buttons.append(view_btn)
            self.room_buttons.append(delete_btn)
            
            # Mettre à jour l'état de ces boutons
            view_btn.update(pygame.mouse.get_pos())
            delete_btn.update(pygame.mouse.get_pos())
    
    def handle_event(self, event):
        # Si on est dans la vue détaillée
        if self.viewing_room_details:
            for button in self.detail_buttons:
                if button.handle_event(event):
                    return True
            return False
        
        # Vue principale des rooms
        for button in self.buttons:
            if button.handle_event(event):
                return True
        
        for button in self.room_buttons:
            if button.handle_event(event):
                return True
        
        return False
    
    def draw(self, screen):
        if self.viewing_room_details and self.selected_room:
            self.draw_room_details(screen)
        else:
            self.draw_rooms_list(screen)
    
    def draw_rooms_list(self, screen):
        # Titre de l'onglet
        title = self.font_normal.render("Gestion des Rooms", True, TEXT_COLOR)
        screen.blit(title, (20, 60))
        
        # Dessiner le bouton "Nouvelle Room"
        for button in self.buttons:
            button.draw(screen, self.font_small)
        
        # En-tête du tableau
        headers = ["Room", "Joueurs", "Actions"]
        header_widths = [400, 150, 300]
        header_x = 50
        
        for i, header in enumerate(headers):
            header_text = self.font_normal.render(header, True, TEXT_COLOR)
            screen.blit(header_text, (header_x, 100))
            header_x += header_widths[i]
        
        # Ligne de séparation
        pygame.draw.line(screen, TEXT_COLOR, (50, 125), (self.width - 50, 125), 1)
        
        # Liste des rooms
        if not self.rooms:
            no_rooms = self.font_normal.render("Aucune room active", True, TEXT_COLOR)
            screen.blit(no_rooms, (self.width // 2 - no_rooms.get_width() // 2, 200))
        else:
            for i, room in enumerate(self.rooms):
                y_pos = 120 + i * 60
                
                # Nom de la room
                room_name = self.font_normal.render(room.name, True, TEXT_COLOR)
                screen.blit(room_name, (50, y_pos + 20))
                
                # Nombre de joueurs
                player_count = self.font_normal.render(f"{room.player_count}/{room.max_players}", True, TEXT_COLOR)
                screen.blit(player_count, (450, y_pos + 20))
                
                # Dessiner les boutons d'action
                self.room_buttons[i*2].draw(screen, self.font_small)     # Bouton "Voir"
                self.room_buttons[i*2+1].draw(screen, self.font_small)   # Bouton "Supprimer"
                
                # Ligne de séparation
                pygame.draw.line(screen, TEXT_COLOR, (50, y_pos + 60), (self.width - 50, y_pos + 60), 1)
    
    def draw_room_details(self, screen):
        room = self.selected_room
        
        # Titre avec nom de la room
        title = self.font_title.render(f"Room: {room.name}", True, TEXT_COLOR)
        screen.blit(title, (50, 60))
        
        # Informations de base
        info_text = self.font_normal.render(f"Joueurs: {room.player_count}/{room.max_players}", True, TEXT_COLOR)
        screen.blit(info_text, (50, 100))
        
        # Mini-carte
        map_rect = pygame.Rect(50, 140, 400, 300)
        pygame.draw.rect(screen, (20, 20, 30), map_rect)
        pygame.draw.rect(screen, TEXT_COLOR, map_rect, 1)
        
        # Dessiner les joueurs sur la mini-carte
        for player in room.players:
            # Couleur basée sur le type de personnage
            color = (255, 0, 0)  # Rouge par défaut
            if player.character_type == "warrior":
                color = (255, 0, 0)
            elif player.character_type == "mage":
                color = (0, 0, 255)
            elif player.character_type == "archer":
                color = (0, 255, 0)
            
            # Position du joueur
            pygame.draw.circle(screen, color, player.position, 8)
            
            # ID du joueur
            player_id = self.font_small.render(player.name, True, TEXT_COLOR)
            screen.blit(player_id, (player.position[0] - player_id.get_width() // 2, 
                                   player.position[1] + 10))
        
        # Liste des joueurs
        player_list_title = self.font_normal.render("Joueurs dans cette room:", True, TEXT_COLOR)
        screen.blit(player_list_title, (500, 140))
        
        for i, player in enumerate(room.players):
            y_pos = 180 + i * 40
            
            # Informations sur le joueur
            char_info = f" - {player.character_type}" if player.character_type else ""
            player_info = self.font_small.render(f"{player.name}{char_info} - Niv.{player.level}", True, TEXT_COLOR)
            screen.blit(player_info, (520, y_pos))
            
            # Bouton "Expulser"
            expel_btn_rect = pygame.Rect(800, y_pos - 5, 100, 30)
            expel_btn = Button(
                expel_btn_rect,
                "Expulser",
                lambda p=player: self.expel_player(p),
                color=WARNING_COLOR
            )
            expel_btn.update(pygame.mouse.get_pos())
            expel_btn.draw(screen, self.font_small)
        
        # Boutons d'action
        for button in self.detail_buttons:
            button.draw(screen, self.font_small)

class LogsTab:
    def __init__(self, width, height, font_normal, font_small):
        self.width = width
        self.height = height
        self.font_normal = font_normal
        self.font_small = font_small
        
        self.logs = []
        self.max_logs = 100
        self.scroll_position = 0
        
        # Boutons spécifiques à cet onglet
        self.buttons = [
            Button(pygame.Rect(width - 250, 60, 200, 40), "Effacer les logs", self.clear_logs)
        ]
    
    def add_log(self, message, log_type="INFO"):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.logs.append({"time": timestamp, "type": log_type, "message": message})
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
    
    def clear_logs(self):
        self.logs = []
        self.scroll_position = 0
    
    def update(self, server_data):
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

class ServerData:
    """Classe qui simule les données du serveur"""
    def __init__(self):
        self.players = []
        self.rooms = []
    
    def generate_demo_data(self):
        # Générer des données de démonstration
        character_types = ["warrior", "mage", "archer", "healer"]
        
        # Générer quelques rooms
        for i in range(3):
            room = Room(f"room_{i}", f"Room {i+1}")
            self.rooms.append(room)
        
        # Générer quelques joueurs
        for i in range(15):
            player = Player(f"player_{i}", f"Player{i}", random.choice(character_types))
            self.players.append(player)
            
            # Assigner certains joueurs à des rooms
            if i < 10:  # les 10 premiers joueurs
                room_idx = random.randint(0, len(self.rooms) - 1)
                room = self.rooms[room_idx]
                player.room_id = room.id
                room.players.append(player)

class TabbedServerUI:
    def __init__(self):
        # Initialisation de pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Swords Line - Serveur")
        self.clock = pygame.time.Clock()
        
        # Polices
        self.font_title = pygame.font.SysFont('Arial', 32)
        self.font_normal = pygame.font.SysFont('Arial', 20)
        self.font_small = pygame.font.SysFont('Arial', 16)
        
        # Création des onglets
        self.tabs = [
            {"value": Tab.DASHBOARD, "text": "Dashboard", "active": True},
            {"value": Tab.ROOMS, "text": "Rooms", "active": False},
            {"value": Tab.LOGS, "text": "Logs", "active": False},
            {"value": Tab.CONFIG, "text": "Configuration", "active": False}
        ]
        
        # Créer les boutons d'onglets
        tab_width = 150
        self.tab_buttons = []
        
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(50 + i * tab_width, 10, tab_width, 40)
            tab_button = TabButton(tab_rect, tab["text"], tab["value"], tab["active"])
            self.tab_buttons.append(tab_button)
        
        # Onglet actif
        self.active_tab = Tab.DASHBOARD
        
        # Contenu des onglets
        self.dashboard_tab = DashboardTab(WIDTH, HEIGHT, self.font_normal, self.font_small)
        self.rooms_tab = RoomsTab(WIDTH, HEIGHT, self.font_normal, self.font_small, self.font_title)
        self.logs_tab = LogsTab(WIDTH, HEIGHT, self.font_normal, self.font_small)
        self.config_tab = ConfigTab(WIDTH, HEIGHT, self.font_normal, self.font_small)
        
        # Données du serveur (simulation)
        self.server_data = ServerData()
        self.server_data.generate_demo_data()
        
        # Ajouter quelques logs de démonstration
        self.logs_tab.add_log("Serveur initialisé", "INFO")
        self.logs_tab.add_log("En attente de démarrage...", "INFO")
    
    def switch_tab(self, tab):
        if self.active_tab != tab:
            self.active_tab = tab
            
            # Mettre à jour l'état actif des boutons d'onglets
            for button in self.tab_buttons:
                button.active = (button.tab_value == tab)
    
    def update(self):
        # Mettre à jour l'état des onglets
        mouse_pos = pygame.mouse.get_pos()
        
        # Mettre à jour les boutons d'onglets
        for button in self.tab_buttons:
            button.update(mouse_pos)

        # Mettre à jour le contenu de l'onglet actif
        if self.active_tab == Tab.DASHBOARD:
            self.dashboard_tab.update(self.server_data)
        elif self.active_tab == Tab.ROOMS:
            self.rooms_tab.update(self.server_data)
        elif self.active_tab == Tab.LOGS:
            self.logs_tab.update(self.server_data)
        elif self.active_tab == Tab.CONFIG:
            self.config_tab.update(self.server_data)

    def draw(self):
        # Effacer l'écran
        self.screen.fill(BACKGROUND_COLOR)
        
        # Dessiner les onglets
        for button in self.tab_buttons:
            button.draw(self.screen, self.font_small)
        
        # Dessiner le contenu de l'onglet actif
        if self.active_tab == Tab.DASHBOARD:
            self.dashboard_tab.draw(self.screen)
        elif self.active_tab == Tab.ROOMS:
            self.rooms_tab.draw(self.screen)
        elif self.active_tab == Tab.LOGS:
            self.logs_tab.draw(self.screen)
        elif self.active_tab == Tab.CONFIG:
            self.config_tab.draw(self.screen)
        
        # Rafraîchir l'écran
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Gestion des clics sur les onglets
                    for button in self.tab_buttons:
                        if button.handle_event(event):
                            self.switch_tab(button.tab_value)
                            break
                    
                    # Gestion des événements dans l'onglet actif
                    if self.active_tab == Tab.DASHBOARD:
                        self.dashboard_tab.handle_event(event)
                    elif self.active_tab == Tab.ROOMS:
                        self.rooms_tab.handle_event(event)
                    elif self.active_tab == Tab.LOGS:
                        self.logs_tab.handle_event(event)
                    elif self.active_tab == Tab.CONFIG:
                        self.config_tab.handle_event(event)
            
            # Mise à jour et dessin
            self.update()
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    ui = TabbedServerUI()
    ui.run()