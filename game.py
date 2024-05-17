from maze_generator import *
from player import *
from color import *
from button import *

from recursive import *
from bfs import *

import time
import pygame as pg
import random

RES = WIDTH, HEIGHT = 1200, 820
window = pg.display.set_mode(RES)

class Game():
    def __init__(self, size, init_type, game_type, algo, sound, character, background):
        self.rows = size
        self.cols = size
        self.TILE = size_of_maze // size
        self.grid = Grid(self.rows, self.cols, background)
        self.maze = Maze_Generator(self.grid) 
        self.game_type = game_type
        self.character = character
        self.result = pg.image.load(os.path.join("pic", "result.png"))
        self.set = pg.image.load(os.path.join("pic", "set.png"))
        self.algo = algo
        self.command = None
        self.sound = sound
        self.settings_button = Button(img=self.set, pos_center=(900, 530), content='', font=font(small_size))
        
        self.pause = False
        self.option = False
        
        if init_type == 'random': self.init_random()
        elif init_type == 'choose': self.init_choose()

        if self.game_type == 'bot':
            if self.algo == 'dfs':
                self.algorithm = Recursive(self.grid.grid_cells, self.start_pos) 
            elif self.algo == 'bfs':
                self.algorithm = BFS(self.grid.grid_cells, self.start_pos)
    
    def init_choose(self):
        start_done = False
        goal_done = False
        self.player = Player(self.grid.grid_cells, (0, 0), self.TILE, self.character)
        goal_point = Player(self.grid.grid_cells, (self.rows - 1, self.cols - 1), self.TILE, "End")
        while True:
            window.fill(theme_color)
            self.maze.draw(window)
            self.player.draw(window)
            goal_point.draw_goal(window)
            if not start_done:
                start_done = self.handle_init_choose(self.player)
            elif not goal_done:
                goal_done = self.handle_init_choose(goal_point)
            else: break
            pg.display.update()

        self.grid.grid_cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = True
            
    
    def handle_init_choose(self, character):
        max_x = self.cols - 1
        max_y = self.rows - 1
        for event in pg.event.get():
                if event.type == pg.QUIT: 
                    pg.quit()
                if event.type == pg.KEYDOWN: 
                    character.x_step = 0
                    character.y_step = 0
                    if event.key in [pg.K_LEFT, pg.K_a] \
                    and character.x != 0:
                        character.move(dx=-1)
                    elif event.key in [pg.K_RIGHT, pg.K_d] \
                    and character.x != max_x:
                        character.move(dx=1)
                    elif event.key in [pg.K_UP, pg.K_w] \
                    and character.y != 0:
                        character.move(dy=-1)
                    elif event.key in [pg.K_DOWN, pg.K_s] \
                    and character.y != max_y:
                        character.move(dy=1)
                    if event.key == pg.K_RETURN:
                        if character == self.player:
                            self.start_pos = (character.y, character.x)
                            self.grid.grid_cells[self.start_pos[0]][self.start_pos[1]].is_start = True
                        else:
                            self.goal_pos = (character.y, character.x)
                        return True
                
    def init_random(self):
        start, goal = (0, 0), (0, 0)
        while start == goal:
            start = (random.randrange(self.rows), random.randrange(self.cols))
            goal = (random.randrange(self.rows), random.randrange(self.cols))
        self.start_pos, self.goal_pos = start, goal
        self.grid.grid_cells[start[0]][start[1]].is_start = True
        self.grid.grid_cells[goal[0]][goal[1]].is_goal = True
        self.player = Player(self.grid.grid_cells, self.start_pos, self.TILE, self.character)
        
    def run_game(self):
        pg.init()  
        pg.display.set_caption("Maze - Path Finding") 
        
        while True:
            window.fill(theme_color)
            self.maze.draw(window)
            self.player.draw(window)
            self.handle_move()
            if self.game_type == 'player':
                """ Bảo """
                window.blit(pg.transform.scale(self.result, (340, 400)), (830, 70))
                self.sound.time = (pg.time.get_ticks() - self.sound.start)/1000
                title, title_rect, shader_title, shader_title_rect = shader_text(f"{self.sound.time:.1f}s", font(min_size),(1055, 230), white, black)
                title2, title_rect2, shader_title2, shader_title_rect2 = shader_text((str)(self.sound.steps), font(min_size), (1050, 330),white, black)
                window.blit(shader_title, shader_title_rect)
                window.blit(title, title_rect)
                window.blit(shader_title2, shader_title_rect2)
                window.blit(title2, title_rect2)
                mouse_pos = pg.mouse.get_pos()
                """"""
                if (self.grid.grid_cells[self.player.y][self.player.x].is_goal == True):
                    time.sleep(1)
                    break
                
            if self.game_type == 'bot':
                if (self.grid.grid_cells[self.algorithm.y][self.algorithm.x].is_goal == True):
                    self.draw_last_trace()
                    pg.display.update()
                    time.sleep(1)
                    break
                self.algorithm.find_way()
            pg.display.update()
        print("is done")
        self.command = None
        
    def victory(self):
        pg.display.set_caption("Victory")
        continue_button = Button(img=self.long_bar, pos_center=(600, 700), content="Continue", font=font(small_size))
        run = True
        start = pg.time.get_ticks()
        tim = (int)((pg.time.get_ticks() - start) / 1000)
        pg.mixer.music.pause()
        while tim != 2:
            tim = (int)((pg.time.get_ticks() - start) / 1000)
            window.fill(theme_color)
            window.blit(self.bg_vic, (180, 0))
            title, title_rect, shader_title, shader_title_rect = shader_text("YOU WIN", font(title_size),(580, 230), white, black)
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)
            mouse_pos = pg.mouse.get_pos()

            if self.s % 2 == 0:
                window.blit(self.vic, (120, 300))
                self.s += 1
            else:
                window.blit(self.vic1, (120, 300))
                self.s += 1

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            pg.time.delay(200)
            pg.display.update()

        pg.display.update()
        self.sound.sound_effect(3)
        pg.time.delay(2300)
        run = True
        window.fill(theme_color)
        while run:
            window.blit(self.result1, (350, 0))
            title, title_rect, shader_title, shader_title_rect = shader_text(f"{self.sound.time:.1f}s", font(small_size), (690, 240), white, black)
            title2, title_rect2, shader_title2, shader_title_rect2 = shader_text((str)(self.sound.steps),font(small_size), (650, 390), white,black)
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)
            window.blit(shader_title2, shader_title_rect2)
            window.blit(title2, title_rect2)
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.sound.sound_select([continue_button])
                    if continue_button.is_pointed(mouse_pos):
                        run = False
            continue_button.update(window)
            continue_button.update_color_line(mouse_pos)
            pg.display.update()
        pg.mixer.music.unpause()
        pg.display.update()
        
    def handle_move(self):
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
            if event.type == pg.KEYDOWN:  # Use pygame.KEYDOWN to detect key press
                if self.game_type == 'player':
                    self.player.x_step = 0
                    self.player.y_step = 0
                    if event.key in [pg.K_LEFT, pg.K_a] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['left']:
                        self.sound.sound_effect(1)
                        self.player.move(dx=-1)
                        self.sound.steps += 1
                    elif event.key in [pg.K_RIGHT, pg.K_d] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['right']:
                        self.sound.sound_effect(1)
                        self.player.move(dx=1)
                        self.sound.steps += 1
                    elif event.key in [pg.K_UP, pg.K_w] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['top']:
                        self.sound.sound_effect(1)
                        self.player.move(dy=-1)
                        self.sound.steps += 1
                    elif event.key in [pg.K_DOWN, pg.K_s] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['bottom']:
                        self.sound.sound_effect(1)
                        self.player.move(dy=1)
                        self.sound.steps += 1
                        
                if event.key in [pg.K_ESCAPE]:
                    self.pause = True
                    self.command = self.esc_menu() # call from child class
                    if self.command == 'get hint':
                        self.get_hint()
                    elif self.command == 'switch algo':
                        self.switch_algo()
        self.settings_button.update(window)
        self.settings_button.update_color_line(mouse_pos)
    
    def switch_algo(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.grid_cells[i][j].visited = False
                
        DFS_button = Button(img=self.long_bar, pos_center=(600, 200), content="Algo: DFS", font=font(small_size))
        BFS_button = Button(img=self.long_bar, pos_center=(600, 350), content="Algo: BFS", font=font(small_size))
        run = True
        while run:
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            
            for button in [DFS_button, BFS_button]:
                button.update_color_line(mouse_pos)
                button.update(window)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if DFS_button.is_pointed(mouse_pos):
                        self.algo = 'dfs'
                        self.algorithm = Recursive(self.grid.grid_cells, self.start_pos)
                        run = False
                        break
                    elif BFS_button.is_pointed(mouse_pos):
                        self.algo = 'bfs'
                        self.algorithm = BFS(self.grid.grid_cells, self.start_pos)
                        run = False
                        break
            
            pg.display.update()
    
    def draw_last_trace(self):
        self.algorithm.trace_back()
        self.maze.draw(window)
        self.player.draw(window)
    
    def get_hint(self):
        self.algorithm = Recursive(self.grid.grid_cells, (self.player.y, self.player.x))
        
        while self.grid.grid_cells[self.algorithm.y][self.algorithm.x].is_goal == False:
            self.algorithm.find_way()
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.grid_cells[i][j].trace = False
                self.grid.grid_cells[i][j].visited = False
                
        self.draw_last_trace()