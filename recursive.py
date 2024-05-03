import pygame as pg 
from maze_generator import *

class Recursive:
    def __init__(self, grid_cells, start_pos):
        self.grid_cells = grid_cells
        self.y = start_pos[0]
        self.x = start_pos[1]
        
    def find_way(self, window, color, tile, trace, start_pos):
        
        trace.append((self.y, self.x))
        self.grid_cells[self.y][self.x].draw_current_cell(window, color, tile)
        self.grid_cells[self.y][self.x].visited = True
        self.grid_cells[self.y][self.x].is_start = False
        
        if (self.grid_cells[self.y][self.x].bars['top'] == False
            and self.grid_cells[self.y - 1][self.x].visited == False):
            self.y -= 1
        elif (self.grid_cells[self.y][self.x].bars['right'] == False
            and self.grid_cells[self.y][self.x + 1].visited  == False):
            self.x += 1
        elif (self.grid_cells[self.y][self.x].bars['bottom'] == False
            and self.grid_cells[self.y + 1][self.x].visited  == False):
            self.y += 1
        elif (self.grid_cells[self.y][self.x].bars['left'] == False
            and self.grid_cells[self.y][self.x - 1].visited == False):
            self.x -= 1
        else:
            trace.pop(-1)
            self.y = trace[-1][0]
            self.x = trace[-1][1]
            trace.pop(-1)
        
        start_pos[0] = self.y
        start_pos[1] = self.x
        self.grid_cells[self.y][self.x].is_start = True
        
        return start_pos

            
            