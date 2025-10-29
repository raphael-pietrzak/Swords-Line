import pygame
from client import ClientMessageSender

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 32)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class TextInput:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.font = pygame.font.Font(None, 32)
        self.color_inactive = pygame.Color('grey')
        self.color_active = pygame.Color('white')
        self.color = self.color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return None

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width()+10)
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class StatusIndicator:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.radius = 10
        self.label = label
        self.status = False
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        color = (0, 255, 0) if self.status else (255, 0, 0)
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        text = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(text, (self.x + 20, self.y - 10))

class MessageDisplay:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.messages = []
        self.font = pygame.font.Font(None, 24)
        self.max_messages = 10

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        y_offset = 10
        for message in self.messages:
            text = self.font.render(message, True, (255, 255, 255))
            screen.blit(text, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 25

class TestUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Network Client")
        self.client = ClientMessageSender()
        self.client.message_callback = self.on_message_received
        self.setup_buttons()
        self.room_input = TextInput(260, 200, 200, 40)
        self.running = True
        
        # Ajout des indicateurs
        self.connection_status = StatusIndicator(650, 30, "Connection")
        self.room_status = StatusIndicator(650, 60, "Room")
        self.message_display = MessageDisplay(300, 300, 450, 250)
        self.client.connect()

    def on_message_received(self, message):
        if message["type"] == "CONNECTED":
            self.connection_status.status = True
            self.client.set_client_id(message["data"]["client_id"])
        elif message["type"] == "JOINED_ROOM":
            self.room_status.status = True
        elif message["type"] == "DISCONNECTED":
            self.connection_status.status = False
        elif message["type"] == "LEFT_ROOM":
            self.room_status.status = False
            
        # Afficher le message dans la zone de messages
        self.message_display.add_message(f"{message['type']}: {str(message['data'])}")

    def setup_buttons(self):
        self.buttons = [
            Button(50, 50, 200, 40, "Connect", (0, 100, 200)),
            Button(50, 100, 200, 40, "Play", (0, 150, 0)),
            Button(50, 150, 200, 40, "Create Room", (150, 0, 0)),
            Button(50, 200, 200, 40, "Join Room", (100, 100, 0)),
            Button(50, 250, 200, 40, "Move Up", (100, 0, 100)),
            Button(50, 300, 200, 40, "Move Down", (100, 0, 100)),
            Button(50, 350, 200, 40, "Move Left", (100, 0, 100)),
            Button(50, 400, 200, 40, "Move Right", (100, 0, 100))
        ]

    def handle_click(self, button):
        if button.text == "Connect":
            self.client.connect()
        elif button.text == "Play":
            self.client.send_message("PLAY1V1", {})
        elif button.text == "Create Room":
            self.client.send_message("CREATE_ROOM", {"room_name": "TestRoom", "max_players": 4})
        elif button.text == "Join Room":
            room_id = self.room_input.text
            if room_id:
                self.client.send_message("JOIN_ROOM", {"room_id": room_id})
        elif button.text == "Move Up":
            self.client.send_message("GAME_ACTION", {"action": "MOVE", "direction": "UP"})
        elif button.text == "Move Down":
            self.client.send_message("GAME_ACTION", {"action": "MOVE", "direction": "DOWN"})
        elif button.text == "Move Left":
            self.client.send_message("GAME_ACTION", {"action": "MOVE", "direction": "LEFT"})
        elif button.text == "Move Right":
            self.client.send_message("GAME_ACTION", {"action": "MOVE", "direction": "RIGHT"})

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event.pos):
                            self.handle_click(button)
                self.room_input.handle_event(event)

            self.screen.fill((50, 50, 50))
            for button in self.buttons:
                button.draw(self.screen)
            self.room_input.draw(self.screen)
            
            # Dessiner les indicateurs et la zone de messages
            self.connection_status.draw(self.screen)
            self.room_status.draw(self.screen)
            self.message_display.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()
        if self.client.socket:
            self.client.disconnect()

if __name__ == "__main__":
    ui = TestUI()
    ui.run()