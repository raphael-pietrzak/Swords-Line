import pygame
from settings import *
from ui.components import Button
from ui.tabs.room_detail import RoomDetail

class RoomsTab:
    def __init__(self, ui_context, server):
        self.width = ui_context.width
        self.height = ui_context.height
        self.font_normal = ui_context.font_normal
        self.font_small = ui_context.font_small
        self.font_title = ui_context.font_title

        # Données du serveur
        self.server = server
        self.room_manager = server.room_manager

        # Boutons spécifiques à cet onglet
        self.buttons = [
            Button(pygame.Rect(self.width - 250, 60, 200, 40), "Nouvelle Room", self.create_room)
        ]
        
        # État interne
        self.rooms = self.room_manager.rooms
        self.selected_room = None
        self.viewing_room_details = False
        
        # Boutons dynamiques pour les rooms (initialisés dans update)
        self.room_buttons = []
        
        self.ui_context = ui_context
        self.room_detail = None
    
    def create_room(self):
        self.room_manager.create_room()
    
    def view_room(self, room):
        self.selected_room = room
        self.viewing_room_details = True
        self.room_detail = RoomDetail(self.ui_context, self.server, room, self.back_to_rooms)
        print(f"Affichage des détails de la room: {room.name}")
    
    def back_to_rooms(self):
        self.viewing_room_details = False
        self.selected_room = None
        self.room_detail = None
    
    def update(self):
        self.rooms = self.room_manager.rooms
        
        if self.viewing_room_details:
            self.room_detail.update(pygame.mouse.get_pos())
        else:
            for button in self.buttons:
                button.update(pygame.mouse.get_pos())
            
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
                    lambda r=room: self.room_manager.remove_room(r.id),
                    color=ERROR_COLOR
                )
                
                self.room_buttons.append(view_btn)
                self.room_buttons.append(delete_btn)
                
                view_btn.update(pygame.mouse.get_pos())
                delete_btn.update(pygame.mouse.get_pos())
    
    def handle_event(self, event):
        if self.viewing_room_details:
            return self.room_detail.handle_event(event)
            
        for button in self.buttons:
            if button.handle_event(event):
                return True
        
        for button in self.room_buttons:
            if button.handle_event(event):
                return True
        
        return False
    
    def draw(self, screen):
        if self.viewing_room_details and self.selected_room:
            self.room_detail.draw(screen)
        else:
            self.draw_rooms_list(screen)
    
    def draw_rooms_list(self, screen):
        title = self.font_normal.render("Gestion des Rooms", True, TEXT_COLOR)
        screen.blit(title, (20, 60))
        
        for button in self.buttons:
            button.draw(screen, self.font_small)
        
        headers = ["Room ID", "Room", "Joueurs", "Actions"]
        header_widths = [100, 300, 150, 300]
        header_x = 50
        
        for i, header in enumerate(headers):
            header_text = self.font_normal.render(header, True, TEXT_COLOR)
            screen.blit(header_text, (header_x, 100))
            header_x += header_widths[i]
        
        pygame.draw.line(screen, TEXT_COLOR, (50, 125), (self.width - 50, 125), 1)
        
        if not self.rooms:
            no_rooms = self.font_normal.render("Aucune room active", True, TEXT_COLOR)
            screen.blit(no_rooms, (self.width // 2 - no_rooms.get_width() // 2, 200))
        else:
            for i, (room_id, room) in enumerate(self.rooms.items()):
                y_pos = 120 + i * 60
                
                room_id_text = self.font_normal.render(str(room_id), True, TEXT_COLOR)
                screen.blit(room_id_text, (50, y_pos + 20))
                
                room_name = self.font_normal.render(room.name, True, TEXT_COLOR)
                screen.blit(room_name, (150, y_pos + 20))
                
                player_count = self.font_normal.render(f"{room.player_count}/{room.max_players}", True, TEXT_COLOR)
                screen.blit(player_count, (450, y_pos + 20))
                
                self.room_buttons[i*2].draw(screen, self.font_small)
                self.room_buttons[i*2+1].draw(screen, self.font_small)
                
                pygame.draw.line(screen, TEXT_COLOR, (50, y_pos + 60), (self.width - 50, y_pos + 60), 1)