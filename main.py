import pygame as pg
import pandas as pd

from color import *
from button import *
from ui import *
from maze_generator import *
from player import *
from sound import *
import os
from game import *
from sign import *

pg.init()

# manager = SaveLoad(file_extension=".save", save_folder="save_data")

class Menu(Game):
    def __init__(self):
        self.table = pg.image.load(os.path.join("pic", "Table.png"))
        self.back = pg.image.load(os.path.join("pic", "Back.png"))
        self.back = pg.transform.scale(self.back, (64, 64))
        self.short_bar = pg.image.load(os.path.join("pic", "short_bar.png"))
        self.long_bar = pg.image.load(os.path.join("pic", "long_bar.png"))
        self.Background_Sound_X = pg.image.load(os.path.join("pic", "Background_Sound_X.png"))
        self.Background_Sound = pg.image.load(os.path.join("pic", "Background_Sound.png"))
        self.Sound_Effect = pg.image.load(os.path.join("pic", "Sound_Effect.png"))
        self.Sound_Effect_X = pg.image.load(os.path.join("pic", "Sound_Effect_X.png"))
        self.Bar = pg.image.load(os.path.join("pic", "bar.png"))
        self.but = pg.image.load(os.path.join("pic", "but.png"))
        self.temp = pg.image.load(os.path.join("pic", "temp.png"))
        self.vic = pg.image.load(os.path.join("pic", "Victory.png"))
        self.vic1 = pg.image.load(os.path.join("pic", "Victory1.png"))
        self.star_fall = pg.image.load(os.path.join("pic", "star_fall.png"))
        self.star = pg.image.load(os.path.join("pic", "star.png"))
        self.star1 = pg.image.load(os.path.join("pic", "star(1).png"))
        self.top = pg.image.load(os.path.join("pic", "arrow1.png"))
        self.bot = pg.image.load(os.path.join("pic", "arrow2.png"))
        self.cha0_1 = pg.image.load(os.path.join("pic", "jump0.png"))
        self.cha0_2 = pg.image.load(os.path.join("pic", "fall0.png"))
        self.cha1_1 = pg.image.load(os.path.join("pic", "jump1.png"))
        self.cha1_2 = pg.image.load(os.path.join("pic", "fall1.png"))
        self.cha2_1 = pg.image.load(os.path.join("pic", "jump2.png"))
        self.cha2_2 = pg.image.load(os.path.join("pic", "fall2.png"))
        self.cha3_1 = pg.image.load(os.path.join("pic", "jump3.png"))
        self.cha3_2 = pg.image.load(os.path.join("pic", "fall3.png"))
        self.frame = pg.image.load(os.path.join("pic", "frame.png"))
        self.frame_option = pg.image.load(os.path.join("pic", "frame_option.png"))
        self.result1 = pg.image.load(os.path.join("pic", "result.png"))
        self.game_exist_table = pg.image.load(os.path.join("pic", "game_name.png"))
        self.game_type = 'player'
        self.input_img = pg.image.load("sign.png")
        self.sound = Sound()
        self.s = 0
        self.bg = 0
        self.sound.background_sound(0)
        
        self.character = "MaskDude"
        self.background = 'green'
        self.isname = ''

    def esc_menu(self):        
        back_to_game_button = Button(img=self.long_bar, pos_center=(600, 550), content='Back to Game', font=font(small_size))
        options_button = Button(img=self.short_bar, pos_center=(450, 400), content='Options', font=font(small_size))
        quit_button = Button(img=self.short_bar, pos_center=(750, 400), content="Quit", font=font(small_size))
        
        if self.game_type == 'player':
            algo_button = Button(img=self.long_bar, pos_center=(600, 250), content='Hint to Goal', font=font(small_size))
        elif self.game_type == 'bot':
            algo_button = Button(img=self.long_bar, pos_center=(600, 250), content='Other Algorithm', font=font(small_size))
        
        lis = [back_to_game_button, options_button, quit_button, algo_button]
        
        while self.pause:
            # mouse_pos     
            self.draw_game()
            mouse_pos = pg.mouse.get_pos()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    
                    self.sound.sound_select(lis)
                    
                    if quit_button.is_pointed(mouse_pos):
                        self.pause = False
                        if self.game_type == 'bot':
                            self.create_new_map()
                        elif self.game_type == 'player':
                            self.save_game()
                            self.all_maps_of_user()
                    elif options_button.is_pointed(mouse_pos):
                        # self.pause = False
                        self.option = True
                        self.options()
                    elif back_to_game_button.is_pointed(mouse_pos):
                        self.pause = False

                    elif algo_button.is_pointed(mouse_pos):
                        if self.game_type == 'player':
                            self.command = 'get hint'
                            self.pause = False
                            self.get_hint()
                        elif self.game_type == 'bot':
                            self.command = 'switch algo'
                            self.switch_algo_bool = True
                            self.switch_algo()
                        
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
        create_new_button = Button(img=self.short_bar, pos_center=(300, 700), content="Create", font=font(small_size))
        skin_button = Button(img=self.short_bar, pos_center=(600, 700), content='Skin', font=font(small_size))
        input_name_button = Input_Button(img=self.input_img, pos_center=(600, 200), content='', font=font(tiny_size))
        input_name_button.active = True
        
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
        
        type_name, type_name_rect = get_text(content='Type name of new world', font=font(tiny_size), pos_center=(600, 150), color=green)
        
        lis = [cancel_button, create_new_button, easy_button, normal_button, hard_button, random_button, choose_button, DFS_button, BFS_button, skin_button]
        text_return = ''
        while True:
            # window.fill(theme_color)
            self.back_ground()
            self.bg += 1
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            
            if self.game_type == 'player':
                buttons = [cancel_button, create_new_button, mode_button[self.size_mode], init_button[self.init_mode], input_name_button, skin_button]
            elif self.game_type == 'bot':
                buttons = [cancel_button, create_new_button, mode_button[self.size_mode], init_button[self.init_mode], algo_button[self.algo_mode], skin_button] 
            
            for button in buttons:
                button.update_color_line(mouse_pos)
                button.update(window)
            
            # title
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)
            
            if self.game_type == 'player':
                window.blit(type_name, type_name_rect)
                text, text_rect = get_text(text_return, font=font(tiny_size), pos_center=(600, 250))
                window.blit(text, text_rect)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    
                    self.sound.sound_select(lis)
                    
                    if input_name_button.is_pointed(mouse_pos) and self.game_type == 'player':
                        input_name_button.active = True
                        
                    elif cancel_button.is_pointed(mouse_pos):
                        if self.game_type == 'player':
                            self.all_maps_of_user()
                        elif self.game_type == 'bot':
                            self.main_menu()
                    elif skin_button.is_pointed(mouse_pos):
                        self.skin()
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
                        
                        self.sound.sound_select([create_new_button])
                        
                        if self.size_mode == 0:     self.size = 20
                        elif self.size_mode == 1:   self.size = 40
                        elif self.size_mode == 2:   self.size = 100
                        
                        if self.init_mode == 0:      self.init = 'random'
                        elif self.init_mode == 1:    self.init = 'choose'
                        
                        if self.algo_mode == 0:      self.algo = 'dfs'
                        elif self.algo_mode == 1:    self.algo = 'bfs'
                        
                        self.in_game = True
                        self.game_name = input_name_button.input.strip()
                        if self.game_name == '' and self.game_type == 'player':
                            text_return = "world's name is empty!"
                            continue
                        
                        Game.__init__(self, self.size, self.init, self.game_type, \
                                      self.algo, self.sound, self.character, self.game_name)
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
            
    def skin(self):
        
        pg.display.set_caption("Skin")
        
        top_button1 = Button(img=self.top, pos_center=(270, 90), content="", font=font(small_size), corner_radius=10)
        bot_button1 = Button(img=self.bot, pos_center=(270, 580), content="", font=font(small_size), corner_radius=10)
        top_button2 = Button(img=self.top, pos_center=(930, 90), content="", font=font(small_size), corner_radius=10)
        bot_button2 = Button(img=self.bot, pos_center=(930, 580), content="", font=font(small_size), corner_radius=10)
        done_button = Button(img=self.short_bar, pos_center=(600, 550), content="Done", font=font(small_size), corner_radius=10)
        random_button = Button(img=self.short_bar, pos_center=(600, 400), content="Random", font=font(small_size),corner_radius=10)

        lis = [top_button1, bot_button1, done_button, top_button2, bot_button2, random_button]

        run = True
        option1 = 0
        option2 = 0
        temp = 0
        cha_lis = [self.cha0_1, self.cha1_1, self.cha2_1, self.cha3_1, self.cha0_2, self.cha1_2,  self.cha2_2, self.cha3_2]

        name_cha_lis = ["MaskDude", "NinjaFrog", "PinkMan", "VirtualGuy"]
        while run:
            
            self.back_ground()
            self.bg += 1
            window.blit(self.frame, (120, 170))
            window.blit(self.frame, (780, 170))
            mouse_pos = pg.mouse.get_pos()
            if temp % 20 >= 0 and temp % 20 <= 10:
                window.blit(pg.transform.scale(cha_lis[(option1 % 4)], (92, 92)), (220, 290))
                temp += 1
            else:
                window.blit(pg.transform.scale(cha_lis[(option1 % 4 + 4)], (92, 92)), (220, 290))
                temp += 1

            self.background = color[option2 % 7]

            pg.draw.rect(window, black, (894, 296, 72, 72), 3)
            window.blit(bg_lis[self.background], (898, 300))

            self.character = name_cha_lis[(option1 % 4)]
            if self.in_game:
                self.player.SPRITES = load_sprite_sheets("MainCharacters", self.character, 32, 32, size_maze=self.rows)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.sound.sound_select(lis)
                    if done_button.is_pointed(mouse_pos):
                        if self.in_game:
                            run = False
                            break
                        else:
                            self.create_new_map()
                    if top_button1.is_pointed(mouse_pos):
                        option1 += 1
                    if top_button2.is_pointed(mouse_pos):
                        option2 += 1
                    if bot_button1.is_pointed(mouse_pos):
                        option1 -= 1
                    if bot_button2.is_pointed(mouse_pos):
                        option2 -= 1
                    if random_button.is_pointed(mouse_pos):
                        option1 = temp * 1
                        option2 = temp * 1

            for button in lis:
                button.update(window)
                button.update_color_line(mouse_pos)
            pg.display.update()
            
    def back_ground(self):
        window.blit(background, (0, 0))
        temp = self.bg % 1070
        if self.bg % 100 >= 0 and self.bg % 100 <= 40:
            window.blit(self.star1, (0, 100))
        else:
            window.blit(self.star, (0, 100))
        window.blit(self.star_fall, (1000 - temp * 1.5, -300 + temp * 1.5))
        window.blit(self.star_fall, (800 - temp * 1.5, -1000 + temp * 1.5))
        window.blit(self.star_fall, (1700 - temp * 1.5, -600 + temp * 1.5))

    def all_maps_of_user(self):
        pg.display.set_caption("Play")
        title, title_rect, shader_title, shader_title_rect = shader_text("Select Map", font(small_size), (600, 60), white, black)
        play_button = Button(img=self.short_bar, pos_center=(190, 720), content="Play", font=font(small_size))
        new_map_button = Button(img=self.short_bar, pos_center=(460, 720), content="New Map", font=font(small_size))
        delete_button = Button(img=self.short_bar, pos_center=(730, 720), content='Delete', font=font(small_size))
        back_button = Button(img=self.short_bar, pos_center=(1000, 720), content='Back', font=font(small_size))
        
        game_names = self.file_manager.get_files()
        lst_game = []
        for i, game_name in enumerate(game_names):
            lst_game.append(Button(img=self.game_exist_table, pos_center=(300 + i % 3 * 300, 250 + i // 3 * 200), content=game_name, font=font(small_size)))
        text_return = ''
        played_game = None
        while True:
            # theme
            self.back_ground()
            self.bg += 1
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            # title
            window.blit(shader_title, shader_title_rect)
            window.blit(title, title_rect)
            # created_map            
            box_of_created_map = pg.Rect(0, 100, 1200, 500)
            pg.draw.rect(window, white, box_of_created_map)
            pg.draw.line(window, black, (0, box_of_created_map.top), (1200, box_of_created_map.top), 10)
            pg.draw.line(window, black, (0, box_of_created_map.bottom), (1200, box_of_created_map.bottom), 10)
            t, t_rect = get_text(text_return, font(tiny_size), (600, 140), black)
            window.blit(t, t_rect)
            # button
            lis = [play_button, back_button, new_map_button, delete_button] + lst_game
            
            for button in lis:
                button.update_color_line(mouse_pos)
                button.update(window)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.sound.sound_select(lis)
                    if back_button.is_pointed(mouse_pos):
                        self.main_menu()
                    if new_map_button.is_pointed(mouse_pos):
                        if len(lst_game) < 6:
                            self.create_new_map()
                        else: text_return = 'max files is 6'
                    for i in range(len(lst_game)):
                        if lst_game[i].is_pointed(mouse_pos):
                            for game in lst_game: game.active = False
                            lst_game[i].active = True
                            played_game = lst_game[i]
                    if delete_button.is_pointed(mouse_pos):
                        self.file_manager.delete(played_game.content)
                        try: lst_game.remove(played_game)
                        except: pass
                        played_game = None
                    if play_button.is_pointed(mouse_pos) and played_game != None:
                        self.in_game = True
                        Game.__init__(self, None, 'load', 'player', None, self.sound, None, played_game.content)
                        self.run_game()
                
            pg.display.update()                 
        
    def options(self):
        sound_button = Button(img=self.long_bar, pos_center=(600, 250), content='Sound',font=font(normal_size), corner_radius=5)
        skin_button = Button(img=self.long_bar, pos_center=(600, 400), content='Skin',font=font(normal_size), corner_radius=5)
        done_button = Button(img=self.short_bar, pos_center=(600, 550), content="Done", font=font(small_size), corner_radius=10)
        lis = [sound_button, skin_button, done_button]
        
        while self.option:
            self.draw_game()
            # window.blit(self.frame_option, (200, 50))
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        break

                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.sound.sound_select(lis)

                        if sound_button.is_pointed(mouse_pos):
                            self.option_sound = True
                            self.sound_menu()
                        if skin_button.is_pointed(mouse_pos):
                            self.skin()
                        if done_button.is_pointed(mouse_pos):
                            self.option = False
                            # self.esc_menu()
            
            for button in lis:
                button.update_color_line(mouse_pos)
                button.update(window)


            pg.display.update()
            
    def sound_menu(self):
        sound_effect_button = Button(img=self.Sound_Effect, pos_center=(360, 250), content='',font=font(small_size), corner_radius=5)
        background_sound_button = Button(img=self.Background_Sound, pos_center=(360, 450), content='', font=font(small_size), corner_radius=5)
        sound_effect_button_x = Button(img=self.Sound_Effect_X, pos_center=(360, 250), content='', font=font(small_size), corner_radius=5)
        background_sound_button_x = Button(img=self.Background_Sound_X, pos_center=(360, 450), content='',font=font(small_size), corner_radius=5)
        # back_to_game_button = Button(img=self.back, pos_center=(930, 115), content='', font=font(small_size), corner_radius=5)
        but1_button = Button(img=self.but, pos_center=(self.sound.pos1 + 22, 340), content='', font=font(small_size), corner_radius=5)
        but2_button = Button(img=self.but, pos_center=(self.sound.pos2 + 22, 540), content='', font=font(small_size), corner_radius=5)
        done_button = Button(img=self.short_bar, pos_center=(600, 700), content="Done", font=font(small_size), corner_radius=10)
        lis = [sound_effect_button, background_sound_button, sound_effect_button_x, background_sound_button_x, done_button,but1_button, but2_button]

        # window.fill(theme_color)
        window.blit(self.Bar, (365, 318))
        window.blit(self.Bar, (365, 518))

        while self.option_sound:
            if self.in_game:
                self.draw_game()
            else: window.blit(background, (0, 0))
            
            window.blit(self.table, (230, 70))
            
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        break

                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.sound.sound_select(lis)
                        if sound_effect_button.is_pointed(mouse_pos):
                            if self.sound.op % 2 == 1:
                                but1_button.rect[0] = 501
                                self.s = 1
                            else:
                                but1_button.rect[0] = 366
                            self.sound.op += 1
                            #self.sound.sound_effect(-1)
                        if background_sound_button.is_pointed(mouse_pos):
                            if self.sound.op2 % 2 == 1:
                                but2_button.rect[0] = 501
                                self.s = 1
                            else:
                                but2_button.rect[0] = 366
                            self.sound.op2 += 1
                            self.sound.background_sound(self.sound.op2)
                        if done_button.is_pointed(mouse_pos):
                            self.option_sound = False
            window.blit(self.temp, (348, 503))
            window.blit(self.temp, (348, 303))
            self.sound.vol1 = but1_button.drag(mouse_pos, self.sound.vol1)
            self.sound.vol2 = but2_button.drag(mouse_pos, self.sound.vol2)
            self.sound.pos1 = but1_button.rect[0]
            self.sound.pos2 = but2_button.rect[0]

            if self.s == 1:
                self.sound.vol1 = -0.2
                self.sound.vol2 = -0.2
                pg.mixer.music.set_volume(0.5 + self.sound.vol2)
                self.s = 0
            else:
                pg.mixer.music.set_volume(0.5 + self.sound.vol2)
                if (self.sound.vol1 >= -0.5 and self.sound.vol1 < -0.48) or but1_button.rect[0] == 366:
                    self.sound.op = 1
                else:
                    self.sound.op = 0
                if (self.sound.vol2 >= -0.5 and self.sound.vol2 < -0.48) or but2_button.rect[0] == 366:
                    self.sound.op2 = 1
                else:
                    self.sound.op2 = 2
                    self.sound.background_sound(self.sound.op2)
            for button in lis:
                if self.sound.op % 2 == 0 and button == sound_effect_button_x:
                    continue
                if self.sound.op2 % 2 == 0 and button == background_sound_button_x:
                    continue

                button.update_color_line(mouse_pos)
                button.update(window)

            pg.display.update()

    def main_menu(self):
        pg.display.set_caption("Menu")
        self.in_game = False
        self.player_name = "kim"
        self.file_manager = File(self.player_name)
        
        play_button = Button(img=self.long_bar, pos_center=(600, 300), content="PLAY", font=font(normal_size))
        bot_button = Button(img=self.long_bar, pos_center=(600, 450), content="BOT", font=font(normal_size))
        options_button = Button(img=self.short_bar, pos_center=(450, 600), content="OPTIONS", font=font(small_size), corner_radius=10)
        quit_button = Button(img=self.short_bar, pos_center=(750, 600), content="QUIT", font=font(small_size), corner_radius=10)
        lis = [play_button, bot_button, options_button, quit_button]
        while True:
            
            # # window.fill(theme_color)
            self.back_ground()
            self.bg += 1
            menu, menu_rect, shader_menu, shader_menu_rect = shader_text("MAZE SOLVE", font(title_size, "super_pixel.ttf"), pos_center=(600, 100), color=white, color_shader=purple)
            
            window.blit(shader_menu, shader_menu_rect)
            window.blit(menu, menu_rect)
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            # button
            
            for button in [play_button, bot_button, options_button, quit_button]:
                button.update_color_line(mouse_pos)
                button.update(window)
                
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.sound.sound_select(lis)
                    if play_button.is_pointed(mouse_pos):
                        self.game_type = 'player'
                       
                        self.all_maps_of_user()
                    if bot_button.is_pointed(mouse_pos):
                        self.game_type = 'bot'
                      
                        self.create_new_map()
                    if options_button.is_pointed(mouse_pos):
                        self.option_sound = True
                        self.sound_menu()
                    if quit_button.is_pointed(mouse_pos):
                       
                        pg.quit()
            pg.display.update()
        
    def sign_up_menu(self):
        
        name = Input_Button(img=self.input_img, pos_center=(600, 200), content='', font=font(tiny_size))
        password = Input_Button(img=self.input_img, pos_center=(600, 350), content='', font=font(tiny_size), hide=True)
        re_password = Input_Button(img=self.input_img, pos_center=(600, 500), content='', font=font(tiny_size), hide=True)
        
        note, note_rect = get_text("Already have an account. ", font=font(tiny_size), pos_center=(540, 750))
        sign_in, sign_in_rect = get_text('Sign in', font=font(tiny_size), pos_center=(780, 750), color=red)
        
        sign_up_button = Button(img=self.short_bar, pos_center=(600, 650), content='SIGN UP', font=font(small_size))

        name_text, name_rect = get_text('Username', font=font(32), pos_center=(600, 130))
        pass_text, pass_rect = get_text('Password', font=font(32), pos_center=(600, 280))
        re_pass_text, re_pass_rect = get_text('Re_password', font=font(32), pos_center=(600, 430))
        text_return = ''
        name.active = True
        while True:
            
            # window.fill(theme_color)
            self.back_ground()
            self.bg += 1
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
                    sign_in, sign_in_rect = get_text('Sign in', font=font(tiny_size), pos_center=(780, 750), color=yellow)
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
            
            text_surface, text_surface_rect = get_text(content=text_return, font=font(tiny_size), pos_center=(600, 560))
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
        
        note, note_rect = get_text("Don't have an account. ", font=font(tiny_size), pos_center=(540, 680))
        sign_up, sign_up_rect = get_text('Sign up', font=font(tiny_size), pos_center=(760, 680), color=red)
        
        name_text, name_rect = get_text('Username', font=font(small_size), pos_center=(600, 200))
        pass_text, pass_rect = get_text('Password', font=font(small_size), pos_center=(600, 350))
        text_return = ''
        
        name.active = True
        while True:
            # window.fill(theme_color)
            self.back_ground()
            self.bg += 1
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
                        sign_up, sign_up_rect = get_text('Sign up', font=font(tiny_size), pos_center=(760, 680), color=yellow)
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
            
            text_surface, text_surface_rect = get_text(content=text_return, font=font(tiny_size), pos_center=(600, 490))
            window.blit(text_surface, text_surface_rect)
                
            name.draw()
            password.draw()
            pg.display.update()
            
            if text_return == 'login successfull':
                self.player_name = name.input
                pg.display.update()
                time.sleep(0.1)
                self.main_menu()
                
    def saveleaderboard(self):
        if self.check == 1:
            df = pd.read_excel('leaderboard.xlsx')
            new_data = {
                'Tên': self.isname,
                'Map': self.size,
                'Steps': self.player.steps,
                'Time': self.elapsed_time 
            }
            existing_row = df[(df['Tên'] == new_data['Tên']) & (df['Map'] == new_data['Map'])]

            if not existing_row.empty:
                if (new_data['Steps'] < existing_row.iloc[0]['Steps']) or \
                        (new_data['Time'] < existing_row.iloc[0]['Time']):
                    df.loc[existing_row.index, ['Steps', 'Time']] = new_data['Steps'], new_data['Time']
            else:
                new_row_df = new_data
                df = pd.concat([df, new_row_df], ignore_index=True)
            df.sort_values(by=['Map', 'Time', 'Steps'], ascending=[False, True, True], inplace=True)
            df.to_excel('leaderboard.xlsx', index=False)
            
if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()