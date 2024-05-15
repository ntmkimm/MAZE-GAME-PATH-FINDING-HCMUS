from maze_generator import *
from player import *
from color import *

from recursive import *
from bfs import *
# from main import *
import time
import pygame as pg
import random

RES = WIDTH, HEIGHT = 1200, 820
window = pg.display.set_mode(RES)

class Game():
    def __init__(self, size, init_type, game_type, algo):
        self.rows = size
        self.cols = size
        self.TILE = size_of_maze // size
        self.grid = Grid(self.rows, self.cols)
        self.maze = Maze_Generator(self.grid) 
        self.game_type = game_type
        self.algo = algo
        self.command = None
        
        self.pause = False
        
        if init_type == 'random':
            self.start_pos, self.goal_pos = self.init_random()
        elif init_type == 'choose':
            self.start_pos, self.goal_pos = (0, 0), (self.rows - 1, self.cols - 1) # step of the player is undone
        
        self.grid.grid_cells[self.start_pos[0]][self.start_pos[1]].is_start = True
        self.grid.grid_cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = True
        
        if self.game_type == 'player':
            self.player = Player(self.grid.grid_cells, self.start_pos, self.TILE)
        elif self.game_type == 'bot':
            if self.algo == 'dfs':
                self.algorithm = Recursive(self.grid.grid_cells, self.start_pos) 
            elif self.algo == 'bfs':
                self.algorithm = BFS(self.grid.grid_cells, self.start_pos)
                
        
        
    def init_random(self):
        start, goal = (0, 0), (0, 0)
        while start == goal:
            start = (random.randrange(self.rows), random.randrange(self.cols))
            goal = (random.randrange(self.rows), random.randrange(self.cols))
        return start, goal
        
    def run_game(self):
        pg.init() 
        # clock = pg.time.Clock() 
        pg.display.set_caption("Maze - Path Finding") 
        
        while True:
            window.fill(light_blue)
            self.maze.draw(window)
            self.handle_move()
            if self.game_type == 'player':
                self.player.draw(window)
                if (self.grid.grid_cells[self.player.y][self.player.x].is_goal == True):
                    time.sleep(1)
                    break
                
            if self.game_type == 'bot':
                if (self.grid.grid_cells[self.algorithm.y][self.algorithm.x].is_goal == True):
                    self.draw_last_trace()
                    time.sleep(1)
                    break
                self.algorithm.find_way()
            pg.display.update()
        print("is done")
        self.command = None
        
    def handle_move(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
            if event.type == pg.KEYDOWN:  # Use pygame.KEYDOWN to detect key press
                if self.game_type == 'player':
                    self.player.x_step = 0
                    self.player.y_step = 0
                    if event.key in [pg.K_LEFT, pg.K_a] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['left']:
                        self.player.move(dx=-1)
                    elif event.key in [pg.K_RIGHT, pg.K_d] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['right']:
                        self.player.move(dx=1)
                    elif event.key in [pg.K_UP, pg.K_w] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['top']:
                        self.player.move(dy=-1)
                    elif event.key in [pg.K_DOWN, pg.K_s] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['bottom']:
                        self.player.move(dy=1)
                if event.key in [pg.K_ESCAPE]:
                    self.pause = True
                    self.command = self.esc_menu() # call from child class
                    if self.command == 'get hint':
                        self.get_hint()
                    elif self.command == 'switch algo':
                        self.switch_algo()
    
    def switch_algo(self):
        pass
    
    def draw_last_trace(self):
        if self.game_type == 'player':
            for i in range(self.rows):
                for j in range(self.cols):
                    self.grid.grid_cells[i][j].trace = False
                    self.grid.grid_cells[i][j].visited = False
        self.algorithm.trace_back(self.goal_pos)
        for i in range(1, len(self.algorithm.trace)): # no draw to first cell of path
            self.grid.grid_cells[self.algorithm.trace[i][0]][self.algorithm.trace[i][1]].trace = True
        
        self.maze.draw(window)
        pg.display.update()
    
    def get_hint(self):
                    
        self.algorithm = Recursive(self.grid.grid_cells, (self.player.y, self.player.x))
        while self.grid.grid_cells[self.algorithm.y][self.algorithm.x].is_goal == False:
            self.algorithm.find_way()
        self.draw_last_trace()