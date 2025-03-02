from models.player import Player
from views.screens.login_screen import LoginScreen
from views.screens.character_screen import CharacterScreen
from views.screens.lobby_screen import LobbyScreen
from views.screens.game_screen import GameScreen

class GameController:
    def __init__(self, network_client, surface):
        self.network = network_client
        self.surface = surface
        self.player = Player()
        self.current_screen = None
        self.game_state = None
        
        self.screens = {
            'login': LoginScreen(surface, self),
            'character': CharacterScreen(surface, self),
            'lobby': LobbyScreen(surface, self),
            'game': GameScreen(surface, self)
        }
        
        self.network.set_message_handler(self.handle_network_message)
        self.switch_screen('login')

    def connect_to_server(self, player_name):
        return self.network.connect(player_name)

    def switch_screen(self, screen_name):
        if self.current_screen:
            self.current_screen.hide()
        self.current_screen = self.screens[screen_name]
        self.current_screen.show()

    def handle_network_message(self, message):
        msg_type = message.get("type")
        
        if msg_type == "CONNECTED":
            self.player.id = message.get("id")
            self.switch_screen('character')
        elif msg_type == "JOINED_ROOM":
            self.player.set_room(message.get("room_id"))
            self.switch_screen('lobby')
        elif msg_type == "GAME_STARTED":
            self.game_state = message.get("game_info")
            self.switch_screen('game')

    def update(self):
        if self.current_screen:
            self.current_screen.update()

    def draw(self):
        if self.current_screen:
            self.current_screen.draw()

    def handle_event(self, event):
        if self.current_screen:
            self.current_screen.handle_event(event)


