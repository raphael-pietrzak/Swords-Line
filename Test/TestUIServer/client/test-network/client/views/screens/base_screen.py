import pygame

class BaseScreen:
    def __init__(self, surface, controller):
        self.surface = surface
        self.controller = controller
        self.active = False
        self.ui_elements = {}

    def show(self):
        self.active = True

    def hide(self):
        self.active = False

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass
