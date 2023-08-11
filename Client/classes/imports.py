from classes.settings import *
import pygame

class Imports:
    def __init__(self):
        self.animations = {}  
        self.imports()

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