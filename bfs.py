import pygame as pg
from maze_generator import *
from collections import deque
import time

dx = (0, 1, 0, -1)
dy = (-1, 0, 1, 0)
di = ('top', 'right', 'bottom', 'left')


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None


class Linkedlist:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_head(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            current_node = self.head
            self.head = node
            node.next = current_node
            current_node.previous = node

    def add_tail(self, node):
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            current_node = self.tail
            self.tail = node
            current_node.next = node
            node.previous = current_node

    def delete_head(self):
        if self.head is None:
            return None
        elif self.head.next is None:
            current_node = self.head
            self.head = None
            self.tail = None
            return current_node
        else:
            current_node = self.head
            self.head = current_node.next
            self.head.previous = None
            return current_node

    def delete_tail(self):
        if self.tail is None:
            return None
        elif self.head.previous is None:
            current_node = self.tail
            self.head = None
            self.tail = None
            return current_node
        else:
            current_node = self.tail
            self.tail = current_node.previous
            self.tail.next = None
            return current_node


class BFS:
    def __init__(self, grid_cells, cur_pos):
        self.grid_cells = grid_cells
        self.y = cur_pos[0]
        self.x = cur_pos[1]
        self.node = Node([cur_pos])
        self.result = Linkedlist()
        self.result.add_head(self.node)
        self.trace = None

    def find_way(self):
        if self.result.head is None or self.result.tail is None:
            return
        start = self.result.delete_head()  # frist: start is [(y, x)]
        current_cell = self.grid_cells[start.data[-1][0]][start.data[-1][1]]  # current cell là start[-1] trong code ban đầu
        current_cell.visited = True
        if current_cell.is_goal:  # if end in start:
            self.y, self.x = current_cell.y, current_cell.x
            self.trace = start.data.copy()
            return
            # f_temp = start.copy()
            # thay vì tìm tất cả các bước - khi bước đi của f_temp < final_list thì mới cập nhật
            # if len(f_temp) < len(self.final_list):
            #     self.final_list = f_temp
        else:
            # có 4 hướng đi tối đa, nên loops qua 4 vòng lặp
            for direct in range(4):
                if not current_cell.bars[di[direct]]:
                    next_cell = self.grid_cells[current_cell.y + dy[direct]][current_cell.x + dx[direct]]
                    if (next_cell.y, next_cell.x) not in start.data and not next_cell.visited:
                        temp = Node(start.data.copy())
                        temp.data.append((next_cell.y, next_cell.x))
                        self.result.add_tail(temp)
                        next_cell.visited = True

    def trace_back(self):
        for pair in self.trace:
            if not self.grid_cells[pair[0]][pair[1]].is_goal \
                and not self.grid_cells[pair[0]][pair[1]].is_start:
                self.grid_cells[pair[0]][pair[1]].trace = True

            
                            