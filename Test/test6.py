import pygame
import threading
import socket
import json
import time
from collections import defaultdict

# Configuration de base
WIDTH, HEIGHT = 2000, 1500
FPS = 60
BACKGROUND_COLOR = (30, 30, 40)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (70, 70, 100)
BUTTON_HOVER_COLOR = (90, 90, 120)
BUTTON_TEXT_COLOR = (240, 240, 240)

class ServerUI:
    def __init__(self, host='localhost', port=5555):
        # Initialisation de pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Swords Line - Serveur")
        self.clock = pygame.time.Clock()
        
        # Configuration du serveur
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # {client_id: {'socket': socket, 'address': addr, 'character': character, 'position': (x, y), ...}}
        self.server_running = False
        self.server_thread = None
        
        # Statistiques du serveur
        self.stats = {
            'connected_players': 0,
            'messages_received': 0,
            'start_time': 0,
            'rooms': defaultdict(int)  # {room_id: player_count}
        }
        
        # Interface utilisateur
        self.font_title = pygame.font.SysFont('Arial', 32)
        self.font_normal = pygame.font.SysFont('Arial', 20)
        self.font_small = pygame.font.SysFont('Arial', 16)
        
        # Boutons
        self.buttons = [
            {'rect': pygame.Rect(50, 600, 200, 40), 'text': 'Démarrer Serveur', 'action': self.start_server, 'enabled': True},
            {'rect': pygame.Rect(270, 600, 200, 40), 'text': 'Arrêter Serveur', 'action': self.stop_server, 'enabled': False},
            {'rect': pygame.Rect(490, 600, 200, 40), 'text': 'Broadcast Message', 'action': self.broadcast_message, 'enabled': False},
            {'rect': pygame.Rect(710, 600, 200, 40), 'text': 'Créer Room', 'action': self.create_room, 'enabled': False}
        ]
        
        # Logs
        self.logs = []
        self.max_logs = 10
        
        # État du jeu
        self.game_state = {
            'players': {},
            'rooms': {},
            'events': []
        }
        
        # Zone de visualisation de la carte
        self.map_surface = pygame.Surface((400, 300))
        self.map_rect = pygame.Rect(50, 150, 400, 300)
        
    def add_log(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.logs.append(f"[{timestamp}] {message}")
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
    
    def start_server(self):
        if not self.server_running:
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen(5)
                self.server_running = True
                self.stats['start_time'] = time.time()
                
                # Activer/désactiver les boutons appropriés
                self.buttons[0]['enabled'] = False  # Désactiver "Démarrer"
                self.buttons[1]['enabled'] = True   # Activer "Arrêter"
                self.buttons[2]['enabled'] = True   # Activer "Broadcast"
                self.buttons[3]['enabled'] = True   # Activer "Créer Room"
                
                # Démarrer le thread du serveur
                self.server_thread = threading.Thread(target=self.run_server)
                self.server_thread.daemon = True
                self.server_thread.start()
                
                self.add_log(f"Serveur démarré sur {self.host}:{self.port}")
            except Exception as e:
                self.add_log(f"Erreur lors du démarrage du serveur: {e}")
    
    def stop_server(self):
        if self.server_running:
            self.server_running = False
            
            # Fermer toutes les connexions clients
            for client_id, client_info in self.clients.items():
                try:
                    client_info['socket'].close()
                except:
                    pass
            
            # Fermer le socket serveur
            if self.server_socket:
                self.server_socket.close()
            
            # Réinitialiser les statistiques
            self.stats['connected_players'] = 0
            self.clients = {}
            
            # Activer/désactiver les boutons appropriés
            self.buttons[0]['enabled'] = True   # Activer "Démarrer"
            self.buttons[1]['enabled'] = False  # Désactiver "Arrêter"
            self.buttons[2]['enabled'] = False  # Désactiver "Broadcast"
            self.buttons[3]['enabled'] = False  # Désactiver "Créer Room"
            
            self.add_log("Serveur arrêté")
    
    def broadcast_message(self):
        # Dans une implémentation complète, ouvrir une boîte de dialogue pour saisir le message
        message = "Annonce du serveur: Maintenance dans 5 minutes!"
        
        if self.server_running and self.clients:
            for client_id, client_info in self.clients.items():
                try:
                    # Format de message simplifié pour l'exemple
                    data = {
                        'type': 'server_message',
                        'content': message
                    }
                    client_info['socket'].send(json.dumps(data).encode())
                except:
                    pass
            
            self.add_log(f"Message diffusé: {message}")
    
    def create_room(self):
        # Dans une implémentation complète, ouvrir une boîte de dialogue pour configurer la room
        room_id = f"room_{len(self.game_state['rooms']) + 1}"
        
        self.game_state['rooms'][room_id] = {
            'id': room_id,
            'name': f"Room {len(self.game_state['rooms']) + 1}",
            'max_players': 8,
            'current_players': 0,
            'created_at': time.time()
        }
        
        self.stats['rooms'][room_id] = 0
        self.add_log(f"Nouvelle room créée: {room_id}")
    
    def run_server(self):
        self.server_socket.settimeout(0.5)
        
        while self.server_running:
            try:
                # Accepter les nouvelles connexions
                client_socket, address = self.server_socket.accept()
                
                # Générer un ID client
                client_id = f"player_{len(self.clients) + 1}"
                
                # Enregistrer le client
                self.clients[client_id] = {
                    'socket': client_socket,
                    'address': address,
                    'character': None,
                    'position': (0, 0),
                    'room': None,
                    'connected_at': time.time()
                }
                
                # Mettre à jour les statistiques
                self.stats['connected_players'] += 1
                
                # Créer un thread pour gérer ce client
                client_thread = threading.Thread(target=self.handle_client, args=(client_id,))
                client_thread.daemon = True
                client_thread.start()
                
                self.add_log(f"Nouveau client connecté: {address[0]}:{address[1]} (ID: {client_id})")
            
            except socket.timeout:
                pass
            except Exception as e:
                if self.server_running:
                    self.add_log(f"Erreur dans la boucle du serveur: {e}")
    
    def handle_client(self, client_id):
        client_socket = self.clients[client_id]['socket']
        client_socket.settimeout(0.5)
        
        # Envoyer un message de bienvenue
        welcome_msg = {
            'type': 'welcome',
            'client_id': client_id,
            'message': 'Bienvenue sur Swords Line!'
        }
        
        try:
            client_socket.send(json.dumps(welcome_msg).encode())
        except:
            pass
        
        while self.server_running and client_id in self.clients:
            try:
                # Recevoir des données du client
                data = client_socket.recv(1024)
                
                if not data:
                    # Le client s'est déconnecté
                    break
                
                # Traiter les données reçues
                message = json.loads(data.decode())
                self.stats['messages_received'] += 1
                
                # Exemples de traitement de messages
                if message['type'] == 'character_select':
                    self.clients[client_id]['character'] = message['character']
                    self.add_log(f"Joueur {client_id} a choisi le personnage: {message['character']}")
                
                elif message['type'] == 'join_room':
                    room_id = message['room_id']
                    
                    # Si la room existe et n'est pas pleine
                    if room_id in self.game_state['rooms'] and self.stats['rooms'][room_id] < self.game_state['rooms'][room_id]['max_players']:
                        # Quitter l'ancienne room si nécessaire
                        old_room = self.clients[client_id]['room']
                        if old_room and old_room in self.stats['rooms']:
                            self.stats['rooms'][old_room] -= 1
                        
                        # Rejoindre la nouvelle room
                        self.clients[client_id]['room'] = room_id
                        self.stats['rooms'][room_id] += 1
                        self.add_log(f"Joueur {client_id} a rejoint la room: {room_id}")
                
                elif message['type'] == 'move':
                    # Mettre à jour la position du joueur
                    self.clients[client_id]['position'] = (message['x'], message['y'])
                    
                    # Mise à jour de l'état du jeu pour tous les joueurs de la même room
                    room_id = self.clients[client_id]['room']
                    if room_id:
                        # Construire l'état du jeu actuel pour cette room
                        room_state = {
                            'type': 'game_state',
                            'players': {}
                        }
                        
                        # Ajouter tous les joueurs de cette room
                        for pid, pinfo in self.clients.items():
                            if pinfo['room'] == room_id:
                                room_state['players'][pid] = {
                                    'character': pinfo['character'],
                                    'position': pinfo['position']
                                }
                        
                        # Envoyer l'état à tous les joueurs de la room
                        for pid, pinfo in self.clients.items():
                            if pinfo['room'] == room_id:
                                try:
                                    pinfo['socket'].send(json.dumps(room_state).encode())
                                except:
                                    pass
            
            except socket.timeout:
                pass
            except json.JSONDecodeError:
                self.add_log(f"Erreur de décodage JSON depuis {client_id}")
            except Exception as e:
                if self.server_running and client_id in self.clients:
                    self.add_log(f"Erreur lors du traitement du client {client_id}: {e}")
                break
        
        # Nettoyage lors de la déconnexion du client
        if client_id in self.clients:
            # Mettre à jour les statistiques de la room
            room_id = self.clients[client_id]['room']
            if room_id and room_id in self.stats['rooms']:
                self.stats['rooms'][room_id] -= 1
            
            # Fermer le socket et supprimer le client
            try:
                self.clients[client_id]['socket'].close()
            except:
                pass
            
            del self.clients[client_id]
            self.stats['connected_players'] -= 1
            
            self.add_log(f"Client déconnecté: {client_id}")
    
    def render_map(self):
        # Dessiner un fond pour la carte
        self.map_surface.fill((20, 20, 30))
        
        # Dessiner les joueurs sur la carte
        for client_id, client_info in self.clients.items():
            if client_info['position']:
                x, y = client_info['position']
                # Normaliser les coordonnées pour l'affichage
                map_x = int(x * self.map_surface.get_width() / 1000)
                map_y = int(y * self.map_surface.get_height() / 1000)
                
                # Choisir une couleur basée sur le personnage
                color = (255, 0, 0)  # Rouge par défaut
                if client_info['character'] == 'warrior':
                    color = (255, 0, 0)  # Rouge pour guerrier
                elif client_info['character'] == 'mage':
                    color = (0, 0, 255)  # Bleu pour mage
                elif client_info['character'] == 'archer':
                    color = (0, 255, 0)  # Vert pour archer
                
                # Dessiner le joueur comme un cercle
                pygame.draw.circle(self.map_surface, color, (map_x, map_y), 5)
                
                # Ajouter l'ID du joueur
                text = self.font_small.render(client_id, True, TEXT_COLOR)
                self.map_surface.blit(text, (map_x - text.get_width() // 2, map_y + 6))
        
        # Afficher la map sur l'écran
        self.screen.blit(self.map_surface, self.map_rect.topleft)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.map_rect, 1)
    
    def run(self):
        running = True
        
        while running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Vérifier si un bouton a été cliqué
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button['rect'].collidepoint(mouse_pos) and button['enabled']:
                            button['action']()
            
            # Effacer l'écran
            self.screen.fill(BACKGROUND_COLOR)
            
            # Afficher le titre
            title = self.font_title.render("Swords Line - Interface Serveur", True, TEXT_COLOR)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
            
            # Afficher les statistiques du serveur
            status_text = "En ligne" if self.server_running else "Hors ligne"
            status_color = (0, 255, 0) if self.server_running else (255, 0, 0)
            
            stats_texts = [
                f"Statut: {status_text}",
                f"Joueurs connectés: {self.stats['connected_players']}",
                f"Messages reçus: {self.stats['messages_received']}",
                f"Temps d'activité: {int(time.time() - self.stats['start_time'])}s" if self.server_running else "Temps d'activité: 0s"
            ]
            
            for i, text in enumerate(stats_texts):
                rendered_text = self.font_normal.render(text, True, TEXT_COLOR if i > 0 else status_color)
                self.screen.blit(rendered_text, (50, 70 + i * 25))
            
            # Afficher la carte et les joueurs
            self.render_map()
            
            # Afficher la liste des joueurs connectés
            player_title = self.font_normal.render("Joueurs connectés:", True, TEXT_COLOR)
            self.screen.blit(player_title, (500, 150))
            
            for i, (client_id, client_info) in enumerate(self.clients.items()):
                room_info = f" - Room: {client_info['room']}" if client_info['room'] else ""
                char_info = f" - Perso: {client_info['character']}" if client_info['character'] else ""
                
                player_text = self.font_small.render(
                    f"{client_id}{char_info}{room_info}", 
                    True, 
                    TEXT_COLOR
                )
                self.screen.blit(player_text, (510, 180 + i * 20))
            
            # Afficher la liste des rooms
            room_title = self.font_normal.render("Rooms:", True, TEXT_COLOR)
            self.screen.blit(room_title, (500, 350))
            
            for i, (room_id, room_info) in enumerate(self.game_state['rooms'].items()):
                player_count = self.stats['rooms'].get(room_id, 0)
                max_players = room_info['max_players']
                
                room_text = self.font_small.render(
                    f"{room_info['name']} - Joueurs: {player_count}/{max_players}", 
                    True, 
                    TEXT_COLOR
                )
                self.screen.blit(room_text, (510, 380 + i * 20))
            
            # Afficher les logs
            log_title = self.font_normal.render("Logs du serveur:", True, TEXT_COLOR)
            self.screen.blit(log_title, (50, 470))
            
            for i, log in enumerate(self.logs):
                log_text = self.font_small.render(log, True, TEXT_COLOR)
                self.screen.blit(log_text, (50, 500 + i * 20))
            
            # Dessiner les boutons
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                # Déterminer la couleur du bouton (survol ou non)
                if button['rect'].collidepoint(mouse_pos) and button['enabled']:
                    color = BUTTON_HOVER_COLOR
                else:
                    color = BUTTON_COLOR
                
                # Griser le bouton s'il est désactivé
                if not button['enabled']:
                    color = (color[0] // 2, color[1] // 2, color[2] // 2)
                
                # Dessiner le bouton
                pygame.draw.rect(self.screen, color, button['rect'])
                pygame.draw.rect(self.screen, TEXT_COLOR, button['rect'], 1)
                
                # Texte du bouton
                button_text = self.font_normal.render(button['text'], True, BUTTON_TEXT_COLOR)
                text_x = button['rect'].x + (button['rect'].width - button_text.get_width()) // 2
                text_y = button['rect'].y + (button['rect'].height - button_text.get_height()) // 2
                self.screen.blit(button_text, (text_x, text_y))
            
            # Mettre à jour l'affichage
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Nettoyer avant de quitter
        if self.server_running:
            self.stop_server()
        
        pygame.quit()

# Pour tester l'interface serveur
if __name__ == "__main__":
    server_ui = ServerUI(host='localhost', port=5555)
    server_ui.run()