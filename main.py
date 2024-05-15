import pygame as pg
from color import *
from button import *
from ui import *
from maze_generator import *
from player import *
from game import *
from sign import *

pg.init()

class Menu(Game):
    def __init__(self):
        self.short_bar = pg.image.load("short_bar.png")
        self.long_bar = pg.image.load("long_bar.png")
        self.game_type = 'player'
        self.input_img = pg.image.load("sign.png")
    
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
        self.algo_mode = 0
        
        title, title_rect, shader_title, shader_title_rect = shader_text("Create New Map", font(big_size), (600, 70), white, black)
        
        # button
        cancel_button = Button(img=self.short_bar, pos_center=(900, 700), content='Cancel', font=font(small_size))
        create_new_button = Button(img=self.long_bar, pos_center=(400, 700), content="Create New Map", font=font(small_size))
        input_name_button = Input_Button(img=self.input_img, pos_center=(600, 200), content='', font=font(tiny_size))
        
        easy_button = Button(img=self.long_bar, pos_center=(600, 500), content="Easy: 20x20", font=font(small_size))
        normal_button = Button(img=self.long_bar, pos_center=(600, 500), content="Normal: 40x40", font=font(small_size))
        hard_button = Button(img=self.long_bar, pos_center=(600, 500), content="Hard: 100x100", font=font(small_size))
        
        DFS_button = Button(img=self.long_bar, pos_center=(600, 200), content="Algo: DFS", font=font(small_size))
        BFS_button = Button(img=self.long_bar, pos_center=(600, 200), content="Algo: BFS", font=font(small_size))
        
        random_button = Button(img=self.long_bar, pos_center=(600, 350), content="Init: Random", font=font(small_size))
        choose_button = Button(img=self.long_bar, pos_center=(600, 350), content="Init: Choose", font=font(small_size))
        
        mode_button = [easy_button, normal_button, hard_button]
        init_button = [random_button, choose_button]
        algo_button = [DFS_button, BFS_button]
        
        type_name, type_name_rect = get_text(content='Type name of word', font=font(tiny_size), pos_center=(600, 150), color=black)
            
        while True:
            window.fill(light_blue)
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            
            if self.game_type == 'player':
                buttons = [cancel_button, create_new_button, mode_button[self.size_mode], init_button[self.init_mode], input_name_button]
            elif self.game_type == 'bot':
                buttons = [cancel_button, create_new_button, mode_button[self.size_mode], init_button[self.init_mode], algo_button[self.algo_mode]] 
            
            for button in buttons:
                button.update_color_line(mouse_pos)
                button.update(window)
            
            # title
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)
            if self.game_type == 'player':
                window.blit(type_name, type_name_rect)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_name_button.is_pointed(mouse_pos) and self.game_type == 'player':
                        input_name_button.active = True
                        
                    elif cancel_button.is_pointed(mouse_pos):
                        if self.game_type == 'player':
                            self.all_maps_of_user()
                        elif self.game_type == 'bot':
                            self.main_menu()
                    
                    elif mode_button[self.size_mode].is_pointed(mouse_pos):
                        self.size_mode = (self.size_mode + 1) % 3
                        pg.display.update()
                    elif algo_button[self.algo_mode].is_pointed(mouse_pos) and self.game_type == 'bot':
                        self.algo_mode = (self.algo_mode + 1) % 2
                        pg.display.update()
                    elif init_button[self.init_mode].is_pointed(mouse_pos):
                        self.init_mode = (self.init_mode + 1) % 2
                        pg.display.update()
                    elif create_new_button.is_pointed(mouse_pos):
                        if self.size_mode == 0:     self.size = 20
                        elif self.size_mode == 1:   self.size = 40
                        elif self.size_mode == 2:   self.size = 100
                        
                        if self.init_mode == 0:      self.init = 'random'
                        elif self.init_mode == 1:    self.init = 'choose'
                        
                        if self.algo_mode == 0:      self.algo = 'dfs'
                        elif self.algo_mode == 1:    self.algo = 'bfs'

                        Game.__init__(self, self.size, self.init, self.game_type, self.algo)
                        self.run_game()
                        
                if event.type == pg.KEYDOWN and self.game_type == 'player':
                    if event.key == pg.K_BACKSPACE:
                        if input_name_button.active:
                            input_name_button.input = input_name_button.input[:-1]
                    else:
                        if input_name_button.active and len(input_name_button.input) <= 36:
                            input_name_button.input += event.unicode
            
            if self.game_type == 'player':
                input_name_button.draw()
            
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
        
        play_button = Button(img=self.long_bar, pos_center=(600, 300), content="PLAY", font=font(normal_size))
        bot_button = Button(img=self.long_bar, pos_center=(600, 450), content="BOT", font=font(normal_size))
        options_button = Button(img=self.short_bar, pos_center=(450, 600), content="OPTIONS", font=font(small_size))
        quit_button = Button(img=self.short_bar, pos_center=(750, 600), content="QUIT", font=font(small_size))
        
        while True:
            
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
        
    def sign_up_menu(self):
        
        name = Input_Button(img=self.input_img, pos_center=(600, 200), content='', font=font(tiny_size))
        password = Input_Button(img=self.input_img, pos_center=(600, 350), content='', font=font(tiny_size), hide=True)
        re_password = Input_Button(img=self.input_img, pos_center=(600, 500), content='', font=font(tiny_size), hide=True)
        
        note, note_rect = get_text("Already have an account. ", font=font(tiny_size), pos_center=(540, 750), color=black)
        sign_in, sign_in_rect = get_text('Sign in', font=font(tiny_size), pos_center=(780, 750), color=red)
        
        sign_up_button = Button(img=self.short_bar, pos_center=(600, 650), content='SIGN UP', font=font(small_size))

        name_text, name_rect = get_text('Username', font=font(32), pos_center=(600, 130), color=black)
        pass_text, pass_rect = get_text('Password', font=font(32), pos_center=(600, 280), color=black)
        re_pass_text, re_pass_rect = get_text('Re_password', font=font(32), pos_center=(600, 430), color=black)
        text_return = ''
        
        while True:
            
            window.fill(white)
            window.blit(name_text, name_rect)
            window.blit(pass_text, pass_rect)
            window.blit(re_pass_text, re_pass_rect)
            window.blit(sign_in, sign_in_rect)
            window.blit(note, note_rect)
            
            mouse_pos = pg.mouse.get_pos()
            
            for button in [name, password, re_password, sign_up_button]:
                button.update_color_line(mouse_pos)
                button.update(window)
            
            for event in pg.event.get():
                if sign_in_rect.collidepoint(mouse_pos):
                    sign_in, sign_in_rect = get_text('Sign in', font=font(tiny_size), pos_center=(780, 750), color=dark_blue)
                else:
                    sign_in, sign_in_rect = get_text('Sign in', font=font(tiny_size), pos_center=(780, 750), color=red)
                    
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if name.is_pointed(mouse_pos):
                        name.active = True
                        password.active = False
                        re_password.active = False
                    if password.is_pointed(mouse_pos):
                        name.active = False
                        password.active = True
                        re_password.active = False
                    if re_password.is_pointed(mouse_pos):
                        name.active = False
                        password.active = False
                        re_password.active = True
                    if sign_up_button.is_pointed(mouse_pos):
                        text_return = sign_up(name.input, password.input, re_password.input)
                    if sign_in_rect.collidepoint(mouse_pos):
                        self.sign_in_menu()
                        
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        if name.active:
                            name.input = name.input[:-1]
                        if password.active:
                            password.input = password.input[:-1]
                        if re_password.active:
                            re_password.input = re_password.input[:-1]
                    else:
                        if name.active and len(name.input) <= 36:
                            name.input += event.unicode
                        if password.active and len(password.input) <= 36:
                            password.input += event.unicode
                        if re_password.active and len(re_password.input) <= 36:
                            re_password.input += event.unicode
            
            text_surface, text_surface_rect = get_text(content=text_return, font=font(tiny_size), pos_center=(600, 560), color=black)
            window.blit(text_surface, text_surface_rect)
            
            name.draw()
            password.draw()
            re_password.draw()
            pg.display.update()
            
            if text_return == 'registered successfully':
                self.sign_in_menu()

    def sign_in_menu(self):
        name = Input_Button(img=self.input_img, pos_center=(600, 270), content='', font=font(tiny_size))
        password = Input_Button(img=self.input_img, pos_center=(600, 420), content='', font=font(tiny_size), hide=True)
        sign_in_button = Button(img=self.short_bar, pos_center=(600, 580), content='SIGN IN', font=font(small_size))
        
        note, note_rect = get_text("Don't have an account. ", font=font(tiny_size), pos_center=(540, 680), color=black)
        sign_up, sign_up_rect = get_text('Sign up', font=font(tiny_size), pos_center=(760, 680), color=red)
        
        name_text, name_rect = get_text('Username', font=font(small_size), pos_center=(600, 200), color=black)
        pass_text, pass_rect = get_text('Password', font=font(small_size), pos_center=(600, 350), color=black)
        text_return = ''
        
        while True:
            window.fill(white)
            window.blit(name_text, name_rect)
            window.blit(pass_text, pass_rect)
            window.blit(sign_up, sign_up_rect)
            window.blit(note, note_rect)
            
            mouse_pos = pg.mouse.get_pos()
            
            for button in [name, password, sign_in_button]:
                    button.update_color_line(mouse_pos)
                    button.update(window)
                
            for event in pg.event.get():
                    if sign_up_rect.collidepoint(mouse_pos):
                        sign_up, sign_up_rect = get_text('Sign up', font=font(tiny_size), pos_center=(760, 680), color=dark_blue)
                    else:
                        sign_up, sign_up_rect = get_text('Sign up', font=font(tiny_size), pos_center=(760, 680), color=red)
                    if event.type == pg.QUIT:
                        pg.quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if name.is_pointed(mouse_pos):
                            name.active = True
                            password.active = False
                        if password.is_pointed(mouse_pos):
                            name.active = False
                            password.active = True
                        if sign_in_button.is_pointed(mouse_pos):
                            text_return = sign_in(name.input, password.input)
                        if sign_up_rect.collidepoint(mouse_pos):
                            self.sign_up_menu()
                            
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            if name.active:
                                name.input = name.input[:-1]
                            if password.active:
                                password.input = password.input[:-1]
                        else:
                            if name.active and len(name.input) <= 36:
                                name.input += event.unicode
                            if password.active and len(password.input) <= 36:
                                password.input += event.unicode
            
            text_surface, text_surface_rect = get_text(content=text_return, font=font(tiny_size), pos_center=(600, 490), color=black)
            window.blit(text_surface, text_surface_rect)
                
            name.draw()
            password.draw()
            pg.display.update()
            
            if text_return == 'login successfull':
                pg.display.update()
                time.sleep(2)
                self.main_menu()
            
if __name__ == "__main__":
    menu = Menu()
    menu.create_new_map()