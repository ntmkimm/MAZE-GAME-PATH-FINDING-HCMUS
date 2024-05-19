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
background = pg.image.load("pic/bg5.jpg")
background = pg.transform.scale(background, RES)

sub_background = pg.image.load("pic/bg5.jpg")
sub_background = pg.transform.scale(sub_background, RES)

class Game():
    def __init__(self, size, init_type, game_type, algo, sound, character):
        self.rows = size
        self.cols = size
        self.TILE = size_of_maze // size
        self.grid = Grid(self.rows, self.cols)
        self.maze = Maze_Generator(self.grid) 
        self.game_type = game_type
        self.character = character
        self.result = pg.image.load(os.path.join("pic", "result.png"))
        self.set = pg.image.load(os.path.join("pic", "set.png"))
        self.algo = algo
        self.command = None
        self.sound = sound
        self.settings_button = Button(img=self.set, pos_center=(1000, 670), content='', font=font(small_size))
        
        self.pause = False
        self.option = False
        
        self.start_time = 0
        self.elapsed_time = 0
        self.pause_start = 0
        
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
        self.goal = Player(self.grid.grid_cells, (self.rows - 1, self.cols - 1), self.TILE, "End")
        while True:
            window.blit(background, (0, 0))
            self.maze.draw(window, self.background)
            self.player.draw(window)
            self.goal.draw(window)
            if not start_done:
                start_done = self.handle_init_choose(self.player)
            elif not goal_done:
                goal_done = self.handle_init_choose(self.goal)
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
        self.goal = Player(self.grid.grid_cells, self.goal_pos, self.TILE, "End")
        
    def run_game(self):
        pg.init()  
        pg.display.set_caption("Maze - Path Finding") 
        self.start_time = pg.time.get_ticks()
        achieved_goal = False
        animation  = 0
        while True and animation < 40:
            self.draw_game()
            if not achieved_goal:
                self.handle_move()
            if self.game_type == 'player':
                if (self.grid.grid_cells[self.player.y][self.player.x].is_goal == True):
                    if animation == 0:
                        self.goal.disappear()
                        achieved_goal = True
                    animation += 1
            if self.game_type == 'bot':
                if (self.grid.grid_cells[self.algorithm.y][self.algorithm.x].is_goal == True):
                    self.draw_last_trace()
                    pg.display.update()
                    time.sleep(1)
                    break
                self.algorithm.find_way()
            pg.display.update()
        print("is done")
        if self.game_type == 'player':
            self.victory()
        self.command = None
        self.in_game = False
        
    def victory(self):
        pg.display.set_caption("Victory")
        quit_button = Button(img=self.short_bar, pos_center=(550, 700), content="Quit", font=font(small_size))
        continue_button = Button(img=self.short_bar, pos_center=(250, 700), content="Replay", font=font(small_size))
        pg.mixer.music.pause()
        
        while True:
            self.draw_game()
            
            title, title_rect, shader_title, shader_title_rect = shader_text("GAME OVER", font(150, font='game_over.ttf'), (400, 130), purple, yellow)
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)
            
            title1, title_rect1, shader_title1, shader_title_rect1 = shader_text("YOU WON!", font(100, font='game_over.ttf'), (400, 230), purple, yellow)
            window.blit(shader_title1, shader_title_rect1)
            window.blit(title1, title_rect1)
            mouse_pos = pg.mouse.get_pos()

            if self.s % 2 == 0 or self.s % 3 == 0 or self.s % 4 == 0 or self.s % 5 == 0:
                window.blit(pg.transform.scale(self.vic, (580, 280)), (120, 300))
                self.s += 1
            else:
                window.blit(pg.transform.scale(self.vic1, (580, 280)), (120, 300))
                self.s += 1
            
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.sound.sound_select([continue_button])
                    if continue_button.is_pointed(mouse_pos):
                        self.grid.grid_cells[self.start_pos[0]][self.start_pos[1]].is_start = False
                        self.grid.grid_cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = False
                        for i in range(self.rows):
                            for j in range(self.cols):
                                self.grid.grid_cells[i][j].trace = False
                        self.init_random()
                        self.run_game()
                    if quit_button.is_pointed(mouse_pos):
                        self.all_maps_of_user()
            for button in [continue_button, quit_button]:
                button.update(window)
                button.update_color_line(mouse_pos)
            pg.display.update()
            
        pg.mixer.music.unpause()
        pg.display.update()
        
    def handle_move(self):
        if not self.pause and not self.option:
            current_ticks = pg.time.get_ticks()
            self.elapsed_time = (current_ticks - self.start_time) / 1000  # Elapsed time in seconds
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.sound.sound_select([self.settings_button])
                if self.settings_button.is_pointed(mouse_pos):
                    self.pause = True
                    self.pause_start = pg.time.get_ticks()
                    self.esc_menu()
                    print(self.pause)
                    self.start_time += pg.time.get_ticks() - self.pause_start  
                        # Adjust start time cause we want to update start time due to pause duration
                    
            if event.type == pg.KEYDOWN:  # Use pygame.KEYDOWN to detect key press
                if self.game_type == 'player':
                    self.player.x_step = 0
                    self.player.y_step = 0
                    if event.key in [pg.K_LEFT, pg.K_a] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['left']:
                        self.sound.sound_effect(1)
                        self.player.move(dx=-1)
                        self.player.steps += 1
                    elif event.key in [pg.K_RIGHT, pg.K_d] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['right']:
                        self.sound.sound_effect(1)
                        self.player.move(dx=1)
                        self.player.steps += 1
                    elif event.key in [pg.K_UP, pg.K_w] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['top']:
                        self.sound.sound_effect(1)
                        self.player.move(dy=-1)
                        self.player.steps += 1
                    elif event.key in [pg.K_DOWN, pg.K_s] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['bottom']:
                        self.sound.sound_effect(1)
                        self.player.move(dy=1)
                        self.player.steps += 1
                        
                if event.key in [pg.K_ESCAPE]: 
                    self.pause = True
                    self.pause_start = pg.time.get_ticks()
                    self.esc_menu()
                    self.start_time += pg.time.get_ticks() - self.pause_start  

                    

        self.settings_button.update(window)
        self.settings_button.update_color_line(mouse_pos)
    
    def switch_algo(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.grid_cells[i][j].visited = False
                
        DFS_button = Button(img=self.long_bar, pos_center=(600, 300), content="Algo: DFS", font=font(small_size))
        BFS_button = Button(img=self.long_bar, pos_center=(600, 450), content="Algo: BFS", font=font(small_size))
        while self.switch_algo_bool:
            
            self.maze.draw(window, self.background)
            self.player.draw(window)
            self.goal.draw(window)
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
                        self.switch_algo_bool = False
                        
                    elif BFS_button.is_pointed(mouse_pos):
                        self.algo = 'bfs'
                        self.algorithm = BFS(self.grid.grid_cells, self.start_pos)
                        self.switch_algo_bool = False
            
            pg.display.update()
    
    def draw_last_trace(self):
        self.algorithm.trace_back()
        self.maze.draw(window, background)
        self.player.draw(window)
    
    def get_hint(self):
        self.algorithm = BFS(self.grid.grid_cells, (self.player.y, self.player.x))
        
        while self.grid.grid_cells[self.algorithm.y][self.algorithm.x].is_goal == False:
            self.algorithm.find_way()
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.grid_cells[i][j].trace = False
                self.grid.grid_cells[i][j].visited = False
        self.draw_last_trace()
        
    def draw_game(self):
        window.blit(background, (0, 0))
        self.maze.draw(window, self.background)
        self.player.draw(window)
        self.goal.draw(window)
        window.blit(pg.transform.scale(self.result, (340, 400)), (830, 170))
        title, title_rect, shader_title, shader_title_rect = shader_text(f"{self.elapsed_time:.1f}s", font(min_size),(1055, 330), white, black)
        title2, title_rect2, shader_title2, shader_title_rect2 = shader_text((str)(self.player.steps), font(min_size), (1050, 430),white, black)
        window.blit(shader_title, shader_title_rect)
        window.blit(title, title_rect)
        window.blit(shader_title2, shader_title_rect2)
        window.blit(title2, title_rect2)