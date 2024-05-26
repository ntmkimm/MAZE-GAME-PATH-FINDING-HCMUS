import os
import random
import math
import pygame as pg
from cell import *
from color import *
from ui import *
            
class Player():
    ANIMATION_DELAY = 3
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
            self.SPRITES = load_sprite_sheets("MainCharacters", self.character, 64, 64, size_maze=self.rows)
        else:
            self.SPRITES = load_sprite_sheets("MainCharacters", self.character, 32, 32, size_maze=self.rows)

        self.x_direction = 'right'
        self.y_direction = ''

        self.animation_count = 0
        
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
        sprite_sheet = 'idle'
            
        sprite_type = sprite_sheet + "_" + self.x_direction
        sprites = self.SPRITES[sprite_type]
        index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.sprite = sprites[index]
        self.animation_count += 1    
        
    def draw(self, window):
        self.get_dynamic()
        window.blit(self.sprite, (self.rect.x, self.rect.y))
    
    def disappear(self):
        self.SPRITES = load_sprite_sheets("MainCharacters", "Disappear", 96, 96, size_maze=self.rows)
        