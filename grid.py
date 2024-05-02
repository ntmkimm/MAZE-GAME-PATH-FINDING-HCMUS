from cell import *

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        #init grid_cells Cell(x, y)
        self.grid_cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.find_neighbor()
        
    def index_cell(self, x, y): # x - col; y - row
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return None
        return self.grid_cells[x + y * self.rows]
            
    
    def find_neighbor(self):
        # for i, cell in enumerate(self.grid_cells):
        #     top = self.index_cell(cell.x, cell.y - 1)
        #     bottom = self.index_cell(cell.x, cell.y + 1)
        #     left = self.index_cell(cell.x - 1, cell.y)
        #     right = self.index_cell(cell.x + 1, cell.y)
            
        #     if top:
        #         self.grid_cells[i].neighbors.append(top)
        #     if right:
        #         self.grid_cells[i].neighbors.append(right)
        #     if bottom:
        #         self.grid_cells[i].neighbors.append(bottom)
        #     if left:
        #         self.grid_cells[i].neighbors.append(left)
            
        for i in range(self.rows):
            for j in range(self.cols):
                if i != 0: # add neighbor top
                    self.grid_cells[i][j].neighbors.append(self.grid_cells[i - 1][j])
                if i != self.rows - 1: # add neighbor bottom
                    self.grid_cells[i][j].neighbors.append(self.grid_cells[i + 1][j])
                if j != 0: # add neighbor left
                    self.grid_cells[i][j].neighbors.append(self.grid_cells[i][j - 1])
                if j != self.cols - 1: # add neighbor right
                    self.grid_cells[i][j].neighbors.append(self.grid_cells[i][j + 1])

