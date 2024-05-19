import pygame as pg 
from maze_generator import *
from collections import deque

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
        self.trace = deque()
        
    def find_way(self):
        self.trace.append((self.y, self.x))
        
        self.grid_cells[self.y][self.x].intersect = is_intersect(self.grid_cells[self.y][self.x])
        
        self.grid_cells[self.y][self.x].visited = True
        # self.grid_cells[self.y][self.x].is_current = False

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
            self.trace.pop()
            self.y = self.trace[-1][0]
            self.x = self.trace[-1][1]
            while self.grid_cells[self.y][self.x].intersect == False and len(self.trace) > 1:
                self.trace.pop()
                self.y = self.trace[-1][0]
                self.x = self.trace[-1][1]
            self.trace.pop()
        
    
    def trace_back(self):
        for pair in self.trace:
            if not self.grid_cells[pair[0]][pair[1]].is_goal \
                and not self.grid_cells[pair[0]][pair[1]].is_start:
                self.grid_cells[pair[0]][pair[1]].trace = True

            
            