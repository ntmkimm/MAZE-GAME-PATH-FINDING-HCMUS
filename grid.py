from cell import *
import json

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        #init Cell(y, x)
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.find_neighbor()     
    
    def find_neighbor(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if i != 0: # add neighbor top
                    self.cells[i][j].neighbors.append(self.cells[i - 1][j])
                if i != self.rows - 1: # add neighbor bottom
                    self.cells[i][j].neighbors.append(self.cells[i + 1][j])
                if j != 0: # add neighbor left
                    self.cells[i][j].neighbors.append(self.cells[i][j - 1])
                if j != self.cols - 1: # add neighbor right
                    self.cells[i][j].neighbors.append(self.cells[i][j + 1])

