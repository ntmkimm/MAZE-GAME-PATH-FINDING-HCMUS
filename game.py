from maze_generator import *
from player import *
from color import *

from recursive import *
import time
import pygame as pg
import random

window = pg.display.set_mode((1200, 820))

class Game():
    def __init__(self, size, init_type, game_type):
        self.rows = size
        self.cols = size
        self.TILE = size_of_maze // size
        self.grid = Grid(self.rows, self.cols)
        self.maze = Maze_Generator(self.grid) 
        self.game_type = game_type
        self.trace = []
        
        if init_type == 'random':
            self.start_pos, self.goal_pos = self.init_random()
        elif init_type == 'choose':
            self.start_pos, self.goal_pos = (0, 0), (self.rows - 1, self.cols - 1) # step of the player is undone 
        self.cur_pos = self.start_pos
        
        self.grid.grid_cells[self.start_pos[0]][self.start_pos[1]].is_start = True
        self.grid.grid_cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = True
        
        self.player = Player(self.grid.grid_cells, self.start_pos, self.goal_pos, self.TILE)
        # self.name_game = name_game
        
        self.recursive = Recursive(self.grid.grid_cells, self.start_pos)
        
    def init_random(self):
        start, goal = (0, 0), (0, 0)
        while start == goal:
            start = [random.randrange(self.rows), random.randrange(self.cols)]
            goal = [random.randrange(self.rows), random.randrange(self.cols)]
        return start, goal
        
        
    def run_game(self, window):
        pg.init() 
        # clock = pg.time.Clock() 
        window.fill(light_blue)
        pg.display.set_caption("Maze - Path Finding") 
        
        while True:
            if self.game_type == 'player':
                self.loop()
            elif self.game_type == 'bot':
                if (self.grid.grid_cells[self.cur_pos[0]][self.cur_pos[1]].is_goal == True):
                    self.draw_last_trace()
                    time.sleep(5)
                    break
                self.loop_bot()
                
                # time.sleep(0.2)
             # quit pygame program
        print("is done")

    def loop(self):
        self.maze.draw(window)
        self.player.update_player()
        self.player.handle_move()
        self.player.draw(window)
        pg.display.update()
    
    def draw_last_trace(self):
        for i in range(len(self.trace)):
            self.grid.grid_cells[self.trace[i][0]][self.trace[i][1]].trace = True
        
        self.maze.draw(window)
        pg.display.update()
        
    def loop_bot(self):
        self.maze.draw(window)
        self.recursive.find_way(window, self.TILE, self.trace, self.cur_pos)
        pg.display.update()