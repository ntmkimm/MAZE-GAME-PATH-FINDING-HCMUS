import pygame as pg
import random
from color import *
import os
import pygame as pg

size_of_maze = 800
dust = pg.image.load(os.path.join("pic", "dust.png")) 
# start = pg.image.load()
checkpoint = pg.image.load(os.path.join("pic", "checkpoint.png")) 

class Cell:
    def __init__(self, y, x, background):
        self.x, self.y = x, y # x - index of col, y - index of row
        self.bars = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        self.init_maze_x = 10
        self.init_maze_y = 10
        
        self.is_start = False
        self.is_current = False
        self.is_goal = False
        self.neighbors = []
        
        self.intersect = False
        self.cost = 0
        
        self.seen = False
        self.visited = False
        self.trace = False
        self.background = background
        
        self.bar_color = black
        self.bar_thick = 2
        
        self.start_color = dark_blue
        self.goal_color = red
    
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
    
    def draw(self, window, TILE):
        x, y = self.init_maze_x + self.x * TILE, self.init_maze_y + self.y * TILE
        
        if self.seen and self.background != None:
            # pg.draw.rect(window, white, (x, y, TILE, TILE))
            window.blit(pg.transform.scale(self.background, (TILE, TILE)), (x, y))
            
        if self.trace == True:
            window.blit(pg.transform.scale(checkpoint, (TILE, TILE)), (x, y))
        elif self.visited == True:
            # pg.draw.rect(window, gray, (x, y, TILE, TILE))
            window.blit(pg.transform.scale(dust, (TILE, TILE)), (x, y))
            
        # if self.is_current:
        #     pg.draw.rect(window, green, (x, y, TILE, TILE))
        if self.is_start:
            pg.draw.rect(window, dark_blue, (x, y, TILE, TILE))
            # window.blit()
        if self.is_goal:
            pg.draw.rect(window, red, (x, y, TILE, TILE))
        
        if self.bars['top']:
            pg.draw.line(window, self.bar_color, (x, y), (x + TILE, y), self.bar_thick)
        if self.bars['bottom']:
            pg.draw.line(window, self.bar_color, (x, y + TILE), (x + TILE, y + TILE), self.bar_thick)
        if self.bars['left']:
            pg.draw.line(window, self.bar_color, (x, y), (x, y + TILE), self.bar_thick)
        if self.bars['right']:
            pg.draw.line(window, self.bar_color, (x + TILE, y), (x + TILE, y + TILE), self.bar_thick)
            

            

        
        
        
                
        
