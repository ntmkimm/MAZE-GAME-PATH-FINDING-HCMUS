import pygame as pg
from maze_generator import *
from collections import deque

dx = (0, 1, 0, -1)
dy = (-1, 0, 1, 0)
di = ('top', 'right', 'bottom', 'left')

class BFS:
    def __init__(self, grid_cells, cur_pos):
        self.grid_cells = grid_cells
        self.y = cur_pos[0]
        self.x = cur_pos[1]
        self.result = [ [ (cur_pos[0], cur_pos[1]) ] ] 
        self.final_list = []

    def find_way(self):
        # while 
        print(self.result)
        start = self.result.pop(0) # frist: start is [(y, x)]
        if self.grid_cells[start[-1][0]][start[-1][0]].is_goal == True: # if end in start:
            f_temp = start.copy()
            #thay vì tìm tất cả các bước - khi bước đi của f_temp < final_list thì mới cập nhật
            if len(f_temp) < len(self.final_list):
                self.final_list = f_temp
        else:
            # có 4 hướng đi tối đa, nên loops qua 4 vòng lặp
            for direct in range(4): # for v in V:
                current_cell = self.grid_cells[start[-1][0]][start[-1][0]] 
                # dòng trên tương đương current cell là v (hay start[-1]) trong code ban đầu 
                if current_cell.bars[di[direct]] == False: 
                    #dòng trên tương đương if (start[-1], v) in E or (v, start[-1]) in E: (nếu có đường đi)
                    if (current_cell.y, current_cell.x) not in start:
                        temp = start.copy()
                        temp.append((current_cell.y, current_cell.x))
                        self.result.append(temp)
                        current_cell.visited = True
                        
                            
    def trace_back(self, goal):
        for pair in range(len(self.final_list)):
            self.grid_cells[pair[0]][pair[1]].trace = True
            
                            