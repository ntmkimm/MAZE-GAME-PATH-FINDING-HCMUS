import pygame as pg
import random
from color import *

#global variables
FPS = 60 #frames per second

RES = WIDTH, HEIGHT = 1200, 800
COL, ROW = 40, 40
TILE = HEIGHT // COL  

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y # x - width, y - height
        self.bars = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        # self.is_start = False
        # self.is_end = False
        # self.is_current = False
        
        # self.is_path = False
        # self.display_path = False
        
        # self.highlight = white
        # self.display_highlight = False
        # self.is_player = False
        self.neighbors = []
        # self.is_avail = True
        
        self.seen = False
        self.bar_color = black
        self.bar_thick = 1
        
    # def draw_current_cell(self, window):
    #     x, y = self.x * TILE, self.y * TILE
    #     pg.draw.rect(window, red, (x + self.bar_thick, y + self.bar_thick, TILE - self.bar_thick, TILE - self.bar_thick))
        
        # return random.choice(self.neighbors) if self.neighbors else None
    
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
    
    def draw_bars(self, window):
        x, y = self.x * TILE, self.y * TILE
        
        if self.seen:
            pg.draw.rect(window, gray, (x, y, TILE, TILE))
        
        if self.bars['top']:
            pg.draw.line(window, self.bar_color, (x, y), (x + TILE, y), self.bar_thick)
        if self.bars['bottom']:
            pg.draw.line(window, self.bar_color, (x, y + TILE), (x + TILE, y + TILE), self.bar_thick)
        if self.bars['left']:
            pg.draw.line(window, self.bar_color, (x, y), (x, y + TILE), self.bar_thick)
        if self.bars['right']:
            pg.draw.line(window, self.bar_color, (x + TILE, y), (x + TILE, y + TILE), self.bar_thick)

    def check_collide(self):
        if self.bars['top']:
            pass
        if self.bars['bottom']:
            pass
        if self.bars['right']:
            pass
        if self.bars['left']:
            pass
        
                
        
