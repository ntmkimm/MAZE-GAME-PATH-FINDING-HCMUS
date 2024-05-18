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
            if next_cells == []:
                # quay lai diem current cell 
                # vi khong con neighbors nao cho 'next_cell'
                stack.pop() 
            else:
                next_cell = random.choice(next_cells) 
                Cell.check_bars(current_cell, next_cell)
                current_cell = next_cell
                stack.append(current_cell)
                
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                value = random.sample(['top', 'none1', 'right','none2', 'bottom','none3', 'left','none4'], 1)
                for direction in value:
                    # if direction == 'none': break
                    if direction == 'top' and self.grid.grid_cells[i][j].bars['top'] == True:
                        temp = random.choice([True, False])
                        self.grid.grid_cells[i][j].bars['top'] = temp
                        self.grid.grid_cells[i - 1][j].bars['bottom'] = temp
                    if direction == 'right' and self.grid.grid_cells[i][j].bars['right'] == True:
                        temp = random.choice([True, False])
                        self.grid.grid_cells[i][j].bars['right'] = temp
                        self.grid.grid_cells[i][j + 1].bars['left'] = temp
                    if direction == 'left' and self.grid.grid_cells[i][j].bars['left'] == True:
                        temp = random.choice([True, False])
                        self.grid.grid_cells[i][j].bars['left'] = temp
                        self.grid.grid_cells[i][j - 1].bars['right'] = temp
                    if direction == 'bottom' and self.grid.grid_cells[i][j].bars['bottom'] == True:
                        temp = random.choice([True, False])
                        self.grid.grid_cells[i][j].bars['bottom'] = temp
                        self.grid.grid_cells[i + 1][j].bars['top'] = temp

    
    def draw(self, window, background): 
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.grid_cells[i][j].draw(window, self.TILE, background)