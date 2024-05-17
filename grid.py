from cell import *

class Grid:
    def __init__(self, rows, cols, background):
        self.rows = rows
        self.cols = cols
        #init Cell(y, x)
        self.grid_cells = [[Cell(r, c, background) for c in range(cols)] for r in range(rows)]
        self.find_neighbor()   
        
    def random_destroy_bars():
        pass       
    
    def find_neighbor(self):
            
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

