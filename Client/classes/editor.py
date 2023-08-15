import socket, json, pygame, sys, time
from classes.settings import *
from pygame import Vector2 as vector
from player.player import Player
from player.animated import Animated
from classes.imports import Imports
from classes.camera import CameraGroup
from random import randint, choice
from player.ressources import Ressource
from classes.client import Client
from classes.menu import Sign

class Editor:
    def __init__(self, switch):
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.animations = Imports().animations
        self.all_sprites = CameraGroup()
        self.player_group = pygame.sprite.Group()
        self.switch_screen = switch

        self.client = Client()
        self.server_data = {}
        self.init_data()
        self.signs = []

        self.gold_label = Sign((150, 50), (200, 70), f"Gold : 0", self.signs)


        self.players = {}
        self.inputs = []


        
    def init_data(self):
        while not self.server_data:
            self.server_data = self.client.get_server_data()
            
        self.uuid = self.server_data["uuid"]
        self.gold_sprites = pygame.sprite.Group()

        # trees
        self.trees = []
        for pos in self.server_data["trees"]:
            self.trees.append(Animated(pos, self.animations[5]['frames'], [self.all_sprites]))

        # gold
        gold = pygame.image.load('graphics/Ressources/Gold_Nugget.png').convert_alpha()
        self.gold = []
        for pos in self.server_data["gold"]:
            Ressource((pos[0], pos[1]), gold, [self.all_sprites, self.gold_sprites])


        Animated((300, 200), self.animations[1]['frames'], self.all_sprites)
        Animated((200, 400), self.animations[2]['frames'], self.all_sprites)
        flint = pygame.image.load('graphics/Ressources/Flint.png').convert_alpha()
        rocks = pygame.image.load('graphics/Ressources/Rocks.png').convert_alpha()


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\nConnexion fermée\n")
                self.client_socket.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_screen("menu")
            
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
        if keys[pygame.K_SPACE]:
            self.inputs.append("attack")
        

    def update_client(self):
        self.client.send_to_server({"inputs" : self.inputs})
        server_data = self.client.get_server_data()
        if server_data:
            self.server_data = server_data


    def update_players(self):
        self.players_data = self.server_data["players"]
        gold_collected = self.server_data["gold"]["collected"]
        if gold_collected:
            for gold in self.gold_sprites.sprites():
                if gold.pos in gold_collected:
                    gold.kill()
                    

        players_to_remove = {player_id for player_id in self.players.keys() if player_id not in self.players_data}
        
        for player_id in players_to_remove:
            player = self.players.pop(player_id)
            self.all_sprites.remove(player)
            
        for player_id, player_data in self.players_data.items():
            if player_id in self.players:
                self.players[player_id].refresh_data(player_data)
            else:
                self.add_new_player(player_id, player_data)
        
        self.player = self.players[self.uuid]
        self.player_group.add(self.player)
        self.gold_label.text = f"Gold : {self.player.gold_count}"

    



    def add_new_player(self, player_id, player_data):
        x, y = player_data['position']
        player = Player((x, y), self.animations[3]['frames'], self.all_sprites)
        self.players[player_id] = player




    def update(self, dt):
        self.event_loop() 
        self.update_client()
        self.update_players()
        self.all_sprites.update(dt)

        # draw
        self.display_surface.fill('beige')
        self.all_sprites.custom_draw(self.player.rect.center)
        self.gold_label.draw()
        


