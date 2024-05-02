from cell import *
from grid import *

class Maze_Generator:
    def __init__(self, grid):
        self.grid = grid #object from grid class
        self.rows = grid.rows
        self.cols = grid.cols
        self.TILE = size_of_maze // self.rows
        self.completed = False
        self.create_maze()
        
    def create_maze(self):
        init_cell = self.grid.grid_cells[0][0]
        stack = []
        stack.append(init_cell)
        while stack != []:
            current_cell = stack[-1]
            next_cells = [cell for cell in current_cell.neighbors if not cell.seen]
            # current_cell.draw_current_cell(window)
            if next_cells == []:
                # quay lai diem current cell 
                # vi khong con neighbors nao cho 'next_cell'
                stack.pop() 
            else:
                next_cell = random.choice(next_cells) 
                Cell.check_bars(current_cell, next_cell)
                current_cell = next_cell
                stack.append(current_cell)
    
    def draw(self, window):
        # for i in range(self.rows * self.cols):
        #     self.grid.grid_cells[i].draw_bars(window, self.TILE)
        # self.grid.display_maze(window)    
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.grid_cells[i][j].draw_bars(window, self.TILE)