import pygame as pg 
from maze_generator import *
from collections import deque
import time

dx = (0, 1, 0, -1)
dy = (-1, 0, 1, 0)
di = ('top', 'right', 'bottom', 'left')

class BFS:
    def __init__(self, grid_cells, cur_pos):
        self.grid_cells = grid_cells
        self.y = cur_pos[0]
        self.x = cur_pos[1]
        self.q = deque([(self.y, self.x)])
        self.grid_cells[self.y][self.x].visited = True
        self.rows = len(self.grid_cells)
        self.cols = len(self.grid_cells[0])
        self.previous = [[-1 for i in range(self.cols)] for j in range(self.rows)]
        self.trace = []
        
    def find_way(self):
        #while q != []:
        self.y, self.x = self.q.pop()
        # self.grid_cells[self.y][self.x].trace = True
        
        if self.grid_cells[self.y][self.x].is_goal == True:
            return
        
        current_cell = self.grid_cells[self.y][self.x]
        
        for direct in range(4):
            y_next = self.y + dy[direct]
            x_next = self.x + dx[direct]
            
            if current_cell.bars[di[direct]] == False:
                next_cell = self.grid_cells[y_next][x_next]
            
                if next_cell.visited == False:
                    # next_cell.cost = current_cell.cost + 1
                    self.previous[y_next][x_next] = (self.y, self.x)
                    next_cell.visited = True
                    self.q.appendleft((y_next, x_next))
                    # time.sleep(0.05)
        
    def trace_back(self, goal):
        if self.grid_cells[goal[0]][goal[1]].visited == False:
            return 'no path'
        
        self.trace = deque()
        current = goal
        while current != -1:
            self.trace.append(current)
            current = self.previous[current[0]][current[1]]
        
        
        
        
        
        
        