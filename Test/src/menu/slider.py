
import pygame
from src.menu.screens import MainMenu, OptionsMenu
from src.menu.screens.collection.main import CollectionMenu

class MenuSlider:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
        # Couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.BLUE = (0, 0, 255)
        
        # Initialisation des écrans
        self.screens = [
            MainMenu(screen_width, screen_height - 50),  # -50 pour la navbar
            OptionsMenu(screen_width, screen_height - 50),
            CollectionMenu(screen_width, screen_height - 50)
        ]
        
        self.current_page = 0
        self.dragging = False
        self.drag_start_x = 0
        self.offset = 0
        
        # Configuration de la navbar
        self.navbar_height = 50
        self.nav_button_width = screen_width // len(self.screens)
        
    def handle_events(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Vérifier si le clic est dans la navbar
                if y > self.screen_height - self.navbar_height:
                    clicked_page = x // self.nav_button_width
                    if 0 <= clicked_page < len(self.screens):
                        self.current_page = clicked_page
                        self.offset = 0
                else:
                    # Commencer le drag
                    self.dragging = True
                    self.drag_start_x = x
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.dragging = False
                    # Déterminer la direction du swipe
                    if abs(self.offset) > self.screen_width / 4:
                        if self.offset > 0 and self.current_page > 0:
                            self.current_page -= 1
                        elif self.offset < 0 and self.current_page < len(self.screens) - 1:
                            self.current_page += 1
                    self.offset = 0
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    x, _ = event.pos
                    self.offset = x - self.drag_start_x
                    # Limiter le drag
                    max_offset = self.screen_width / 2
                    self.offset = max(min(self.offset, max_offset), -max_offset)
            
            # Propager l'événement à l'écran actuel
            self.screens[self.current_page].handle_event(event)
        self.screens[self.current_page].update(dt)
        return True
    
    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Dessiner les écrans
        for i, screen in enumerate(self.screens):
            x = i * self.screen_width - (self.current_page * self.screen_width) + self.offset
            # Dessiner l'écran actuel
            surface = screen.draw()
            self.screen.blit(surface, (x, 0))
        
        # Dessiner la navbar
        pygame.draw.rect(self.screen, self.GRAY, 
                        (0, self.screen_height - self.navbar_height, 
                         self.screen_width, self.navbar_height))
        
        # Dessiner les boutons de navigation
        for i, screen in enumerate(self.screens):
            button_x = i * self.nav_button_width
            button_color = self.BLUE if i == self.current_page else self.WHITE
            pygame.draw.rect(self.screen, button_color,
                           (button_x + 5, self.screen_height - self.navbar_height + 5,
                            self.nav_button_width - 10, self.navbar_height - 10))
            
            # Afficher le nom du menu dans le bouton
            font = pygame.font.Font(None, 24)
            text = font.render(screen.name, True, self.BLACK)
            text_rect = text.get_rect(center=(button_x + self.nav_button_width/2,
                                            self.screen_height - self.navbar_height/2))
            self.screen.blit(text, text_rect)

        
        pygame.display.flip()
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000
            running = self.handle_events(dt)
            self.draw()
            clock.tick(60)
        
        pygame.quit()

