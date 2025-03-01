import pygame
from settings import *
from ui_components import Button
class RoomsTab:
    def __init__(self, ui_context, server_data):
        self.width = ui_context.width
        self.height = ui_context.height
        self.font_normal = ui_context.font_normal
        self.font_small = ui_context.font_small
        self.font_title = ui_context.font_title

        # Données du serveur
        self.server_data = server_data
        
        # Boutons spécifiques à cet onglet
        self.buttons = [
            Button(pygame.Rect(self.width - 250, 60, 200, 40), "Nouvelle Room", self.create_room)
        ]
        
        # État interne
        self.rooms = {}  # Référence aux rooms du serveur
        self.selected_room = None
        self.viewing_room_details = False
        
        # Boutons dynamiques pour les rooms (initialisés dans update)
        self.room_buttons = []
        
        # Boutons pour la vue détaillée
        self.detail_buttons = [
            Button(pygame.Rect(50, self.height - 80, 150, 40), "Retour", self.back_to_rooms),
            Button(pygame.Rect(220, self.height - 80, 200, 40), "Message à la room", self.message_room),
            Button(pygame.Rect(440, self.height - 80, 150, 40), "Supprimer room", self.delete_room, color=ERROR_COLOR)
        ]
    
    def create_room(self):
        self.server_data.create_room()
    
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
    
    def update(self):
        self.rooms = self.server_data.rooms
        
        # Mettre à jour l'état des boutons
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
        
        # Si on est dans la vue détaillée, mettre à jour ces boutons également
        if self.viewing_room_details:
            for button in self.detail_buttons:
                button.update(pygame.mouse.get_pos())
        
        # Créer les boutons dynamiques pour chaque room
        self.room_buttons = []
        for i, (room_id, room) in enumerate(self.rooms.items()):
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
        headers = ["Room ID", "Room", "Joueurs", "Actions"]
        header_widths = [100, 300, 150, 300]
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
            for i, (room_id, room) in enumerate(self.rooms.items()):
                y_pos = 120 + i * 60
                
                # ID de la room
                room_id_text = self.font_normal.render(str(room_id), True, TEXT_COLOR)
                screen.blit(room_id_text, (50, y_pos + 20))
                
                # Nom de la room
                room_name = self.font_normal.render(room.name, True, TEXT_COLOR)
                screen.blit(room_name, (150, y_pos + 20))
                
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