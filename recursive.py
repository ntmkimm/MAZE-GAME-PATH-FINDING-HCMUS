import pygame as pg 
from maze_generator import *

def is_intersect(cell):
    count = 0
    if cell.bars['top'] == False:
        count += 1
    if cell.bars['right'] == False:
        count += 1
    if cell.bars['bottom'] == False:
        count += 1
    if cell.bars['left'] == False:
        count += 1
    if count > 2:
        return True
    if count <= 2:
        return False

class Recursive:
    def __init__(self, grid_cells, cur_pos):
        self.grid_cells = grid_cells
        self.y = cur_pos[0]
        self.x = cur_pos[1]
        
    def find_way(self, trace, cur_pos):
        
        trace.append((self.y, self.x))
        
        self.grid_cells[self.y][self.x].intersect = is_intersect(self.grid_cells[self.y][self.x])
        
        self.grid_cells[self.y][self.x].visited = True
        self.grid_cells[self.y][self.x].is_current = False

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
            while self.grid_cells[self.y][self.x].intersect == False and len(trace) > 1:
                trace.pop(-1)
                self.y = trace[-1][0]
                self.x = trace[-1][1]
            trace.pop(-1)
        
        cur_pos[0] = self.y
        cur_pos[1] = self.x
        self.grid_cells[self.y][self.x].is_current = True

            
            