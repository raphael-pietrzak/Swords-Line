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

        self.client = Client()

        self.players = {}
        self.trees = {}
        self.houses = {}

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
        
    def handle_communication(self):
        self.client.send({'inputs': self.inputs, 'id': str(self.client.id)})
        data = self.client.get_server_data()
        trees = data['trees']
        players = data['players']
        houses = data['houses']
        self.id = data['id']
        self.faction = data['players'][self.id]['faction']

        for tree in trees:
            if tree['id'] in self.trees:
                self.trees[tree['id']].update_data(tree)
            else:
                self.trees[tree['id']] = Tree(tree['position'], self.graphics['tree'], self.all_sprites)
                self.trees[tree['id']].update_data(tree)

        for player in players:
            if player['id'] in self.players:
                self.players[player['id']].update_data(player)
            else:
                graphics = self.graphics['goblin']
                match player['faction']:
                    case 'Goblin': graphics = self.graphics['goblin']
                    case 'Knight': graphics = self.graphics['knight']
                        
                self.players[player['id']] = Player(player['position'], graphics, self.all_sprites)
                self.players[player['id']].update_data(player)


            
        for house in houses:
            if house['id'] in self.houses:
                self.houses[house['id']].update_data(house)
            else:
                graphics = self.graphics['goblin_house']
                match house['faction']:
                    case 'Goblin': graphics = self.graphics['goblin_house']
                    case 'Knight': graphics = self.graphics['knight_house']
                self.houses[house['id']] = House(house['position'], graphics, self.all_sprites, house['faction'])
                self.houses[house['id']].update_data(house)
            
    def update(self, dt):
        self.event_loop()
        self.all_sprites.update(dt)
        
        self.display_surface.fill('aquamarine3')
        self.handle_communication()

        self.all_sprites.custom_draw(self.players[self.id].rect.center)
