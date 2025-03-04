import pygame
from client_simulation import ClientMessageSender

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

class TestUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Network Client")
        self.client = ClientMessageSender()
        self.setup_buttons()
        self.running = True

    def setup_buttons(self):
        self.buttons = [
            Button(50, 50, 200, 40, "Connect", (0, 100, 200)),
            Button(50, 100, 200, 40, "Join Server", (0, 150, 0)),
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
            self.client.set_client_id("player123")
        elif button.text == "Join Server":
            self.client.send_message("JOIN", {"name": "TestPlayer"})
        elif button.text == "Create Room":
            self.client.send_message("CREATE_ROOM", {"room_name": "TestRoom", "max_players": 4})
        elif button.text == "Join Room":
            if self.client.room_id:
                self.client.send_message("JOIN_ROOM", {"room_id": self.client.room_id})
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

            self.screen.fill((50, 50, 50))
            for button in self.buttons:
                button.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        if self.client.socket:
            self.client.disconnect()

if __name__ == "__main__":
    ui = TestUI()
    ui.run()
