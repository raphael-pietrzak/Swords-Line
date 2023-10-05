import pygame, sys
from pygame import Vector2 as vector
from random import choice, randint

from classes.settings import *
from classes.imports import Graphics
from classes.camera import CameraGroup
from entities.player import Gobelin, Knight
from entities.sprites import Tree, Animated
from entities.houses import House
from network.server import Server
from ping import FPSCounter


class Editor:
    def __init__(self, switch):

        
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.switch_screen = switch
        self.server = Server()
        self.fps_counter = FPSCounter('MAIN')

        # groups
        self.all_sprites = CameraGroup()
        self.player_sprites = pygame.sprite.Group()
        self.trees_sprites = pygame.sprite.Group()
        self.houses_sprites = pygame.sprite.Group()

        # animations
        self.animations = Graphics().animations

        # map
        self.generate_map()


        
    def generate_map(self):
        
        for i in range(100):
            Tree((randint(-900, 900), randint(-900, 900)), self.animations['tree'], [self.all_sprites, self.trees_sprites])
        
        self.knight_house = House((0, 0), self.animations['knight_house'], [self.all_sprites, self.houses_sprites], "Knight")
        self.goblin_house = House((300, 300), self.animations['goblin_house'], [self.all_sprites, self.houses_sprites], "Goblin")
        
        Animated((200, 400), self.animations['fire'], self.all_sprites)






    # events
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.server.close()
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('[ EVENT ] : Return pressed')
                    self.server.send('Server Pressed Return', 'TCP')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.server.stop()
                    self.switch_screen("menu")

            self.get_winner()



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
                    if sprite in self.houses_sprites and sprite.faction == player.faction and not sprite.regeneration_cooldown.active:
                        sprite.regeneration_cooldown.activate()
                        self.regenerate_player(player, self.knight_house)

            player_houses = [house for house in self.houses_sprites if house.faction == player.faction]
            self.update_house_visibility(player, player_houses)


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
    
    

    def handle_clients_data(self):
        clients = self.server.get_clients()
        for client_id, client in clients.items():
            if client_id not in self.clients:
                faction = choice(['knight', 'goblin'])
                match faction:
                    case 'knight': player = Knight(self.knight_house.rect.center, self.animations['knight'], [self.all_sprites, self.player_sprites])
                    case 'goblin': player = Gobelin(self.goblin_house.rect.center, self.animations['goblin'], [self.all_sprites, self.player_sprites])
                    
                self.clients[client_id] = player
            
            inputs = client.message['inputs']
            self.clients[client_id].move(inputs)
            data = self.get_json_game_data(client_id)
            self.server.send(data, client.address)



    def update(self, dt):
        self.event_loop() 

        # draw
        self.display_surface.fill('beige')
        self.send_server_data()
        self.all_sprites.update(dt)
        self.all_sprites.custom_draw((0, 0))


        self.fps_counter.ping()




    def send_server_data(self):
        clients = self.server.receive('UDP')

        message = {}

        for player in self.player_sprites:
            if player not in clients:
                self.player_sprites.remove(player)
                self.all_sprites.remove(player)

        for uuid, client in clients.items():
            player = client.player
            if player not in self.player_sprites:
                self.player_sprites.add(player)
                self.all_sprites.add(player)

            message[uuid] = {'pos' : client.player.get_position(), 'color' : client.player.color}
        
        self.server.send(message, 'UDP')

        