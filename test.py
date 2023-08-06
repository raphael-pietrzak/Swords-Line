
import pygame

class Baleine(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
    
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect(center=(100, 100))

class Elephant(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
    
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect(center=(100, 100))

class Ecureil(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
    
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect(center=(100, 100))


class Lapin(Ecureil):
    def __init__(self, group):
        super().__init__(group)
    
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect(center=(100, 100))



animaux_sprites = pygame.sprite.Group()

Baleine(animaux_sprites)
Elephant(animaux_sprites)
Ecureil(animaux_sprites)
Lapin(animaux_sprites)

print(animaux_sprites.sprites())