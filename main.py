import pygame as pg
from color import *
from button import *
from ui import *
from maze_generator import *
from player import *
from game import *

pg.init()

class Menu():
    def __init__(self, window):
        self.short_bar = pg.image.load("short_bar.png")
        self.long_bar = pg.image.load("long_bar.png")
        self.game_type = 'player'
        
    def create_new_map(self):
        pg.display.set_caption("Choose size map")
        self.size_mode = 0
        self.init_mode = 0
        
        while True:
            window.fill(light_blue)
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            # title
            title, title_rect, shader_title, shader_title_rect = shader_text("Create New Map", font(big_size), (600, 50), white, black)
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)

            # type name of world
            # box_type_name = pg.Rect(, 100, 1200, 500)
            # pg.draw.rect(window, white, box_of_created_map)
            # pg.draw.line(window, black, (0, box_of_created_map.top), (1200, box_of_created_map.top), 10)
            # pg.draw.line(window, black, (0, box_of_created_map.bottom), (1200, box_of_created_map.bottom), 10)
            
            # button
            cancel_button = Button(img=self.short_bar, pos_center=(900, 700), content='Cancel', font=font(small_size))
            create_new_button = Button(img=self.long_bar, pos_center=(400, 700), content="Create New Map", font=font(small_size))
            
            easy_button = Button(img=self.long_bar, pos_center=(600, 500), content="Easy: 20x20", font=font(small_size))
            normal_button = Button(img=self.long_bar, pos_center=(600, 500), content="Normal: 40x40", font=font(small_size))
            hard_button = Button(img=self.long_bar, pos_center=(600, 500), content="Hard: 100x100", font=font(small_size))
            
            random_button = Button(img=self.long_bar, pos_center=(600, 350), content="Init: Random", font=font(small_size))
            choose_button = Button(img=self.long_bar, pos_center=(600, 350), content="Init: Choose", font=font(small_size))
                        
            mode_button = [easy_button, normal_button, hard_button]
            init_button = [random_button, choose_button]
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if cancel_button.is_pointed(mouse_pos):
                        if self.game_type == 'player':
                            self.all_maps_of_user(window)
                        elif self.game_type == 'bot':
                            self.main_menu()
                    if mode_button[self.size_mode].is_pointed(mouse_pos):
                        self.size_mode = (self.size_mode + 1) % 3
                        
                    if init_button[self.init_mode].is_pointed(mouse_pos):
                        self.init_mode = (self.init_mode + 1) % 2
                        
                    if create_new_button.is_pointed(mouse_pos):
                        if self.size_mode == 0:     self.size = 20
                        elif self.size_mode == 1:   self.size = 40
                        elif self.size_mode == 2:   self.size = 100
                        
                        if self.init_mode == 0:      self.init = 'random'
                        elif self.init_mode == 1:    self.init = 'choose'

                        game = Game(self.size, self.init, self.game_type)
                        game.run_game(window)
                    
                        
            for button in [cancel_button, create_new_button, mode_button[self.size_mode], init_button[self.init_mode]]:
                button.update_color_line(mouse_pos)
                button.update(window)
                        
            pg.display.update()

    def all_maps_of_user(self, window):
        pg.display.set_caption("Play")
        while True:
            # theme
            window.fill(light_blue)
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            # title
            title, title_rect, shader_title, shader_title_rect = shader_text("Select Map", font(big_size), (600, 50), white, black)
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)
            # created_map
            box_of_created_map = pg.Rect(0, 100, 1200, 500)
            pg.draw.rect(window, white, box_of_created_map)
            pg.draw.line(window, black, (0, box_of_created_map.top), (1200, box_of_created_map.top), 10)
            pg.draw.line(window, black, (0, box_of_created_map.bottom), (1200, box_of_created_map.bottom), 10)
            # button
            back_button = Button(img=self.short_bar, pos_center=(900, 700), content='Back', font=font(small_size))
            new_map_button = Button(img=self.long_bar, pos_center=(400, 700), content="Create New Map", font=font(small_size))
            
            for button in [back_button, new_map_button]:
                button.update_color_line(mouse_pos)
                button.update(window)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back_button.is_pointed(mouse_pos):
                        self.main_menu()
                    if new_map_button.is_pointed(mouse_pos):
                        self.create_new_map()
                
            pg.display.update()
                    
        
    def options(self):
        pass

    def main_menu(self):
        pg.display.set_caption("Menu")
        short_bar = pg.image.load("short_bar.png")
        long_bar = pg.image.load("long_bar.png")
        # window.fill()
        while True:
            for event in pg.event.get():
                    if event.type == pg.QUIT: 
                        pg.quit()
                        break
            
            window.fill(light_blue)
            mouse_pos = pg.mouse.get_pos()
            menu, menu_rect, shader_menu, shader_menu_rect = shader_text("MAZESOLVE", font(100), pos_center=(600, 100), color=white, color_shader=black)
            PLAY_BUTTON = Button(img=self.long_bar, pos_center=(600, 300), content="PLAY", font=font(normal_size))
            BOT_BUTTON = Button(img=self.long_bar, pos_center=(600, 450), content="BOT", font=font(normal_size))
            OPTIONS_BUTTON = Button(img=self.short_bar, pos_center=(450, 600), content="OPTIONS", font=font(small_size))
            QUIT_BUTTON = Button(img=self.short_bar, pos_center=(750, 600), content="QUIT", font=font(small_size))
            
            window.blit(shader_menu, shader_menu_rect)
            window.blit(menu, menu_rect)
            
            for button in [PLAY_BUTTON, BOT_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.update_color_line(mouse_pos)
                button.update(window)
                
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.is_pointed(mouse_pos):
                        self.game_type = 'player'
                        self.all_maps_of_user(window)
                    if BOT_BUTTON.is_pointed(mouse_pos):
                        self.game_type = 'bot'
                        self.create_new_map()
                    if OPTIONS_BUTTON.is_pointed(mouse_pos):
                        self.options()
                    if QUIT_BUTTON.is_pointed(mouse_pos):
                        pg.quit()
            pg.display.update()
        
        
if __name__ == "__main__":
    menu = Menu(window)
    menu.main_menu()
            