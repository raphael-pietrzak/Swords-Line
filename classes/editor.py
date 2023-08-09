import pygame, sys
from classes.settings import *
from classes.player.gobelin import Gobelin
from classes.player.knight import Knight
from classes.player.animated import Animated

from random import randint
from pygame import Vector2 as vector

class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.imports()

        # decoration
        self.sprites_group = CameraGroup()
        self.player_group = pygame.sprite.Group()
        self.player1_group = pygame.sprite.Group()
        self.player2_group = pygame.sprite.Group()
        
        Animated(self.animations[2]['frames'], (600, 100), self.sprites_group)
        Animated(self.animations[5]['frames'], (1200, 100), self.sprites_group)
        Animated(self.animations[2]['frames'], (800, 100), self.sprites_group)
        Animated(self.animations[5]['frames'], (800, 100), self.sprites_group)
        Animated(self.animations[2]['frames'], (200, 100), self.sprites_group)
        Animated(self.animations[5]['frames'], (300, 100), self.sprites_group)

        # player
        Gobelin(self.animations[3]['frames'], (800, 100), [self.sprites_group, self.player_group, self.player1_group])        
        Knight(self.animations[4]['frames'], (600, 200), [self.sprites_group, self.player_group, self.player2_group])

        Gobelin(self.animations[3]['frames'], (800, 100), [self.sprites_group, self.player_group, self.player1_group])
        Gobelin(self.animations[3]['frames'], (600, 200), [self.sprites_group, self.player_group, self.player1_group])
        Knight(self.animations[4]['frames'], (600, 200), [self.sprites_group, self.player_group, self.player2_group])
        Knight(self.animations[4]['frames'], (800, 100), [self.sprites_group, self.player_group, self.player2_group])

        self.player1_index = 0 
        self.player2_index = 0

        self.player1 = self.player1_group.sprites()[self.player1_index]
        self.player2 = self.player2_group.sprites()[self.player2_index]


    def imports(self):
        self.animations = {}
        for key, value in EDITOR_DATA.items():
            sprite_sheet = pygame.image.load(value['path']).convert_alpha()
            frames = self.get_frames_from_sprite_sheet(sprite_sheet, value['cols'], value['rows'])
            self.animations[key] = {'frames': frames, 'index': 0, 'length': len(frames)}


    def switch_player(self, player):
        if player == 'player1':
            self.player1_index = (self.player1_index + 1) % len(self.player1_group)
            self.player1 = self.player1_group.sprites()[self.player1_index]
        else:
            self.player2_index = (self.player2_index + 1) % len(self.player2_group)
            self.player2 = self.player2_group.sprites()[self.player2_index]

    def get_frames_from_sprite_sheet(self, sheet, cols, rows):
        frames = []
        frame_width = sheet.get_width() // cols
        frame_height = sheet.get_height() // rows

        for row in range(rows): # cut out frames
            for col in range(cols):
                rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                frame = sheet.subsurface(rect)
                frames.append(frame)
        i = 0
        for image in frames: # remove empty images
            i += 1
            width, height = image.get_size()
            alpha1 = image.get_at((width // 2, height // 2))[3]
            alpha2 = image.get_at((width // 2, 3 * height // 4 -5 ))[3]
            if alpha1 == 0 and alpha2 == 0:
                frames.remove(image)
        return frames
    


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for player in self.player_group:
                # player.event_loop(event)
                if player.is_dead:
                    Animated(self.animations[1]['frames'], player.rect.center, self.sprites_group)
                    if player.id == 1:
                        Gobelin(player.frames, (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), player.group)
                    else:
                        Knight(player.frames, (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), player.group)
                    player.kill()

                    
            self.player1 = self.player1_group.sprites()[self.player1_index]
            self.player2 = self.player2_group.sprites()[self.player2_index]

            self.player1.event_loop(event)
            self.player2.event_loop(event)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    self.switch_player("player1")
                if event.key == pygame.K_LSHIFT:
                    self.switch_player("player2")


    def get_barycenter(self, sprite1, sprite2):
        # Get the positions of the sprites
        x1, y1 = sprite1.rect.center
        x2, y2 = sprite2.rect.center

        # If the sprites have weights, you can include them in the calculation
        weight1 = 1  # Replace with the actual weight of sprite1
        weight2 = 1  # Replace with the actual weight of sprite2

        # Calculate the weighted sum of x and y coordinates
        weighted_sum_x = (x1 * weight1) + (x2 * weight2)
        weighted_sum_y = (y1 * weight1) + (y2 * weight2)

        # Calculate the total weight
        total_weight = weight1 + weight2

        # Calculate the barycenter
        barycenter_x = weighted_sum_x / total_weight
        barycenter_y = weighted_sum_y / total_weight

        return vector(barycenter_x, barycenter_y)





           
            

    def update(self, dt):
        self.display_surface.fill('beige')
        for sprite in self.sprites_group:
            sprite.update(dt)
        barycentre = self.get_barycenter(self.player1, self.player2)
        self.sprites_group.custom_draw(barycentre)

        # self.sprites_group.draw(self.display_surface)
        # for sprite in self.player_group:
        #     pygame.draw.rect(self.display_surface, 'yellow', sprite.hitbox)
        self.event_loop()



class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector(0, 0)
        self.display_surface = pygame.display.get_surface()
    
    def custom_draw(self, barycentre):
        self.offset.x = WINDOW_WIDTH // 2 - barycentre.x
        self.offset.y = WINDOW_HEIGHT // 2 - barycentre.y

        for sprite in self.sprites():
            sprite.pos += self.offset
            self.display_surface.blit(sprite.image, sprite.rect)


        