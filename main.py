import pygame as pg
from color import *
from button import *
from ui import *
from maze_generator import *
from player import *
from game import *

pg.init()

class Menu(Game):
    def __init__(self):
        self.short_bar = pg.image.load("short_bar.png")
        self.long_bar = pg.image.load("long_bar.png")
        self.game_type = 'player'
        
    def esc_menu(self):
        back_to_game_button = Button(img=self.long_bar, pos_center=(600, 250), content='Back to Game', font=font(small_size))
        options_button = Button(img=self.short_bar, pos_center=(450, 550), content='Options', font=font(small_size))
        quit_button = Button(img=self.short_bar, pos_center=(750, 550), content="Quit", font=font(small_size))

        if self.game_type == 'player':
            algo_button = Button(img=self.long_bar, pos_center=(600, 400), content='Hint to Goal', font=font(small_size))
        elif self.game_type == 'bot':
            algo_button = Button(img=self.long_bar, pos_center=(600, 400), content='Other Algorithm', font=font(small_size))
        
        
        while self.pause:
            # mouse_pos     
            mouse_pos = pg.mouse.get_pos()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if quit_button.is_pointed(mouse_pos):
                        self.pause = False
                        self.main_menu()
                    elif options_button.is_pointed(mouse_pos):
                        self.pause = False
                        self.options()
                    elif back_to_game_button.is_pointed(mouse_pos):
                        self.pause = False

                    elif algo_button.is_pointed(mouse_pos):
                        if self.game_type == 'player':
                            self.pause = False
                            return 'get hint'
                        elif self.game_type == 'bot':
                            self.pause = False
                            return 'switch algo'
                        
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause = False        
        
            for button in [back_to_game_button, options_button, quit_button, algo_button]:
                button.update_color_line(mouse_pos)
                button.update(window)
                        
            pg.display.update()
        
    def create_new_map(self):
        pg.display.set_caption("Choose size map")
        self.size_mode = 0
        self.init_mode = 0
        
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
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if cancel_button.is_pointed(mouse_pos):
                        if self.game_type == 'player':
                            self.all_maps_of_user()
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

                        Game.__init__(self, self.size, self.init, self.game_type)
                        self.run_game()
                    
                        
            for button in [cancel_button, create_new_button, mode_button[self.size_mode], init_button[self.init_mode]]:
                button.update_color_line(mouse_pos)
                button.update(window)
                        
            pg.display.update()

    def all_maps_of_user(self):
        pg.display.set_caption("Play")
        
        back_button = Button(img=self.short_bar, pos_center=(900, 700), content='Back', font=font(small_size))
        new_map_button = Button(img=self.long_bar, pos_center=(400, 700), content="Create New Map", font=font(small_size))
        
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
        
        play_button = Button(img=self.long_bar, pos_center=(600, 300), content="PLAY", font=font(normal_size))
        bot_button = Button(img=self.long_bar, pos_center=(600, 450), content="BOT", font=font(normal_size))
        options_button = Button(img=self.short_bar, pos_center=(450, 600), content="OPTIONS", font=font(small_size))
        quit_button = Button(img=self.short_bar, pos_center=(750, 600), content="QUIT", font=font(small_size))
        
        while True:
            for event in pg.event.get():
                    if event.type == pg.QUIT: 
                        pg.quit()
                        break
            
            window.fill(light_blue)
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            # button
            menu, menu_rect, shader_menu, shader_menu_rect = shader_text("MAZESOLVE", font(100), pos_center=(600, 100), color=white, color_shader=black)
            
            window.blit(shader_menu, shader_menu_rect)
            window.blit(menu, menu_rect)
            
            for button in [play_button, bot_button, options_button, quit_button]:
                button.update_color_line(mouse_pos)
                button.update(window)
                
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_button.is_pointed(mouse_pos):
                        self.game_type = 'player'
                        self.all_maps_of_user()
                    if bot_button.is_pointed(mouse_pos):
                        self.game_type = 'bot'
                        self.create_new_map()
                    if options_button.is_pointed(mouse_pos):
                        self.options()
                    if quit_button.is_pointed(mouse_pos):
                        pg.quit()
            pg.display.update()
        
# if __name__ == "__main__":
#     menu = Menu()
#     menu.main_menu()