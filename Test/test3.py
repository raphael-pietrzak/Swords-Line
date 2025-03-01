import pygame
import sys

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
        
        # Configuration du menu
        self.pages = [
            {"name": "Menu Principal", "color": (255, 0, 0)},
            {"name": "Options", "color": (0, 255, 0)},
            {"name": "Credits", "color": (0, 0, 255)}
        ]
        self.current_page = 0
        self.dragging = False
        self.drag_start_x = 0
        self.offset = 0
        self.transition_speed = 15
        
        # Configuration de la navbar
        self.navbar_height = 50
        self.nav_button_width = screen_width // len(self.pages)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Vérifier si le clic est dans la navbar
                if y > self.screen_height - self.navbar_height:
                    clicked_page = x // self.nav_button_width
                    if 0 <= clicked_page < len(self.pages):
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
                        elif self.offset < 0 and self.current_page < len(self.pages) - 1:
                            self.current_page += 1
                    self.offset = 0
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    x, _ = event.pos
                    self.offset = x - self.drag_start_x
                    # Limiter le drag
                    max_offset = self.screen_width / 2
                    self.offset = max(min(self.offset, max_offset), -max_offset)
        
        return True
    
    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Dessiner les pages
        for i, page in enumerate(self.pages):
            x = i * self.screen_width - (self.current_page * self.screen_width) + self.offset
            pygame.draw.rect(self.screen, page["color"], 
                           (x, 0, self.screen_width, self.screen_height - self.navbar_height))
            
            # Afficher le nom de la page
            font = pygame.font.Font(None, 36)
            text = font.render(page["name"], True, self.WHITE)
            text_rect = text.get_rect(center=(x + self.screen_width/2, self.screen_height/2))
            self.screen.blit(text, text_rect)
        
        # Dessiner la navbar
        pygame.draw.rect(self.screen, self.GRAY, 
                        (0, self.screen_height - self.navbar_height, 
                         self.screen_width, self.navbar_height))
        
        # Dessiner les boutons de navigation
        for i in range(len(self.pages)):
            button_x = i * self.nav_button_width
            button_color = self.BLUE if i == self.current_page else self.WHITE
            pygame.draw.rect(self.screen, button_color,
                           (button_x + 5, self.screen_height - self.navbar_height + 5,
                            self.nav_button_width - 10, self.navbar_height - 10))
            
            # Afficher le nom du menu dans le bouton
            font = pygame.font.Font(None, 24)
            text = font.render(self.pages[i]["name"], True, self.BLACK)
            text_rect = text.get_rect(center=(button_x + self.nav_button_width/2,
                                            self.screen_height - self.navbar_height/2))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.draw()
            clock.tick(60)
        
        pygame.quit()

# Exemple d'utilisation
if __name__ == "__main__":
    slider = MenuSlider(800, 600)
    slider.run()