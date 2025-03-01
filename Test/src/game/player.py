from abc import abstractmethod
import pygame
from src.core.events import EventManager, Event, EventType
from src.settings import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

    @abstractmethod
    def draw(self, surface, camera):
        pass

class Player(Sprite):
    def __init__(self, event_manager: EventManager):
        super().__init__()
        self.event_manager = event_manager
        self.rect = pygame.Rect(400, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = PLAYER_SPEED
        
    def handle_input(self, keys):
        movement = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]: movement.x = -1
        elif keys[pygame.K_RIGHT]: movement.x = 1
        if keys[pygame.K_UP]: movement.y = -1
        elif keys[pygame.K_DOWN]: movement.y = 1
            
        if movement.length() > 0:
            movement.normalize_ip()
            self.rect.x += movement.x * self.speed
            self.rect.y += movement.y * self.speed
            self.event_manager.post(Event(
                EventType.PLAYER_MOVE,
                {'position': (self.rect.x, self.rect.y)}
            ))

    def draw(self, surface, camera):
        pygame.draw.rect(surface, (0, 255, 0), camera.apply(self))

class Tree(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 32, 32)

    def draw(self, surface, camera):
        pygame.draw.rect(surface, (0, 128, 0), camera.apply(self))