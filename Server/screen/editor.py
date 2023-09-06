import threading
import pygame, sys, math
from pygame import Vector2 as vector
from random import randint

from classes.settings import *

from classes.imports import Graphics
from classes.camera import CameraGroup
from menu.menu_items import MenuItemsGroup
from entities.player import Gobelin, Knight
from entities.sprites import Tree, Animated, Resource, Sprite
from entities.houses import House
from network.server import Server

from menu.menu import Sign

class Editor:
    def __init__(self, switch):
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.switch_screen = switch
        self.inputs = []
        self.inputs_2 = []

        # groups
        self.all_sprites = CameraGroup()
        self.player_sprites = pygame.sprite.Group()
        self.trees_sprites = pygame.sprite.Group()
        self.resources_sprites = pygame.sprite.Group()
        self.houses_sprites = pygame.sprite.Group()

        # animations
        self.animations = Graphics().animations

        # ressources
        self.collected_resources = {
            "log": 0,
            "gold": 0,
            "twigs": 0,
            "pinecone": 0
        }

        # map
        self.generate_map()
        self.server = Server()


        
    def generate_map(self):
        
        for i in range(100):
            Tree((randint(-900, 900), randint(-900, 900)), self.animations['tree'], [self.all_sprites, self.trees_sprites])
        
        # for i in range(100):
        #     Gobelin((randint(-900, 900), randint(-900, 900)), self.animations['goblin'], [self.all_sprites, self.player_sprites])
        self.knight_house = House((0, 0), self.animations['knight_house'], [self.all_sprites, self.houses_sprites], "Knight")
        self.goblin_house = House((300, 300), self.animations['goblin_house'], [self.all_sprites, self.houses_sprites], "Goblin")
        
        self.player2 = Gobelin(self.goblin_house.rect.center, self.animations['goblin'], [self.all_sprites, self.player_sprites])
        self.thread_init()

        Animated((200, 400), self.animations['fire'], self.all_sprites)




    def thread_init(self):
        self.player1 = Knight(self.knight_house.rect.center, self.animations['knight'], [self.all_sprites, self.player_sprites])



    # events
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.server.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.server.stop()
                    self.switch_screen("menu")
            
            self.get_keyboard_inputs_player_2()
            self.get_keyboard_inputs()

            self.get_winner()
    

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


    def get_keyboard_inputs_player_2(self):
        keys = pygame.key.get_pressed()

        self.inputs_2 = []

        if keys[pygame.K_s]:
            self.inputs_2.append("left")
        if keys[pygame.K_f]:
            self.inputs_2.append("right")
        if keys[pygame.K_e]:
            self.inputs_2.append("up")
        if keys[pygame.K_d]:
            self.inputs_2.append("down")
        if keys[pygame.K_LMETA] and not self.inputs:
            self.inputs_2.append("attack")


    def handle_collected_resources(self, sprite):
        if sprite.resource_type in self.collected_resources:
            self.collected_resources[sprite.resource_type] += 1
        sprite.pick_up()

    def regenerate_player(self, player, house):
        player.regenerate(house.healing_amount)

    def update_house_visibility(self, player, player_houses):
        for house in player_houses:
            house.is_visible = False
        for house in player_houses:
            distance = vector(player.rect.center).distance_to(vector(house.rect.center))
            if distance < house.radius:
                house.is_visible = True
                break
    

    def check_collision(self):
        for player in self.player_sprites:
            activate_cooldown = False

            collision_players = [pnj for pnj in self.player_sprites if pnj != player and player.sword_hitbox.colliderect(pnj.hitbox)]
            for sprite in collision_players:
                if player.status == 'attack' and not player.damage_cooldown.active:
                    activate_cooldown = True
                    sprite.take_damage(player.damage)
            
            collision_trees = [tree for tree in self.trees_sprites if player.sword_hitbox.colliderect(tree.hitbox)]
            for sprite in collision_trees:
                if player.status == 'attack' and not player.damage_cooldown.active:
                    activate_cooldown = True
                    sprite.burn()

            collision_houses = [house for house in self.houses_sprites if player.sword_hitbox.colliderect(house.hitbox)]
            for sprite in collision_houses:
                if player.status == 'attack' and not player.damage_cooldown.active:
                    if sprite.faction != player.faction:
                        activate_cooldown = True
                        sprite.take_damage(player.damage)

            if activate_cooldown:
                player.damage_cooldown.activate()

            collision_sprites = pygame.sprite.spritecollide(player, self.all_sprites, False, pygame.sprite.collide_mask)
            for sprite in collision_sprites:
                if sprite != player:
                    if sprite in self.resources_sprites:
                        self.handle_collected_resources(sprite)
                    if sprite in self.houses_sprites and sprite.faction == player.faction and not sprite.regeneration_cooldown.active:
                        sprite.regeneration_cooldown.activate()
                        self.regenerate_player(player, self.knight_house)

            player_houses = [house for house in self.houses_sprites if house.faction == player.faction]
            self.update_house_visibility(player, player_houses)


    def new_player(self, player_id):
        player = Gobelin((0, 0), self.animations['goblin'], [self.all_sprites, self.player_sprites])
        player.id = player_id
        return player

    def get_winner(self):
        if self.is_one_faction_remaining():
            text = "YOU WIN"
            print(text)
            self.switch_screen("menu")
    
    def is_one_faction_remaining(self):
        if len(self.houses_sprites) <= 1:
            house = self.houses_sprites.sprites()[0]
            for player in self.player_sprites:
                if player.faction != house.faction:
                    player.respawn_point = None
                    return False
            return True
        return False
    
    def get_json_game_data(self):
        # {                                        # !     FORMAT JSON
        #   "players": [
        #     { "id": 1, "faction": "knight", "position": [200, 300], "health": 100, status": "idle", direction": "right" },
        #     { "id": 2, "faction": "goblin", "position": [400, 250] , "health": 100, status": "idle", direction": "right" }
        #   ],
        # }

        server_data = {}
        server_data['players'] = []
        server_data['trees'] = []

        for player in self.player_sprites:
            server_data['players'].append(player.json_data)
        
        for tree in self.trees_sprites:
            server_data['trees'].append(tree.get_json_data())
        
        return server_data
    

    def print_clients_data(self):
        client_data = self.server.get_clients_data()
        for adress, data in client_data.items():
            print(f"{adress} : {data}")

    def update(self, dt):
        self.event_loop() 
        self.check_collision()
        self.all_sprites.update(dt)

        self.print_clients_data()
        data = self.get_json_game_data()
        clients = self.server.get_clients()
        for client in clients:
            self.server.send(data, client)
        



        self.player1.move(self.inputs)
        self.player2.move(self.inputs_2)



        # draw
        self.display_surface.fill('beige')
        self.all_sprites.custom_draw(self.player1.rect.center)




        


