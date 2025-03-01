import pygame
import os
from typing import Dict, Tuple
from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Camera: 
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.target = None
        self.bounds = None
        
    def set_bounds(self, left: int, top: int, right: int, bottom: int):
        """Définit les limites de déplacement de la caméra"""
        self.bounds = pygame.Rect(left, top, right - left, bottom - top)

    def set_target(self, target: 'AnimatedSprite'):
        """Définit l'objet que la caméra doit suivre"""
        self.target = target
        print(self.target.rect)
        
    def update(self):
        if self.target:
            # Calcul de la position désirée
            wanted_x = self.target.rect.centerx - self.width // 2
            wanted_y = self.target.rect.centery - self.height // 2
            
            # Application des limites si définies
            if self.bounds:
                wanted_x = max(self.bounds.left, min(wanted_x, self.bounds.right - self.width))
                wanted_y = max(self.bounds.top, min(wanted_y, self.bounds.bottom - self.height))
                
            self.x = wanted_x
            self.y = wanted_y

    def apply(self, entity: pygame.sprite.Sprite) -> pygame.Rect:
        """Applique le décalage de la caméra à une entité"""
        return pygame.Rect(
            entity.rect.x - self.x,
            entity.rect.y - self.y,
            entity.rect.width,
            entity.rect.height
        )

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, sprite_sheet_path: str, sprite_size: Tuple[int, int]):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprite_width, self.sprite_height = sprite_size
        
        # Dictionnaire des animations
        self.animations: Dict[str, list] = {}
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, sprite_size[0], sprite_size[1])
        self.image = pygame.Surface(sprite_size, pygame.SRCALPHA)
        
        # Direction et mouvement
        self.direction = Direction.DOWN
        self.speed = 5
        self.moving = False

    def load_animation(self, name: str, start_row: int, frames_count: int):
        """Charge une animation depuis la sprite sheet"""
        animation_frames = []
        for i in range(frames_count):
            frame = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
            frame.blit(
                self.sprite_sheet,
                (0, 0),
                (i * self.sprite_width,
                 start_row * self.sprite_height,
                 self.sprite_width,
                 self.sprite_height)
            )
            animation_frames.append(frame)
        self.animations[name] = animation_frames

    def set_animation(self, name: str):
        """Change l'animation courante"""
        if name != self.current_animation and name in self.animations:
            self.current_animation = name
            self.current_frame = 0
            self.animation_timer = 0

    def update(self, dt: float):
        """Met à jour l'animation et la position"""
        # Mise à jour de l'animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_frame]

        # Mise à jour de la position
        if self.moving:
            if self.direction == Direction.RIGHT:
                self.position.x += self.speed
            elif self.direction == Direction.LEFT:
                self.position.x -= self.speed
            elif self.direction == Direction.UP:
                self.position.y -= self.speed
            elif self.direction == Direction.DOWN:
                self.position.y += self.speed

        # Mise à jour du rectangle de collision
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

class Player(AnimatedSprite):
    def __init__(self, x: int, y: int):
        # super().__init__(x, y, "player_spritesheet.png", (32, 48))
        
        # # Chargement des animations
        # self.load_animation("idle_down", 0, 3)
        # self.load_animation("idle_left", 1, 3)
        # self.load_animation("idle_right", 2, 3)
        # self.load_animation("idle_up", 3, 3)
        # self.load_animation("walk_down", 4, 4)
        # self.load_animation("walk_left", 5, 4)
        # self.load_animation("walk_right", 6, 4)
        # self.load_animation("walk_up", 7, 4)
        
        # self.set_animation("idle_down")
        pass

    def handle_input(self, keys):
        """Gère les entrées clavier"""
        self.moving = False
        
        if keys[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT
            self.moving = True
            self.set_animation("walk_right")
        elif keys[pygame.K_LEFT]:
            self.direction = Direction.LEFT
            self.moving = True
            self.set_animation("walk_left")
        elif keys[pygame.K_UP]:
            self.direction = Direction.UP
            self.moving = True
            self.set_animation("walk_up")
        elif keys[pygame.K_DOWN]:
            self.direction = Direction.DOWN
            self.moving = True
            self.set_animation("walk_down")
        else:
            # Animation idle selon la dernière direction
            if self.direction == Direction.RIGHT:
                self.set_animation("idle_right")
            elif self.direction == Direction.LEFT:
                self.set_animation("idle_left")
            elif self.direction == Direction.UP:
                self.set_animation("idle_up")
            else:
                self.set_animation("idle_down")
    
