import os
import random
import math
import pygame as pg
from cell import *
from color import *
from ui import *
            
class Player(): # sprite make it easy to fit pixel perfect

    ANIMATION_DELAY = 3
    # define our initialization area
    
    def __init__(self, grid_cells, init_pos, tile, character):
        # inherit Cell class
        Cell.__init__(self, init_pos[0], init_pos[1])
        self.grid_cells = grid_cells
        self.rows = len(self.grid_cells)
        self.cols = self.rows
        self.TILE = tile
        self.character = character
        self.rect = pg.Rect(self.init_maze_x + self.x * self.TILE, self.init_maze_y + self.y * self.TILE, self.TILE, self.TILE)
        self.x_step = 0
        self.y_step = 0

        if self.character == "End":
            self.SPRITES = load_sprite_sheeets("MainCharacters", self.character, 64, 64, size_maze=self.rows)
        else:
            self.SPRITES = load_sprite_sheeets("MainCharacters", self.character, 32, 32, size_maze=self.rows)
    
        self.mask = None
        self.x_direction = 'right'
        self.y_direction = ''

        self.animation_count = 0
        self.steps = 0
        self.start = 0
        self.time = 0
        
    def move(self, dx=0, dy=0):
        if dx < 0:
            self.x_direction = "left"
            self.x_step = -self.TILE
            self.x -= 1
        elif dx > 0:
            self.x_direction = "right"
            self.x_step = self.TILE
            self.x += 1
        if dy < 0:
            self.y_direction = "up"
            self.y_step = -self.TILE
            self.y -= 1
        elif dy > 0:
            self.y_direction = "down"
            self.y_step = self.TILE
            self.y += 1
        self.rect.x += self.x_step
        self.rect.y += self.y_step
    
    def get_dynamic(self):
        #MAKING PLAYER LOOK DYNAMIC
        sprite_sheet = 'idle'
            
        sprite_type = sprite_sheet + "_" + self.x_direction
        sprites = self.SPRITES[sprite_type]
        index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.sprite = sprites[index]
        self.animation_count += 1    
        self.masking()
    
    def masking(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)
    
    # draw character everytime we update the position of the character
    def draw(self, window):
        self.get_dynamic()
        window.blit(self.sprite, (self.rect.x, self.rect.y))
    
    # def draw_goal(self, window):
    #     rect = self.init_maze_x + self.x * self.TILE + 2, self.init_maze_y + self.y * self.TILE + 2, self.TILE - 3, self.TILE - 3
    #     pg.draw.rect(window, red, rect)
        