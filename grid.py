from cell import *

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
        #init grid_cells
        self.grid_cells = [Cell(c, r) for r in range(rows) for c in range(cols)]
        self.find_neighbor()
        
    def index_cell(self, x, y):
        if x < 0 or x > COL - 1 or y < 0 or y > ROW - 1:
            return None
        return self.grid_cells[x + y * COL]
            
    
    def find_neighbor(self):
        for i, cell in enumerate(self.grid_cells):
            top = self.index_cell(cell.x, cell.y - 1)
            bottom = self.index_cell(cell.x, cell.y + 1)
            left = self.index_cell(cell.x - 1, cell.y)
            right = self.index_cell(cell.x + 1, cell.y)
            
            if top:
                self.grid_cells[i].neighbors.append(top)
            if right:
                self.grid_cells[i].neighbors.append(right)
            if bottom:
                self.grid_cells[i].neighbors.append(bottom)
            if left:
                self.grid_cells[i].neighbors.append(left)
