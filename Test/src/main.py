import pygame
from src.core.events import EventManager, Event, EventType, GameState
from src.game.player import Player, Tree
from src.ui.menu2 import Menu
from src.settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLOR_GAME_BACKGROUND, COLOR_PLAYER
from src.core.menu_events import GameMenuManager
from src.game.camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Gestionnaire d'événements
        self.event_manager = EventManager()
        
        # États du jeu
        self.state = GameState.MENU

        # Menu
        self.menu_manager = GameMenuManager(self.event_manager)
        self.menu = self.create_menu_structure(self.event_manager)
        self.menu_manager.menu_state.push_menu(self.menu)


        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.event_manager)
        self.all_sprites.add(Tree(100, 100))
        self.all_sprites.add(self.player)
        self.all_sprites.add(Player(self.event_manager))
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.camera.set_target(self.player)
        
        # Configuration des écouteurs d'événements
        self.setup_event_listeners()

    def create_menu_structure(self, event_manager):
        # Menu principal
        main_menu = Menu('main', event_manager)
        main_menu.add_button("Jouer", "play", (100, 100))
        main_menu.add_button("Options", "options", (100, 160))
        main_menu.add_button("Quitter", "quit", (100, 220))

        # Sous-menu Options
        options_menu = Menu('options', event_manager)
        options_menu.add_button("Son", "sound", (100, 100))
        options_menu.add_button("Graphiques", "graphics", (100, 160))
        options_menu.add_button("Contrôles", "controls", (100, 220))
        options_menu.add_button("Retour", "back", (100, 280))
        
        # Sous-menu Son
        sound_menu = Menu('sound', event_manager)
        sound_menu.add_button("Volume", "volume", (100, 100))
        sound_menu.add_button("Muet", "mute", (100, 160))
        sound_menu.add_button("Retour", "back", (100, 220))
        options_menu.add_submenu(sound_menu)
        
        # Sous-menu Graphiques
        graphics_menu = Menu('graphics', event_manager)
        graphics_menu.add_button("Résolution", "resolution", (100, 100))
        graphics_menu.add_button("Mode Plein écran", "fullscreen", (100, 160))
        graphics_menu.add_button("Retour", "back", (100, 220))
        options_menu.add_submenu(graphics_menu)
        
        # Sous-menu Contrôles
        controls_menu = Menu('controls', event_manager)
        controls_menu.add_button("Configurer touches", "keybinds", (100, 100))
        controls_menu.add_button("Sensibilité", "sensitivity", (100, 160))
        controls_menu.add_button("Retour", "back", (100, 220))
        options_menu.add_submenu(controls_menu)
        
        # Ajouter le sous-menu Options au menu principal
        main_menu.add_submenu(options_menu)

        return main_menu
        
    def setup_event_listeners(self):
        self.event_manager.subscribe(EventType.QUIT, lambda _: self.quit())
        self.event_manager.subscribe(EventType.STATE_CHANGE, self.handle_state_change)
        self.event_manager.subscribe(EventType.PLAYER_MOVE, self.handle_player_move)
        
    def handle_state_change(self, event: Event):
        new_state = event.data.get('new_state')
        if new_state:
            self.state = new_state
            
    def handle_player_move(self, event: Event):
        # Ici vous pouvez ajouter la logique pour gérer le mouvement du joueur
        # Par exemple, mettre à jour la caméra, vérifier les collisions, etc.
        pass
        
    def quit(self):
        self.running = False
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            # Gestion des événements Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_manager.post(Event(EventType.QUIT))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.event_manager.post(Event(EventType.STATE_CHANGE, {'new_state': GameState.MENU}))
                    
                # Gestion des événements selon l'état
                if self.state == GameState.MENU:
                    self.menu_manager.handle_event(event)
                elif self.state == GameState.PLAYING:
                    # Gérer les événements du jeu
                    pass
                    
            # Mise à jour selon l'état
            if self.state == GameState.PLAYING:
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys)
                
            # Rendu selon l'état
            if self.state == GameState.MENU:
                self.menu_manager.draw(self.screen)
            elif self.state == GameState.SETTINGS:
                self.screen.fill((0, 0, 100))
            elif self.state == GameState.PLAYING:
                self.camera.update()
                self.screen.fill((0, 100, 0)) 
                for sprite in self.all_sprites:
                    sprite.draw(self.screen, self.camera)


                
            pygame.display.flip()
            
