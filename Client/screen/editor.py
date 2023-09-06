import sys, pygame
import threading
import time
from network.client import Client
from classes.camera import CameraGroup
from entities.player import Player, Gobelin, Knight
from entities.houses import House
from entities.sprites import Tree
from classes.settings import *
from classes.imports import Graphics

class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.lock = threading.Lock()
        self.client = Client()
        self.clients = {}

        self.player_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.house_sprites = pygame.sprite.Group()

        self.player_dict = {}
        self.tree_dict = {}

        self.all_sprites = CameraGroup()

        self.graphics = Graphics().animations


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        self.get_keyboard_inputs()

    
    def get_keyboard_inputs(self):
        keys = pygame.key.get_pressed()

        self.inputs = []

        if keys[pygame.K_LEFT]:
            self.inputs.append("left")
        if keys[pygame.K_RIGHT]:
            self.inputs.append("right")
        if keys[pygame.K_UP]:
            self.inputs.append("up")
        if keys[pygame.K_DOWN]:
            self.inputs.append("down")
        if keys[pygame.K_RMETA] and not self.inputs:
            self.inputs.append("attack")
        

      

    def update(self, dt):
        self.event_loop()
        self.client.send(self.inputs)
        self.all_sprites.update(dt)

        self.display_surface.fill('aquamarine3')
        self.all_sprites.custom_draw((0, 0))
