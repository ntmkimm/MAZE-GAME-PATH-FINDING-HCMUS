from maze_generator import *
from player import *
from color import *
import pygame as pg



class Game():
    def __init__(self, window, size):
        self.window = window
        self.rows = size
        self.cols = size
        self.TILE = size_of_maze // size
        self.grid = Grid(self.rows, self.cols)
        self.maze = Maze_Generator(self.grid)
        self.player = Player(self.grid.grid_cells, 0, self.TILE, self.TILE)
        self.mode = 0
        # self.name_game = name_game
        
    def run_game(self, window):
        pg.init() 
        # clock = pg.time.Clock() 
        window.fill(light_blue)
        pg.display.set_caption("Maze - Path Finding") 
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    pg.quit()
                    break
            self.loop()
             # quit pygame program
        quit() # quit python program

    def loop(self):
        self.maze.draw(self.window)
        self.player.update_player()
        self.player.handle_move()
        self.player.draw(self.window)
        pg.display.update()