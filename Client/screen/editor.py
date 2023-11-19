import json, socket, sys, threading, time, pygame
from entities.sprites import Tree, Flame
from classes.camera import CameraGroup
from network.client import Client
from classes.ping import FPSCounter
from classes.settings import *
from entities.player import Gobelin, Knight
from classes.imports import Graphics
from entities.houses import House
        


class Editor:
    def __init__(self):

        self.fps_counter = FPSCounter('MAIN')

        pygame.init()
        self.client = Client()
        self.players = {}
        self.trees = {}
        self.houses = {}
        self.flames = {}

        self.animations = Graphics().animations
        self.all_sprites = CameraGroup()
        self.players_sprites = pygame.sprite.Group()
        self.trees_sprites = pygame.sprite.Group()
        self.houses_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()

        self.inputs = []

        
        self.display_surface = pygame.display.get_surface()
        self.player = Gobelin((300, 300), self.animations['goblin'], [self.players_sprites, self.all_sprites])
        self.player.uuid = self.client.uuid
        self.players[self.client.uuid] = self.player


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.client.close()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('[ EVENT ] : Return pressed')
                    self.client.send('Client Pressed Return', 'TCP')
                    if not self.client.is_online():
                        self.client.start()

            if event.type == pygame.VIDEORESIZE:
                self.display_surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
                global WINDOW_WIDTH, WINDOW_HEIGHT

                WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h

                        


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



    def draw(self):
        data_tcp = self.client.receive('TCP')

        if data_tcp:
            if data_tcp['type'] == 'tree':
                for uuid, tree_data in data_tcp['data'].items():
                    if uuid not in self.trees:
                        self.trees[uuid] = Tree(tree_data['pos'], self.animations['tree'], [self.trees_sprites, self.all_sprites])
                    else:
                        self.trees[uuid].update_data(tree_data)
            
            if data_tcp['type'] == 'house':
                for uuid, house_data in data_tcp['data'].items():
                    if uuid not in self.houses:
                        match house_data['faction']:
                            case 'goblin': self.houses[uuid] = House(house_data['pos'], self.animations['goblin_house'], [self.houses_sprites, self.all_sprites], 'Goblin', self.player)
                            case 'knight': self.houses[uuid] = House(house_data['pos'], self.animations['knight_house'], [self.houses_sprites, self.all_sprites], 'Knight', self.player)
                    else:
                        self.houses[uuid].update_data(house_data)
            
            if data_tcp['type'] == 'damage':
                for uuid, damage_data in data_tcp['data'].items():
                    if uuid not in self.flames:
                        self.flames[uuid] = Flame(damage_data['pos'], self.animations['fire'], [self.damage_sprites, self.all_sprites])
                    else:
                        self.flames[uuid].update_data(damage_data)



        data = self.client.receive('UDP')

        if not data:
            return
        players = data['players']
        houses = data['houses']
        
        for uuid, player_data in players.items():
            if uuid not in self.players:
                new_player = None
                match player_data['faction']:
                    case 'goblin': new_player = Gobelin(player_data['pos'], self.animations['goblin'], [self.players_sprites, self.all_sprites])
                    case 'knight': new_player = Knight(player_data['pos'], self.animations['knight'], [self.players_sprites, self.all_sprites])
                    case _: new_player = Gobelin(player_data['pos'], self.animations['goblin'], [self.players_sprites, self.all_sprites])
                self.players[uuid] = new_player
            else:
                self.players[uuid].update_data(player_data)

        
        for uuid, house_data in houses.items():
            if uuid not in self.houses:
                match house_data['faction']:
                    case 'goblin': self.houses[uuid] = House(house_data['pos'], self.animations['goblin_house'], [self.houses_sprites, self.all_sprites], 'Goblin', self.player)
                    case 'knight': self.houses[uuid] = House(house_data['pos'], self.animations['knight_house'], [self.houses_sprites, self.all_sprites], 'Knight', self.player)
            else:
                self.houses[uuid].update_data(house_data)


        






    def update(self, dt):
        # Ping

        self.event_loop()
        self.display_surface.fill(EDITOR_BG_COLOR)

        self.get_keyboard_inputs()
        self.client.send({'inputs': self.inputs}, 'UDP')

        self.draw()
        
        self.all_sprites.update(dt)

        if self.client.uuid in  self.players:
            self.all_sprites.custom_draw(self.player.rect.center)

        self.player.lifes_bar.draw()

        self.fps_counter.ping()




