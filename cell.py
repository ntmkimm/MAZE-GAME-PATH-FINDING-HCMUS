import pygame as pg
import random
from color import *

size_of_maze = 760

class Cell:
    def __init__(self, y, x):
        self.x, self.y = x, y # x - index of col, y - index of row
        self.bars = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        self.init_maze_x = 20
        self.init_maze_y = 20
        
        self.is_start = False
        self.is_goal = False
        self.neighbors = []
        
        self.seen = False
        self.visited = False
        
        self.bar_color = black
        self.bar_thick = 1
        
        self.goal_color = red
        
    def draw_current_cell(self, window, color, TILE):
        x, y = self.init_maze_x + self.x * TILE, self.init_maze_y + self.y * TILE
        if self.visited == True:
            pg.draw.rect(window, gray, (x + 2 * self.bar_thick, y + 2 * self.bar_thick, TILE - 4 * self.bar_thick, TILE - 4 * self.bar_thick))
    
        pg.draw.rect(window, color, (x + 2 * self.bar_thick, y + 2 * self.bar_thick, TILE - 4 * self.bar_thick, TILE - 4 * self.bar_thick))
    
    def check_bars(current, next):
        dx = next.x - current.x
        dy = next.y - current.y
        
        current.seen = True
        next.seen = True
        
        if dx == 1: # current|next
            current.bars['right'] = False
            next.bars['left'] = False
        elif dx == -1: # next|current
            next.bars['right'] = False
            current.bars['left'] = False
        if dy == 1: #current/next (current is above next)
            next.bars['top'] = False
            current.bars['bottom'] = False
        elif dy == -1: #next/current
            next.bars['bottom'] = False
            current.bars['top'] = False
        # print(current.bars)
        # print(next.bars)
    
    def draw_bars(self, window, TILE):
        x, y = self.init_maze_x + self.x * TILE, self.init_maze_y + self.y * TILE
        
        if self.is_goal:
            pg.draw.rect(window, self.goal_color, (x + 2, y + 2, TILE - 4, TILE - 4))
        elif self.seen:
            pg.draw.rect(window, white, (x, y, TILE, TILE))
        
        if self.bars['top']:
            pg.draw.line(window, self.bar_color, (x, y), (x + TILE, y), self.bar_thick)
        if self.bars['bottom']:
            pg.draw.line(window, self.bar_color, (x, y + TILE), (x + TILE, y + TILE), self.bar_thick)
        if self.bars['left']:
            pg.draw.line(window, self.bar_color, (x, y), (x, y + TILE), self.bar_thick)
        if self.bars['right']:
            pg.draw.line(window, self.bar_color, (x + TILE, y), (x + TILE, y + TILE), self.bar_thick)
            

        
        
        
                
        
