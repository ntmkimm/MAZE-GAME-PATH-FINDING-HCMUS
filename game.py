from maze_generator import *
from player import *
from color import *
from sound import *
from recursive import *
# from main import *
import time
import pygame as pg
import random


window = pg.display.set_mode((1200, 820))

class Game():
    def __init__(self, size, init_type, game_type, sound, character, background):
        self.rows = size
        self.cols = size
        self.TILE = size_of_maze // size
        self.grid = Grid(self.rows, self.cols, background)
        self.maze = Maze_Generator(self.grid) 
        self.game_type = game_type
        self.character = character
        self.result = pg.image.load(os.path.join("pic", "result.png"))
        self.set = pg.image.load(os.path.join("pic", "set.png"))
        self.trace = []
        self.sound = sound
        self.settings_button = Button(img=self.set, pos_center=(900, 530), content='', font=font(small_size))
        self.pause = False
        self.option = False

        if init_type == 'random':
            self.start_pos, self.goal_pos = self.init_random()
        elif init_type == 'choose':
            self.start_pos, self.goal_pos = (0, 0), (self.rows - 1, self.cols - 1) # step of the player is undone
        
        self.grid.grid_cells[self.start_pos[0]][self.start_pos[1]].is_start = True
        self.grid.grid_cells[self.goal_pos[0]][self.goal_pos[1]].is_goal = True
        
        if self.game_type == 'player':
            self.player = Player(self.grid.grid_cells, self.start_pos, self.TILE, self.character)
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
        self.sound.start = pg.time.get_ticks()
        
        while True:
            window.fill(light_blue)
            if self.game_type == 'player':
                window.blit(pg.transform.scale(self.result, (340, 400)), (830, 70))
                self.sound.time = (pg.time.get_ticks() - self.sound.start)/1000
                title, title_rect, shader_title, shader_title_rect = shader_text(f"{self.sound.time:.1f}s", font(min_size),(1055, 230), white, black)
                title2, title_rect2, shader_title2, shader_title_rect2 = shader_text((str)(self.sound.steps), font(min_size), (1050, 330),white, black)
                window.blit(shader_title, shader_title_rect)
                window.blit(title, title_rect)
                window.blit(shader_title2, shader_title_rect2)
                window.blit(title2, title_rect2)
                mouse_pos = pg.mouse.get_pos()
                if (self.grid.grid_cells[self.player.y][self.player.x].is_goal == True):
                    time.sleep(1)
                    break
                self.loop()

            elif self.game_type == 'bot':
                if (self.grid.grid_cells[self.recursive.y][self.recursive.x].is_goal == True):
                    self.draw_last_trace()
                    time.sleep(1)
                    break
                self.loop_bot()
        print("is done")

    def loop(self):
        self.maze.draw(window)
        self.handle_move()
        self.player.update_player()
        self.player.draw(window)
        pg.display.update()

        
    def handle_move(self):
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.sound.sound_select([self.settings_button])
                if self.settings_button.is_pointed(mouse_pos):
                    self.pause = True
                    self.esc_menu()
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
                    self.esc_menu() # call from child class
        self.settings_button.update(window)
        self.settings_button.update_color_line(mouse_pos)


    
    def draw_last_trace(self):
        if self.game_type == 'bot':
            for i in range(len(self.trace)):
                self.grid.grid_cells[self.trace[i][0]][self.trace[i][1]].trace = True
        
        self.maze.draw(window)
        pg.display.update()
        
    def loop_bot(self):
        self.maze.draw(window)
        self.recursive.find_way(self.trace, self.start_pos)
        self.handle_move()
        pg.display.update()