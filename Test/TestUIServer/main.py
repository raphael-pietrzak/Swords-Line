import pygame
import time
import random  # Pour les données de démonstration
from enum import Enum
from tabs import DashboardTab, RoomsTab, LogsTab, ConfigTab
from ui_components import TabButton
from settings import *


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