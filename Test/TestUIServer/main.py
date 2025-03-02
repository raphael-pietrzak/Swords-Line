import pygame
import time
import random  # Pour les données de démonstration
from enum import Enum
from tabs import DashboardTab, RoomsTab, LogsTab, ConfigTab
from ui_components import TabButton, UIContext
from settings import *
from models import ServerData

class TabbedServerUI:
    def __init__(self):
        # Initialisation de pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ui_context = UIContext(WIDTH, HEIGHT)
        pygame.display.set_caption("Swords Line - Serveur")
        self.clock = pygame.time.Clock()
        self.running = True
        
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


        # Données du serveur (simulation)
        self.server_data = ServerData()
        self.server_data.generate_demo_data()
        
        # Onglet actif
        self.active_tab = Tab.DASHBOARD

        
        # Contenu des onglets
        self.dashboard_tab = DashboardTab(self.ui_context, self.server_data)
        self.rooms_tab = RoomsTab(self.ui_context, self.server_data)
        self.logs_tab = LogsTab(self.ui_context, self.server_data)
        self.config_tab = ConfigTab(self.ui_context, self.server_data)
        

        
        # Ajouter quelques logs de démonstration
        self.server_data.add_log("Serveur initialisé", "INFO")
        self.server_data.add_log("En attente de démarrage...", "INFO")
    
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
            self.dashboard_tab.update()
        elif self.active_tab == Tab.ROOMS:
            self.rooms_tab.update()
        elif self.active_tab == Tab.LOGS:
            self.logs_tab.update()
        elif self.active_tab == Tab.CONFIG:
            self.config_tab.update()

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

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
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

    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            
            for event in pygame.event.get():
                self.handle_event(event)
            
            # Mise à jour et dessin
            self.update()
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    ui = TabbedServerUI()
    ui.run()