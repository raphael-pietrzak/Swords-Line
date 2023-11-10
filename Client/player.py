


from random import randint
import time

from pygame import Vector2 as vector

from  classes.settings import *



class Player:
    def __init__(self):
        self.pos = vector((randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        self.speed = 400
        self.last_update_time = time.time()
        self.color =  (randint(0, 255), randint(0, 255), randint(0, 255))
        self.inputs = []

    def move(self, inputs):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        if 'up' in inputs:
            self.pos.y -= self.speed * time_elapsed
        if 'down' in inputs:
            self.pos.y += self.speed * time_elapsed
        if 'left' in inputs:
            self.pos.x -= self.speed * time_elapsed
        if 'right' in inputs:
            self.pos.x += self.speed * time_elapsed
    
    def get_position(self):
        return [int(self.pos.x), int(self.pos.y)]