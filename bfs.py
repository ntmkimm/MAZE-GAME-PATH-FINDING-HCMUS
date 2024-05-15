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
        self.result = deque([deque([(cur_pos[0], cur_pos[1])])])

    def find_way(self):
        # while 
        if self.result == []:
            return
        start = self.result.popleft() # frist: start is [(y, x)]
        current_cell = self.grid_cells[start[-1][0]][start[-1][1]] #current cell là start[-1] trong code ban đầu 
        current_cell.visited = True
        # print(self.result)
        if current_cell.is_goal: # if end in start:
            self.y, self.x = current_cell.y, current_cell.x
            self.trace = start.copy()
            return
            f_temp = start.copy()
            #thay vì tìm tất cả các bước - khi bước đi của f_temp < final_list thì mới cập nhật
            # if len(f_temp) < len(self.final_list):
            #     self.final_list = f_temp
        else:
            # có 4 hướng đi tối đa, nên loops qua 4 vòng lặp
            for direct in range(4): # for v in V:
                if not current_cell.bars[di[direct]]: 
                    #dòng trên tương đương if (start[-1], v) in E or (v, start[-1]) in E: (nếu có đường đi)
                    next_cell = self.grid_cells[current_cell.y + dy[direct]][current_cell.x + dx[direct]]
                    if (next_cell.y, next_cell.x) not in start and not next_cell.visited:
                        temp = start.copy()
                        temp.append((next_cell.y, next_cell.x))
                        self.result.append(temp)
                        next_cell.visited == True
        # time.sleep(0.2)
                            
    def trace_back(self):
        for pair in self.trace:
            self.grid_cells[pair[0]][pair[1]].trace = True
            
                            