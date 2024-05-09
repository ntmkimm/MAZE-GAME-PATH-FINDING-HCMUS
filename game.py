from maze_generator import *
from player import *
from color import *

from recursive import *
# from main import *
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
            self.recursive = Recursive(self.grid.grid_cells, self.start_pos) 
        
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
            if self.game_type == 'player':
                if (self.grid.grid_cells[self.player.y][self.player.x].is_goal == True):
                    time.sleep(1)
                    break
                self.loop()
            elif self.game_type == 'bot':
                if (self.grid.grid_cells[self.recursive.y][self.recursive.x].is_goal == True):
                    self.draw_last_trace()
                    time.sleep(1)
                    break
                self.loop_bot(self.start_pos)

        print("is done")

    def loop(self):
        self.maze.draw(window)
        self.handle_move()
        self.player.update_player()
        self.player.draw(window)
        pg.display.update()
        
    def loop_bot(self, cur_pos):
        self.maze.draw(window)
        self.recursive.find_way(self.trace, cur_pos)
        self.handle_move()
        pg.display.update()
        
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
                    command = self.esc_menu() # call from child class
                    if command == 'get hint':
                        self.recursive = Recursive(self.grid.grid_cells, (self.player.y, self.player.x))
                        self.loop_bot((self.player.y, self.player.x))
                    elif command == 'switch algo':
                        self.switch_algo()
    
    def switch_algo(self):
        pass
    
    def draw_last_trace(self):
        for i in range(len(self.trace)):
            self.grid.grid_cells[self.trace[i][0]][self.trace[i][1]].trace = True
        
        self.maze.draw(window)
        pg.display.update()