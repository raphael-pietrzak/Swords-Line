import pygame, sys
from classes.settings import *
from pygame import Vector2 as vector
from classes.player import Square
from classes.client import Client


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.imports()
        self.client = Client()
        self.players_data = {}
        self.inputs_data = {}


    # support
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

    # event
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
    

    def draw(self):
        print(self.players_data)
        for key, value in self.players_data.items():
            if 'position' in value:
                x = value['position']['x']
                y = value['position']['y']
                rect = pygame.Rect(x, y, 50, 50)
                pygame.draw.rect(self.display_surface, BLUE_CONTOUR, rect)

    def update_inputs(self):
        self.inputs_data["movement"] = self.movement()

    

            

    # update
    def update(self, dt):
        self.display_surface.fill('beige')
        self.event_loop()   
        self.update_inputs()

        print(self.inputs_data)
        self.players_data = self.client.send(self.inputs_data)

        self.draw()
    




class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector(0, 0)
        self.display_surface = pygame.display.get_surface()
    
    def custom_draw(self, position):
        self.offset.x = WINDOW_WIDTH // 2 - position.x
        self.offset.y = WINDOW_HEIGHT // 2 - position.y

        for sprite in self.sprites():
            sprite.pos += self.offset
            self.display_surface.blit(sprite.image, sprite.rect)