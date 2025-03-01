import pygame
from src.menu.ui.animation import AnimationMixin
from src.menu.screens.base import Screen


class Card(AnimationMixin):
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.init_animation()
        self.is_expanded = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_animating = True
                self.animation_time = 0
                return True
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Button(AnimationMixin):
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.init_animation()
        self.visible = False
        
    def handle_event(self, event):
        if not self.visible:  # Empêche le clic quand invisible
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_animating = True
                self.animation_time = 0
                return True
        return False
    
    def draw(self, screen):
        if not self.visible:
            return
        
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Container:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.min_height = height * 0.6  # Hauteur minimale (juste la carte)
        self.max_height = height  # Hauteur maximale (avec boutons)
        self.current_height = self.min_height
        self.width = width
        self.rect = pygame.Rect(x, y, width, self.current_height)
        self.color = (100, 100, 100)
        self.is_animating = False
        self.animation_time = 0
        self.animation_duration = 0.4
        
        # Création de la carte
        card_width = width * 0.8
        card_height = self.min_height * 0.7
        card_x = x + (width - card_width) / 2
        card_y = y + self.min_height * 0.15
        self.card = Card(card_x, card_y, card_width, card_height, (200, 200, 200))
        
        # Création des boutons
        button_width = width * 0.7
        button_height = height * 0.15
        button_x = x + (width - button_width) / 2
        
        button1_y = y + height * 0.6
        button2_y = y + height * 0.8
        
        self.buttons = [
            Button(button_x, button1_y, button_width, button_height, (150, 150, 255), "Button 1"),
            Button(button_x, button2_y, button_width, button_height, (150, 255, 150), "Button 2")
        ]
    
    def update(self, dt):
        print("test")
        self.card.update_animation(dt)
        
        if self.is_animating:
            self.animation_time += dt
            progress = min(1.0, self.animation_time / self.animation_duration)
            
            if self.card.is_expanded:
                self.current_height = self.max_height
            else:
                self.current_height = self.min_height
            
            self.rect.height = self.current_height
            
            # Mise à jour de la visibilité des boutons
            for button in self.buttons:
                button.visible = self.card.is_expanded
            
            if progress >= 1.0:
                self.is_animating = False
        
        for button in self.buttons:
            button.update_animation(dt)
    
    def _lerp(self, start, end, t):
        return start + (end - start) * t
    
    def handle_event(self, event):
        if self.card.handle_event(event):
            self.card.is_expanded = not self.card.is_expanded
            self.is_animating = True
            self.animation_time = 0
            # Mise à jour immédiate de la hauteur
            self.current_height = self.max_height if self.card.is_expanded else self.min_height
            self.rect.height = self.current_height
            
        for button in self.buttons:
            button.handle_event(event)
    
    def draw(self, screen):
        # Dessiner le container
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Dessiner la carte
        self.card.draw(screen)
        
        # Dessiner les boutons
        for button in self.buttons:
            button.draw(screen)

class CardGrid:
    def __init__(self, x, y, cols, rows, container_width, container_height, padding=20):
        self.containers = []
        self.selected_container = None
        
        for row in range(rows):
            for col in range(cols):
                container_x = x + (container_width + padding) * col
                container_y = y + (container_height + padding) * row
                container = Container(container_x, container_y, container_width, container_height)
                self.containers.append(container)
    
    def handle_event(self, event):
        for container in self.containers:
            if container.handle_event(event):
                # Si un container est déjà sélectionné et c'est un autre
                if self.selected_container and self.selected_container != container:
                    self.selected_container.card.is_expanded = False
                    self.selected_container.is_animating = True
                    self.selected_container.animation_time = 0
                    self.selected_container.current_height = self.selected_container.min_height
                    self.selected_container.rect.height = self.selected_container.current_height
                
                self.selected_container = container if container.card.is_expanded else None
                break
    
    def update(self, dt):
        for container in self.containers:
            container.update(dt)
    
    def draw(self, screen):
        for container in self.containers:
            container.draw(screen)

class CollectionMenu(Screen):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.grid = CardGrid(
            x=50, 
            y=50, 
            cols=3, 
            rows=3, 
            container_width=200, 
            container_height=150
        )
        self.name = "Collection"
    
    def handle_event(self, event):
        self.grid.handle_event(event)

    def update(self, dt):
        self.grid.update(dt)

    def draw(self):
        self.grid.draw(self.surface)
        return self.surface

