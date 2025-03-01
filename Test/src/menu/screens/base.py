
import pygame
from abc import ABC, abstractmethod

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))

    @abstractmethod
    def update(self, dt):
        pass
        
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

