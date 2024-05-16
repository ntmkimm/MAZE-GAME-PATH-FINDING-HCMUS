import pygame as pg
from color import *
from button import *
from ui import *
from maze_generator import *
from player import *
from sound import *
import os
from game import *

pg.init()

class Menu(Game):
    def __init__(self):
        self.table = pg.image.load(os.path.join("pic", "Table.png"))
        self.back = pg.image.load(os.path.join("pic", "Back.png"))
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
        self.bg_vic = pg.image.load(os.path.join("pic", "bg.png"))
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
        self.yellow = pg.image.load(os.path.join("pic", "Yellow.png"))
        self.blue = pg.image.load(os.path.join("pic", "Blue.png"))
        self.brown = pg.image.load(os.path.join("pic", "Brown.png"))
        self.gray = pg.image.load(os.path.join("pic", "Gray.png"))
        self.green = pg.image.load(os.path.join("pic", "Green.png"))
        self.pink = pg.image.load(os.path.join("pic", "pink.png"))
        self.purple = pg.image.load(os.path.join("pic", "Purple.png"))
        self.result1 = pg.image.load(os.path.join("pic", "result.png"))
        self.game_type = 'player'
        self.sound = Sound()
        self.s = 0
        self.bg = 0
        self.background = self.yellow
        self.sound.background_sound(0)


    def esc_menu(self):
        back_to_game_button = Button(img=self.long_bar, pos_center=(600, 350), content='Back to Game', font=font(small_size))
        options_button = Button(img=self.short_bar, pos_center=(450, 500), content='Options', font=font(small_size))
        quit_button = Button(img=self.short_bar, pos_center=(750, 500), content="Quit", font=font(small_size))
        lis = [back_to_game_button, options_button, quit_button]
        
        while self.pause:
            # mouse_pos     
            mouse_pos = pg.mouse.get_pos()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.sound.sound_select(lis)
                    if quit_button.is_pointed(mouse_pos):
                        self.pause = False
                        self.main_menu()
                    elif options_button.is_pointed(mouse_pos):
                        self.pause = False
                        self.option = True
                        self.options()
                    elif back_to_game_button.is_pointed(mouse_pos):
                        self.pause = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause = False        

            for button in [back_to_game_button, options_button, quit_button]:
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

        lis = [cancel_button, create_new_button, easy_button, normal_button, hard_button, random_button, choose_button]
                    
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
                    self.sound.sound_select(lis)
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
                        self.sound.sound_select([create_new_button])
                        if self.size_mode == 0:     self.size = 20
                        elif self.size_mode == 1:   self.size = 40
                        elif self.size_mode == 2:   self.size = 100
                        
                        if self.init_mode == 0:      self.init = 'random'
                        elif self.init_mode == 1:    self.init = 'choose'

                        self.skin()

                        Game.__init__(self, self.size, self.init, self.game_type, self.sound, self.character, self.background)
                        self.run_game()
                        self.victory()
                        #self.result()
                    
                        
            for button in [cancel_button, create_new_button, mode_button[self.size_mode], init_button[self.init_mode]]:
                button.update_color_line(mouse_pos)
                button.update(window)
                        
            pg.display.update()

    def all_maps_of_user(self):
        pg.display.set_caption("Play")
        
        back_button = Button(img=self.short_bar, pos_center=(900, 700), content='Back', font=font(small_size))
        new_map_button = Button(img=self.long_bar, pos_center=(400, 700), content="Create New Map", font=font(small_size))
        lis = [back_button, new_map_button]
        
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
                    self.sound.sound_select(lis)
                    if back_button.is_pointed(mouse_pos):
                        self.main_menu()
                    if new_map_button.is_pointed(mouse_pos):
                        self.create_new_map()
                
            pg.display.update()                 
        
    def options(self):
        sound_effect_button = Button(img=self.Sound_Effect, pos_center=(360, 200), content='',font=font(small_size), corner_radius=2)
        background_sound_button = Button(img=self.Background_Sound, pos_center=(360, 400), content='', font=font(small_size), corner_radius=2)
        sound_effect_button_x = Button(img=self.Sound_Effect_X, pos_center=(360, 200), content='', font=font(small_size), corner_radius=2)
        background_sound_button_x = Button(img=self.Background_Sound_X, pos_center=(360, 400), content='',font=font(small_size), corner_radius=2)
        back_to_game_button = Button(img=self.back, pos_center=(930, 70), content='', font=font(small_size), corner_radius=2)
        but1_button = Button(img=self.but, pos_center=(self.sound.pos1 + 22, 290), content='', font=font(small_size), corner_radius=2)
        but2_button = Button(img=self.but, pos_center=(self.sound.pos2 + 22, 490), content='', font=font(small_size), corner_radius=2)


        lis = [sound_effect_button, background_sound_button, sound_effect_button_x, background_sound_button_x, back_to_game_button,but1_button, but2_button]

        window.fill(light_blue)
        window.blit(self.table, (230, 20))
        window.blit(self.Bar, (365, 268))
        window.blit(self.Bar, (365, 468))



        while self.option:

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
                        if back_to_game_button.is_pointed(mouse_pos):
                            self.option = False
            window.blit(self.temp, (348, 453))
            window.blit(self.temp, (348, 253))
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

    def skin(self):
        pg.display.set_caption("Skin")
        top_button1 = Button(img=self.top, pos_center=(270, 90), content="", font=font(small_size), corner_radius=10)
        bot_button1 = Button(img=self.bot, pos_center=(270, 580), content="", font=font(small_size), corner_radius=10)
        top_button2 = Button(img=self.top, pos_center=(930, 90), content="", font=font(small_size), corner_radius=10)
        bot_button2 = Button(img=self.bot, pos_center=(930, 580), content="", font=font(small_size), corner_radius=10)
        play_button = Button(img=self.short_bar, pos_center=(600, 700), content="Play", font=font(small_size), corner_radius=10)
        random_button = Button(img=self.short_bar, pos_center=(600, 400), content="Random", font=font(small_size),corner_radius=10)
        back_button = Button(img=self.short_bar, pos_center=(600, 200), content="Back", font=font(small_size), corner_radius=10)
        lis = [top_button1, bot_button1, play_button, top_button2, bot_button2, back_button, random_button]

        run = True
        option1 = 0
        option2 = 0
        temp = 0
        cha_lis = [self.cha0_1, self.cha0_2, self.cha1_1, self.cha1_2, self.cha2_1, self.cha2_2, self.cha3_1, self.cha3_2]
        bg_lis = [self.yellow, self.gray, self.green, self.blue, self.pink, self.purple, self.brown]
        name_cha_lis = ["MaskDude", "NinjaFrog", "PinkMan", "VirtualGuy"]
        while run:
            window.fill(light_blue)
            window.blit(self.frame, (120, 170))
            window.blit(self.frame, (780, 170))
            mouse_pos = pg.mouse.get_pos()
            if temp % 40 >= 0 and temp % 40 <= 20:
                window.blit(cha_lis[(option1 % 8)], (150, 220))
                temp += 1
            else:
                window.blit(cha_lis[(option1 % 8) + 1], (150, 220))
                temp += 1

            pg.draw.rect(window, black, (894, 296, 72, 72), 3)
            window.blit(bg_lis[option2 % 7], (898, 300))

            self.character = name_cha_lis[(int)((option1 % 8) / 2)]
            self.background = bg_lis[option2 % 7]

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.sound.sound_select(lis)
                    if play_button.is_pointed(mouse_pos):
                        run = False
                    if back_button.is_pointed(mouse_pos):
                        self.create_new_map()
                    if top_button1.is_pointed(mouse_pos):
                        option1 += 2
                    if top_button2.is_pointed(mouse_pos):
                        option2 += 2
                    if bot_button1.is_pointed(mouse_pos):
                        option1 -= 2
                    if bot_button2.is_pointed(mouse_pos):
                        option2 -= 2
                    if random_button.is_pointed(mouse_pos):
                        self.character = name_cha_lis[(int)((temp % 8) / 2)]
                        self.background = bg_lis[temp % 7]
                        run = False

            for button in lis:
                button.update(window)
                button.update_color_line(mouse_pos)
            pg.display.update()
    def victory(self):
        pg.display.set_caption("Victory")
        continue_button = Button(img=self.long_bar, pos_center=(600, 700), content="Continue", font=font(small_size))
        run = True
        start = pg.time.get_ticks()
        tim = (int)((pg.time.get_ticks() - start) / 1000)
        pg.mixer.music.pause()
        while tim != 2:
            tim = (int)((pg.time.get_ticks() - start) / 1000)
            window.fill(light_blue)
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
        window.fill(light_blue)
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

    def back_ground(self):
        temp = self.bg % 1070
        if self.bg % 100 >= 0 and self.bg % 100 <= 40:
            window.blit(self.star1, (0, 100))
        else:
            window.blit(self.star, (0, 100))
        window.blit(self.star_fall, (1000 - temp * 1.5, -300 + temp * 1.5))
        window.blit(self.star_fall, (800 - temp * 1.5, -1000 + temp * 1.5))
        window.blit(self.star_fall, (1700 - temp * 1.5, -600 + temp * 1.5))
        title3, menu_rect, shader_menu, shader_menu_rect = shader_text("MAZESOLVE", font(100), pos_center=(600, 100),color=white, color_shader=black)
        window.blit(shader_menu, shader_menu_rect)
        window.blit(title3, menu_rect)



    def main_menu(self):
        pg.display.set_caption("Menu")

        play_button = Button(img=self.long_bar, pos_center=(600, 300), content="PLAY", font=font(normal_size))
        bot_button = Button(img=self.long_bar, pos_center=(600, 450), content="BOT", font=font(normal_size))
        options_button = Button(img=self.short_bar, pos_center=(450, 600), content="OPTIONS", font=font(small_size), corner_radius=10)
        quit_button = Button(img=self.short_bar, pos_center=(750, 600), content="QUIT", font=font(small_size), corner_radius=10)
        lis = [play_button, bot_button, options_button, quit_button]

        while True:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()

            
            window.fill(light_blue)
            # mouse_pos
            mouse_pos = pg.mouse.get_pos()
            # button

            self.back_ground()
            self.bg += 1

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
                        self.option = True
                        self.options()
                    if quit_button.is_pointed(mouse_pos):
                        pg.quit()
            pg.display.update()
        
        
if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()
            