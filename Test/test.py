import pygame
import math

class AnimatedClickable:
    def __init__(self, x, y, width, height, color):
        self.original_rect = pygame.Rect(x, y, width, height)
        self.current_rect = self.original_rect.copy()
        self.color = color
        
        # États d'animation
        self.is_animating = False
        self.animation_time = 0
        self.animation_duration = 0.2  # Durée totale de l'animation en secondes
        
        # Échelles pour chaque phase
        self.scales = {
            'normal': 1.0,
            'compress': 0.8,
            'expand': 1.2
        }
        
    def update(self, dt):
        if not self.is_animating:
            return
            
        self.animation_time += dt
        progress = self.animation_time / self.animation_duration
        
        if progress >= 1.0:
            # Animation terminée
            self.is_animating = False
            current_scale = self.scales['normal']
        else:
            # Calcul de l'échelle actuelle selon la phase
            if progress < 0.2:  # Phase 1: compression rapide (20% du temps)
                t = progress / 0.2
                current_scale = self._lerp(self.scales['normal'], self.scales['compress'], t)
            elif progress < 0.5:  # Phase 2: expansion (30% du temps)
                t = (progress - 0.2) / 0.3
                current_scale = self._lerp(self.scales['compress'], self.scales['expand'], t)
            else:  # Phase 3: retour à la normale (50% du temps)
                t = (progress - 0.5) / 0.5
                current_scale = self._lerp(self.scales['expand'], self.scales['normal'], t)
        
        # Mise à jour du rectangle avec l'échelle
        new_width = self.original_rect.width * current_scale
        new_height = self.original_rect.height * current_scale
        self.current_rect.width = new_width
        self.current_rect.height = new_height
        
        # Centrage du rectangle
        self.current_rect.centerx = self.original_rect.centerx
        self.current_rect.centery = self.original_rect.centery
    
    def _lerp(self, start, end, t):
        """Interpolation linéaire entre deux valeurs"""
        return start + (end - start) * t
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.original_rect.collidepoint(event.pos):
                self.is_animating = True
                self.animation_time = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.current_rect)

# Exemple d'utilisation
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Création de plusieurs boutons animés
    buttons = [
        AnimatedClickable(100, 100, 200, 100, (255, 0, 0)),  # Rouge
        AnimatedClickable(400, 100, 200, 100, (0, 255, 0)),  # Vert
        AnimatedClickable(250, 300, 200, 100, (0, 0, 255))   # Bleu
    ]
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time en secondes
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)
        
        screen.fill((255, 255, 255))  # Fond blanc
        
        # Mise à jour et dessin des boutons
        for button in buttons:
            button.update(dt)
            button.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()