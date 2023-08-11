import pygame


class Cooldown:
    def __init__(self, duration):
        self.active = False
        self.duration = duration
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.active:
            if current_time - self.start_time >= self.duration:
                self.deactivate()
                self.active = False

