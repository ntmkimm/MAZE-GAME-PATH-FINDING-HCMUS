from maze_generator import *
from player import *
from color import *
import pygame as pg
import random


class Game():
    def __init__(self, window, size, init):
        self.window = window
        self.rows = size
        self.cols = size
        self.TILE = size_of_maze // size
        self.grid = Grid(self.rows, self.cols)
        self.maze = Maze_Generator(self.grid)
        if init == 'random':
            self.start_pos, self.goal_pos = self.init_random()
        # elif init == 'choose':
        #     self.start_pos, self.goal_pos = self
        
        self.player = Player(self.grid.grid_cells, self.start_pos, self.goal_pos, self.TILE)
        # self.name_game = name_game
        
    def init_random(self):
        start, goal = (0, 0), (0, 0)
        while start == goal:
            start = (random.randint(0, self.rows), random.randint(0, self.cols))
            goal = (random.randint(0, self.rows), random.randint(0, self.cols))
        return start, goal
        
        
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