import time
import pygame, sys
from pygame import Vector2 as vector
from random import choice, randint

from classes.settings import *
from classes.imports import Graphics
from classes.camera import CameraGroup
from entities.player import Goblin, Knight
from entities.sprites import Block, Tree, Animated
from entities.houses import House
from network.server import Server
from classes.ping import FPSCounter
from menu.online_indicator import OnlineIndicator

class Editor:
    def __init__(self, switch):
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.switch_screen = switch
        self.fps_counter = FPSCounter('MAIN')

        # groups
        self.all_sprites = CameraGroup()
        self.player_sprites = CameraGroup()
        self.trees_sprites = pygame.sprite.Group()
        self.houses_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.players = {}

        # animations
        self.animations = Graphics().animations

        # map
        self.generate_map()

        # server
        self.server = Server()



    # imports
    def generate_map(self):
        
        for _ in range(100):
            Tree((randint(-900, 900), randint(-900, 900)), self.animations['tree'], self.animations['tree_fire'], [self.all_sprites, self.trees_sprites], self.collision_sprites)
        
        self.knight_house = House((300, 300), self.animations['knight_house'], [self.all_sprites, self.houses_sprites], "knight")
        self.goblin_house = House((20, 20), self.animations['goblin_house'], [self.all_sprites, self.houses_sprites], "goblin")
        
        Animated((200, 400), self.animations['fire'], self.all_sprites)


        self.offline_players = [
            Goblin((300, 300), self.animations['goblin'], [self.all_sprites, self.player_sprites], self.goblin_house, self.collision_sprites),
            Knight((200, 200), self.animations['knight'], [self.all_sprites, self.player_sprites], self.knight_house, self.collision_sprites)]
        self.offline_player_index = 0
        self.player = self.offline_players[self.offline_player_index]



    # events
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.server.close()
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.server.online:
                    print('[ EVENT ] : Return pressed')
                    self.server.send('Server Pressed Return', 'TCP')

                if event.key == pygame.K_ESCAPE:
                    self.server.close()
                    self.switch_screen("menu")

                if event.key == pygame.K_h:
                    self.all_sprites.hitbox_active = not self.all_sprites.hitbox_active

                if event.key == pygame.K_v:
                    for house in self.houses_sprites:
                        house.is_visible = not house.is_visible
            
                if event.key == pygame.K_o:
                    self.server.toggle()

                if event.key == pygame.K_s:
                    self.offline_player_index += 1
                    if self.offline_player_index >= len(self.offline_players):
                        self.offline_player_index = 0
                    self.player = self.offline_players[self.offline_player_index]

    
    def update_players_from_keyboard(self):
        keys = pygame.key.get_pressed()
        inputs = []

        if keys[pygame.K_UP]:
            inputs.append('up')
        if keys[pygame.K_DOWN]:
            inputs.append('down')
        if keys[pygame.K_LEFT]:
            inputs.append('left')
        if keys[pygame.K_RIGHT]:
            inputs.append('right')
        if keys[pygame.K_RMETA]:
            inputs.append('attack')

        for player in self.offline_players:
            if player == self.player:
                self.player.inputs = inputs
            else:
                player.inputs = []


    # def update_house_visibility(self, player):
    #     for house in self.houses_sprites:
    #         distance = vector(player.rect.center).distance_to(vector(house.rect.center))
    #         if distance < house.radius:
    #             house.is_visible = True
    #             break
    

    # server events
    def update_players_from_server(self):
        # Utilisation conseillée :
        new_players = self.server.get_new_clients()
        if new_players:
            print(f'[ NEW PLAYER ] : {uuid}')
            for uuid in new_players:
                player = self.generate_player()
                self.players[uuid] = player
            

        del_players = self.server.get_del_clients()
        if del_players:
            print(f'[ DEL PLAYER ] : {del_players}')
            for uuid in del_players:
                player = self.players.get(uuid)
                if not player: break
                self.player_sprites.remove(player)
                self.all_sprites.remove(player)
                del self.players[uuid]

        clients_data = self.server.receive('UDP')
        for uuid, data in clients_data.items():
            player = self.players.get(uuid)
            if not player: continue
            player.inputs = data['inputs']
        
    
    def send_player_data(self):
        message = {uuid: {'color': player.color, 'pos': player.get_position()} for uuid, player in self.players.items()}
        self.server.send(message, 'UDP')
    

    def generate_player(self):
        faction = choice(['knight', 'goblin'])

        match faction:
            case 'knight': player = Knight(
                pos = self.knight_house.rect.center, 
                frames = self.animations['knight'], 
                group = [self.all_sprites, self.player_sprites], 
                house = self.knight_house,
                collision_sprites = self.collision_sprites)

            case 'goblin': player = Goblin(
                pos = self.goblin_house.rect.center, 
                frames = self.animations['goblin'], 
                group = [self.all_sprites, self.player_sprites], 
                house = self.goblin_house,
                collision_sprites = self.collision_sprites)

        return player


    # collisions
    def collide_check(self):
        players_attacking = [player for player in self.player_sprites if player.is_attacking and not player.hit_success and int(player.frame_index) == 4]

        # sword collide
        for player in players_attacking:

            trees_attacked = [tree for tree in self.trees_sprites if tree.hitbox.colliderect(player.sword_hitbox)]
            for tree in trees_attacked:
                tree.burn()
                player.hit_success = True

            players_attacked = [enemy for enemy in self.player_sprites if enemy.hitbox.colliderect(player.sword_hitbox)]
            for victim in players_attacked:
                if victim != player:
                    victim.take_damage(player.damage)
                    player.hit_success = True
            
        for house in self.houses_sprites:
            house.is_visible = False



    # display
    def update(self, dt):
        self.event_loop() 

        
        # update
        self.update_players_from_server()
        self.update_players_from_keyboard()

        self.collide_check()
        self.all_sprites.update(dt)

        self.send_player_data()
        self.server.update_indicator()
        self.fps_counter.ping()


        # draw
        self.display_surface.fill('beige')
        self.all_sprites.custom_draw(self.player.rect.center)
        self.server.online_indicator.draw()

        



########################################################################################################

    




    def regenerate_player(self, player, house):
        player.regenerate(house.healing_amount)




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