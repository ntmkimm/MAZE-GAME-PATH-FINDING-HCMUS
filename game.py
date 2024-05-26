from maze_generator import *
from player import *
from color import *
from button import *
from save_load import *

from recursive import *
from bfs import *

import pygame as pg
import pandas as pd
import random

RES = WIDTH, HEIGHT = 1200, 820
window = pg.display.set_mode(RES)
background = pg.image.load("pic/bg5.jpg")
background = pg.transform.scale(background, RES)

class Game():
    def __init__(self, size, init_type, game_type, algo, sound, character, game_name):
        self.result = pg.image.load(os.path.join("pic", "result.png"))
        self.set = pg.image.load(os.path.join("pic", "set.png"))
        self.game_type = game_type
        self.command = None
        self.sound = sound
        self.pause = False
        self.option = False
        self.game_name = game_name
        self.start_time = 0
        self.elapsed_time = 0
        self.pause_start = 0
        self.add_time = 0
        
        if init_type != 'load': 
            self.rows = size
            self.cols = size
            self.TILE = size_of_maze // size
            self.grid = Grid(self.rows, self.cols)
            self.maze = Maze_Generator(self.grid) 
            self.character = character
            self.algo = algo
            self.steps = 0
            
            if init_type == 'random': self.init_random()
            elif init_type == 'choose': self.init_choose()
            
            if self.game_type == 'bot':
                if self.algo == 'dfs':
                    self.algorithm = Recursive(self.grid.cells, self.start_pos) 
                elif self.algo == 'bfs':
                    self.algorithm = BFS(self.grid.cells, self.start_pos)
                    
        elif init_type == 'load':
            data = self.file_manager.load(self.game_name)
            self.rows = self.cols = data["size"]
            self.grid = Grid(self.rows, self.cols)
            self.maze = Maze_Generator(self.grid, type='load')
            self.TILE = size_of_maze // data["size"]
            self.character = data["character"]
            self.background = data["background"]
            self.add_time = data["elapsed_time"]
            self.start_pos = data["start_pos"]
            self.goal_pos = data["goal_pos"]
            
            for index in range(len(data["grid_cells"])): 
                y, x = index // self.rows, index % self.cols
                self.grid.cells[y][x].bars = data["grid_cells"][str(index)]
                self.grid.cells[y][x].seen = True
            
            self.player = Player(self.grid.cells, data["cur_pos"], self.TILE, self.character)
            self.goal = Player(self.grid.cells, self.goal_pos, self.TILE, "End")
            self.steps = data["steps"]
            
            self.grid.cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = True
            self.grid.cells[self.start_pos[0]][self.start_pos[1]].is_start = True
    
    def init_choose(self):
        start_done = False
        goal_done = False
        self.player = Player(self.grid.cells, (0, 0), self.TILE, self.character)
        self.goal = Player(self.grid.cells, (self.rows - 1, self.cols - 1), self.TILE, "End")
        
        flag = False
        while True:
            window.blit(background, (0, 0))
            self.maze.draw(window, self.background)
            self.player.draw(window)
            self.goal.draw(window)
            
            box = pg.Rect(825, 680, 360, 80)
            pg.draw.rect(window, purple, box)
            pg.draw.line(window, yellow, (box.left, box.top), (box.right, box.top), 5)
            pg.draw.line(window, yellow, (box.left, box.bottom), (box.right, box.bottom), 5)
            text_surface, text_surface_rect = get_text(content="Choose Init Places", font=font(tiny_size), pos_center=(1005, 700))
            window.blit(text_surface, text_surface_rect)
            text_surface1, text_surface_rect1 = get_text(content="Using Keys To Move", font=font(tiny_size), pos_center=(1005, 720))
            window.blit(text_surface1, text_surface_rect1)
            text_surface2, text_surface_rect2 = get_text(content="Press Enter To Choose", font=font(tiny_size), pos_center=(1005, 740))
            window.blit(text_surface2, text_surface_rect2)
            if flag:
                now = pg.time.get_ticks()
                if now - start <= 1500:
                    title, title_rect, shader_title, shader_title_rect = shader_text("Choose Again!", font(big_size), (600, 400), white, purple)
                    window.blit(shader_title, shader_title_rect)
                    window.blit(title, title_rect)
                else: flag = False
                    
            if not start_done:
                start_done = self.handle_init_choose(self.player)
            elif not goal_done:
                goal_done = self.handle_init_choose(self.goal)
            else:
                if self.check_exist_way(self.start_pos): break
                else:
                    flag = True
                    start = pg.time.get_ticks()
                    self.grid.cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = False
                    self.grid.cells[self.start_pos[0]][self.start_pos[1]].is_start = False
                    start_done = False
                    goal_done = False
            pg.display.update()

        self.grid.cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = True        
    
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
                            self.grid.cells[self.start_pos[0]][self.start_pos[1]].is_start = True
                        else:
                            self.goal_pos = (character.y, character.x)
                            self.grid.cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = True
                        return True

    def check_exist_way(self, start):
            solve = BFS(self.grid.cells, start)
            while solve.result.head is not None and solve.result.tail is not None:
                solve.find_way()
            for i in range(self.rows):
                for j in range(self.cols):
                    self.grid.cells[i][j].visited = False
            if solve.trace == [] or solve.trace == None: return False
            return True
    
    def init_random(self):
        start, goal = (0, 0), (0, 0)
        animation = 0
        box = pg.Rect(825, 680, 360, 80)
        while animation < 100:
            start = (random.randrange(self.rows), random.randrange(self.cols))
            goal = (random.randrange(self.rows), random.randrange(self.cols))
            
            self.goal_pos = goal
            self.grid.cells[goal[0]][goal[1]].is_goal = True

            if self.check_exist_way(start) == True and start != goal: break
            else:
                self.grid.cells[goal[0]][goal[1]].is_goal = False
                pg.draw.rect(window, purple, box)
                pg.draw.line(window, yellow, (box.left, box.top), (box.right, box.top), 5)
                pg.draw.line(window, yellow, (box.left, box.bottom), (box.right, box.bottom), 5)
                if animation % 2 == 0:
                    text_surface, text_surface_rect = get_text(content="Choose Again!", font=font(small_size), pos_center=(1005, 720))
                else:
                    text_surface, text_surface_rect = get_text(content="Choose Again!", font=font(tiny_size), pos_center=(1005, 720))
                window.blit(text_surface, text_surface_rect)
                animation += 1
            
        self.start_pos, self.goal_pos = start, goal
        self.grid.cells[start[0]][start[1]].is_start = True
        self.grid.cells[goal[0]][goal[1]].is_goal = True
        self.player = Player(self.grid.cells, self.start_pos, self.TILE, self.character)
        self.goal = Player(self.grid.cells, self.goal_pos, self.TILE, "End")
        
    def run_game(self):
        pg.init()  
        pg.display.set_caption("Maze - Path Finding") 
        self.start_time = pg.time.get_ticks()
        achieved_goal = False
        animation  = 0
        while True and animation < 5:
            self.draw_game()
            if not achieved_goal:
                self.handle_move()
            if self.game_type == 'player':
                if (self.grid.cells[self.player.y][self.player.x].is_goal == True):
                    if animation == 0:
                        self.goal.disappear()
                        achieved_goal = True
                    animation += 1
            if self.game_type == 'bot':
                if (self.grid.cells[self.algorithm.y][self.algorithm.x].is_goal == True):
                    self.draw_last_trace()
                    if animation == 0:
                        # self.goal.disappear()
                        achieved_goal = True
                    animation += 1
                if not achieved_goal:
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
        self.sound.sound_effect(3)
        self.save_leaderboard()
        self.add_time = 0
        victory = True
        while victory:
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
                        self.grid.cells[self.start_pos[0]][self.start_pos[1]].is_start = False
                        self.grid.cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = False
                        for i in range(self.rows):
                            for j in range(self.cols):
                                self.grid.cells[i][j].trace = False
                        victory = False
                        self.init_random()
                        self.sound.sound3.stop()
                        pg.mixer.music.unpause()
                        self.sound.sound_effect(1)
                        self.steps = 0
                        self.elapsed_time = 0
                        self.run_game()
                    if quit_button.is_pointed(mouse_pos):
                        victory = False
                        self.save_game()
                        self.sound.sound3.stop()
                        if self.sound.background_sound(self.sound.op2):
                            pg.mixer.music.unpause()
                        self.sound.sound_effect(1)
                        self.all_maps_of_user()
            for button in [continue_button, quit_button]:
                button.update(window)
                button.update_color_line(mouse_pos)
            pg.display.update()
            
        self.add_time = 0
        pg.mixer.music.unpause()
            
    def save_game(self):
        grid_cells = {}
        for y in range(self.rows):
            for x in range(self.cols):
                grid_cells[y * self.rows + x] = self.grid.cells[y][x].bars
                
        data_to_save = {
            "character" : self.character,
            "background" : self.background,
            "elapsed_time" : self.elapsed_time,
            "steps" : self.steps,
            "size" : self.rows,
            "start_pos": self.start_pos,
            "goal_pos" : self.goal_pos, 
            "cur_pos" : (self.player.y, self.player.x), 
            "grid_cells" : grid_cells
            }
        
        self.file_manager.save(data_to_save, self.game_name)
        
    def handle_move(self):
        settings_button = Button(img=self.set, pos_center=(1000, 670), content='', font=font(small_size))
        
        if not self.pause and not self.option:
            current_ticks = pg.time.get_ticks()
            self.elapsed_time = (current_ticks - self.start_time) / 1000  + self.add_time
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.sound.sound_select([settings_button])
                if settings_button.is_pointed(mouse_pos):
                    self.pause = True
                    self.pause_start = pg.time.get_ticks()
                    self.esc_menu()
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
                        self.steps += 1
                    if event.key in [pg.K_RIGHT, pg.K_d] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['right']:
                        self.sound.sound_effect(1)
                        self.player.move(dx=1)
                        self.steps += 1
                    if event.key in [pg.K_UP, pg.K_w] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['top']:
                        self.sound.sound_effect(1)
                        self.player.move(dy=-1)
                        self.steps += 1
                    if event.key in [pg.K_DOWN, pg.K_s] \
                    and not self.player.grid_cells[self.player.y][self.player.x].bars['bottom']:
                        self.sound.sound_effect(1)
                        self.player.move(dy=1)
                        self.steps += 1
                elif self.game_type == 'bot':
                    if event.key == pg.K_h:
                        for i in range(self.rows):
                            for j in range(self.cols):
                                self.grid.cells[i][j].visited = False
                        if self.algo == 'bfs':
                            self.algo = 'dfs'
                            self.algorithm = Recursive(self.grid.cells, self.start_pos)
                        elif self.algo == 'dfs':
                            self.algo = 'bfs'
                            self.algorithm = BFS(self.grid.cells, self.start_pos)
                if event.key in [pg.K_ESCAPE]: 
                    self.pause = True
                    self.pause_start = pg.time.get_ticks()
                    self.esc_menu()
                    self.start_time += pg.time.get_ticks() - self.pause_start  

        settings_button.update(window)
        settings_button.update_color_line(mouse_pos)
    
    def switch_algo(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.cells[i][j].visited = False
                
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
                        self.algorithm = Recursive(self.grid.cells, self.start_pos)
                        self.switch_algo_bool = False
                        
                    elif BFS_button.is_pointed(mouse_pos):
                        self.algo = 'bfs'
                        self.algorithm = BFS(self.grid.cells, self.start_pos)
                        self.switch_algo_bool = False
            
            pg.display.update()
    
    def draw_last_trace(self):
        self.algorithm.trace_back()
        self.maze.draw(window, self.background)
        self.player.draw(window)
        self.goal.draw(window)
    
    def get_hint(self):
        self.algorithm = BFS(self.grid.cells, (self.player.y, self.player.x))
        
        while self.grid.cells[self.algorithm.y][self.algorithm.x].is_goal == False:
            self.algorithm.find_way()
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.cells[i][j].trace = False
                self.grid.cells[i][j].visited = False
        self.draw_last_trace()
        
    def draw_game(self):
        window.blit(background, (0, 0))
        self.maze.draw(window, self.background)
        self.player.draw(window)
        self.goal.draw(window)
        window.blit(pg.transform.scale(self.result, (340, 400)), (830, 170))
        title, title_rect, shader_title, shader_title_rect = shader_text(f"{self.elapsed_time:.1f}s", font(min_size),(1055, 330), white, black)
        title2, title_rect2, shader_title2, shader_title_rect2 = shader_text((str)(self.steps), font(min_size), (1050, 430),white, black)
        window.blit(shader_title, shader_title_rect)
        window.blit(title, title_rect)
        window.blit(shader_title2, shader_title_rect2)
        window.blit(title2, title_rect2)
        
        if self.game_type == 'bot':
            if self.algo == 'bfs':
                algo_type = 'BFS'
            elif self.algo == 'dfs':
                algo_type = 'DFS'
                
            algo, algo_r, shade_algo, shade_r = shader_text("Algorithm : " + algo_type, font(tiny_size), (1000, 80), white, black)
            window.blit(shade_algo, shade_r)
            window.blit(algo, algo_r)
            algo, algo_r, shade_algo, shade_r = shader_text("Press H to switch", font(tiny_size), (1000, 130), white, black)
            window.blit(shade_algo, shade_r)
            window.blit(algo, algo_r)
    
    def save_leaderboard(self):
        if self.rows == 20: mode = 'easy'
        elif self.rows == 40: mode = 'medium'
        elif self.rows == 100: mode = 'hard'
        
        df = pd.read_excel(os.path.join('save_data', 'leaderboard' + mode + '.xlsx'))
        new_data = {
            'Tên': self.player_name,
            'Map': self.rows,
            'Steps': self.steps,
            'Time': self.elapsed_time
        }
        existing_row = df[(df['Tên'] == new_data['Tên']) & (df['Map'] == new_data['Map'])]

        if not existing_row.empty:
            if (new_data['Steps'] < existing_row.iloc[0]['Steps']) or \
                    (new_data['Time'] < existing_row.iloc[0]['Time']):
                df.loc[existing_row.index, ['Steps', 'Time']] = new_data['Steps'], new_data['Time']
        else:
            new_row_df = pd.DataFrame([new_data])
            df = pd.concat([df, new_row_df], ignore_index=True)
            
        df.sort_values(by=['Map', 'Steps', 'Time'], ascending=[False, True, True], inplace=True)
        df.to_excel(os.path.join('save_data', 'leaderboard' + mode + '.xlsx'), index=False)