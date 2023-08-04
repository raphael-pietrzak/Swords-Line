import pygame, sys
from classes.settings import *
from classes.sprites import Animated, Gobelin, Knight
from random import randint

class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.imports()

        # decoration
        self.sprites_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        Animated(self.animations[2]['frames'], (400, 100), self.sprites_group)
        Animated(self.animations[5]['frames'], (1000, 100), self.sprites_group)

        # player
        self.player1 = Gobelin(self.animations[3]['frames'], (800, 100), [self.sprites_group, self.player_group])        
        self.player2 = Knight(self.animations[4]['frames'], (600, 200), [self.sprites_group, self.player_group])

        Gobelin(self.animations[3]['frames'], (200, 100), [self.sprites_group, self.player_group])
        Knight(self.animations[4]['frames'], (300, 200), [self.sprites_group, self.player_group])
        Gobelin(self.animations[3]['frames'], (400, 100), [self.sprites_group, self.player_group])
        Knight(self.animations[4]['frames'], (500, 200), [self.sprites_group, self.player_group])

    def imports(self):
        self.animations = {}
        for key, value in EDITOR_DATA.items():
            sprite_sheet = pygame.image.load(value['path']).convert_alpha()
            frames = self.get_frames_from_sprite_sheet(sprite_sheet, value['cols'], value['rows'])
            self.animations[key] = {'frames': frames, 'index': 0, 'length': len(frames)}


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
                player.event_loop(event)
                if player.is_dead:
                    Animated(self.animations[1]['frames'], player.rect.center, self.sprites_group)
                    if player.id == 1:
                        Gobelin(player.frames, (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), player.group)
                    else:
                        Knight(player.frames, (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), player.group)
                    player.kill()

            # self.player1.event_loop(event)
            # self.player2.event_loop(event)

                    
            

    def update(self, dt):
        self.display_surface.fill('beige')
        for sprite in self.sprites_group:
            sprite.update(dt)
        self.sprites_group.draw(self.display_surface)
        # for sprite in self.player_group:
        #     pygame.draw.rect(self.display_surface, 'yellow', sprite.hitbox)
        self.event_loop()



class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def custom_draw(self):
        pass