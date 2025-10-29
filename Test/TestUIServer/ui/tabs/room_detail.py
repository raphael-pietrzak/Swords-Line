import pygame
from settings import *
from ui.components import Button

class RoomDetail:
    def __init__(self, ui_context, server, room, on_back):
        self.width = ui_context.width
        self.height = ui_context.height
        self.font_normal = ui_context.font_normal
        self.font_small = ui_context.font_small
        self.font_title = ui_context.font_title
        self.server = server
        self.room = room
        self.on_back = on_back

        # Boutons de base
        self.buttons = [
            Button(pygame.Rect(50, self.height - 80, 150, 40), "Retour", self.on_back),
            Button(pygame.Rect(220, self.height - 80, 200, 40), "Message à la room", self.message_room),
            Button(pygame.Rect(440, self.height - 80, 150, 40), "Supprimer room", self.delete_room, color=ERROR_COLOR)
        ]
        # Boutons d'expulsion
        self.expel_buttons = {}
        self.update_expel_buttons()

    def update_expel_buttons(self):
        # Supprimer les boutons des joueurs qui ne sont plus là
        to_remove = [player_id for player_id in self.expel_buttons if player_id not in 
                    [p.id for p in self.room.players]]
        for player_id in to_remove:
            del self.expel_buttons[player_id]
        
        # Ajouter les boutons pour les nouveaux joueurs
        for i, player in enumerate(self.room.players):
            if player.id not in self.expel_buttons:
                y_pos = 180 + i * 40
                expel_btn = Button(
                    pygame.Rect(800, y_pos - 5, 100, 30),
                    "Expulser",
                    lambda p=player: self.expel_player(p),
                    color=WARNING_COLOR
                )
                self.expel_buttons[player.id] = expel_btn

    def message_room(self):
        self.server.broadcast_to_room(self.room.id, "CHAT_MESSAGE",
            {
                "author": "Serveur",
                "message": "Bonjour à toute la room!"
            }
        )

    def delete_room(self):
        self.server.room_manager.remove_room(self.room.id)
        self.on_back()

    def expel_player(self, player):
        if player:
            self.room.remove_player(player.id)
            print(f"Joueur {player.name} expulsé de la room {self.room.name}")

    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)
        for button in self.expel_buttons.values():
            button.update(mouse_pos)

    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return True
        for button in self.expel_buttons.values():
            if button.handle_event(event):
                return True
        return False

    def draw(self, screen):
        # Titre avec nom de la room
        title = self.font_title.render(f"Room: {self.room.name}", True, TEXT_COLOR)
        screen.blit(title, (50, 60))
        
        # Informations de base
        info_text = self.font_normal.render(f"Joueurs: {self.room.player_count}/{self.room.max_players}", True, TEXT_COLOR)
        screen.blit(info_text, (50, 100))
        
        # Mini-carte
        map_rect = pygame.Rect(50, 140, 400, 300)
        pygame.draw.rect(screen, (20, 20, 30), map_rect)
        pygame.draw.rect(screen, TEXT_COLOR, map_rect, 1)
        
        # Dessiner les joueurs sur la mini-carte
        for player in self.room.players:
            color = (255, 0, 0)  # Rouge par défaut
            if player.character_type == "warrior":
                color = (255, 0, 0)
            elif player.character_type == "mage":
                color = (0, 0, 255)
            elif player.character_type == "archer":
                color = (0, 255, 0)
            
            pygame.draw.circle(screen, color, player.position, 8)
            player_id = self.font_small.render(player.name, True, TEXT_COLOR)
            screen.blit(player_id, (player.position[0] - player_id.get_width() // 2, 
                                  player.position[1] + 10))
        
        # Liste des joueurs
        player_list_title = self.font_normal.render("Joueurs dans cette room:", True, TEXT_COLOR)
        screen.blit(player_list_title, (500, 140))
        
        for i, player in enumerate(self.room.players):
            y_pos = 180 + i * 40
            char_info = f" - {player.character_type}" if player.character_type else ""
            player_info = self.font_small.render(f"{player.name}{char_info} - Niv.{player.level}", True, TEXT_COLOR)
            screen.blit(player_info, (520, y_pos))
            
            if player.id in self.expel_buttons:
                self.expel_buttons[player.id].draw(screen, self.font_small)
        
        # Boutons d'action
        for button in self.buttons:
            button.draw(screen, self.font_small)
