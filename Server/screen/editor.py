import pygame, sys
from random import choice, randint

from classes.settings import *
from classes.imports import Graphics
from classes.camera import CameraGroup
from entities.player import Goblin, Knight
from entities.sprites import  Flame, Tree
from entities.houses import House
from network.server import Server
from classes.ping import FPSCounter
from menu.end_party import EndPartySurface

class Editor:
    def __init__(self, switch):
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.switch_screen = switch
        self.fps_counter = FPSCounter('MAIN')
        self.end_game_screen = EndPartySurface(self.switch_screen)
        self.is_game_over = False

        # groups
        self.all_sprites = CameraGroup()
        self.player_sprites = pygame.sprite.Group()
        self.trees_sprites = pygame.sprite.Group()
        self.houses_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.players = {}

        # animations
        self.animations = Graphics().animations

        # map
        self.build_map()

        # server
        self.server = Server()


    # imports
    def build_map(self):
        
        for _ in range(100):
            Tree((randint(-900, 900), randint(-900, 900)), self.animations['tree'], self.animations['tree_fire'], [self.all_sprites, self.trees_sprites], self.collision_sprites)
        
        self.knight_house = House((300, 300), self.animations['knight_house'], [self.all_sprites, self.houses_sprites], "knight")
        self.goblin_house = House((20, 20), self.animations['goblin_house'], [self.all_sprites, self.houses_sprites], "goblin")
        
        Flame((200, 400), self.animations['fire'], [self.all_sprites, self.damage_sprites])


        self.player1 = Goblin((300, 300), self.animations['goblin'], [self.all_sprites, self.player_sprites], self.goblin_house, self.collision_sprites)
        self.player2 = Knight((200, 200), self.animations['knight'], [self.all_sprites, self.player_sprites], self.knight_house, self.collision_sprites)
        self.offline_players = [self.player1, self.player2]

        self.players['player1'] = self.player1
        self.players['player2'] = self.player2
        


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
                    self.switch_screen("home")

                if event.key == pygame.K_h:
                    self.all_sprites.hitbox_active = not self.all_sprites.hitbox_active

                if event.key == pygame.K_o:
                    self.server.toggle()

                if event.key == pygame.K_s:
                    self.offline_player_index += 1
                    if self.offline_player_index >= len(self.offline_players):
                        self.offline_player_index = 0
                    self.player = self.offline_players[self.offline_player_index]

            if self.is_game_over:
                self.end_game_screen.event_loop(event)

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
    
    def update_players_from_server(self):
        # Utilisation conseillée :
        new_players = self.server.get_new_clients()
        if new_players:
            for uuid in new_players:
                print(f'[ NEW PLAYER ] : {uuid}')
                player = self.generate_player()
                self.players[uuid] = player
                self.server.send({'data': 'TCP message init'}, 'TCP')
            

        del_players = self.server.get_del_clients()
        if del_players:
            for uuid in del_players:
                print(f'[ DEL PLAYER ] : {uuid}')
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
        # message = {uuid: {'color': player.color, 'pos': player.get_position()} for uuid, player in self.players.items()}
        message = {uuid: player.get_data() for uuid, player in self.players.items()}
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

    def get_damage(self):
        damage_sprites = pygame.sprite.spritecollide(self.player, self.damage_sprites, False, pygame.sprite.collide_mask)
        for sprite in damage_sprites:
            if not sprite.attack_cooldown.active:
                self.player.take_damage(sprite.damage)
                sprite.attack_cooldown.activate()

    def check_game_end(self):
        for player in self.player_sprites:
            if player.dead:
                # self.is_game_over = True
                # self.server.close()
                # player.kill()
                break



    # display
    def update(self, dt):
        self.event_loop() 

        
        # update
        self.update_players_from_server()
        self.update_players_from_keyboard()

        self.collide_check()
        self.all_sprites.update(dt)

        self.get_damage()
        self.check_game_end()

        self.send_player_data()
        # self.server.update_indicator()
        self.fps_counter.ping()


        # draw
        self.display_surface.fill('beige')
        self.all_sprites.custom_draw(self.player.rect.center)
        # self.server.online_indicator.draw()
        self.end_game_screen.draw() if self.is_game_over else None
        self.player.lifes_bar.draw()

        