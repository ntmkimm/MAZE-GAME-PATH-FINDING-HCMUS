import pygame as pg
from game import *
import ui
from color import *

def sign_up(name1,name2):
    with open('text.txt','r') as f1:
        name = f1.readlines()
    user = []
    password = []
    for i in range(0,len(name),2):
        user.append(name[i].strip())
    for j in range(1,len(name),2):
        password.append(name[j].strip())
    name_1 = name1
    
    if name_1 in user:
        return 'name already existed'
    else:
        with open('text.txt','a') as f2:
            f2.write('\n'+name1)
            f2.write('\n'+name2)
        return 'registered successfully'


def sign_in(name1,name2):
    with open('text.txt','r') as f1:
        name = f1.readlines()
    user = []
    password = []
    for i in range(0,len(name),2):
        user.append(name[i].strip())
    for j in range(1,len(name),2):
        password.append(name[j].strip())
    name_1 = name1
    user_password_pairs = list(zip(user,password))
    
    if (name1,name2) in user_password_pairs:
        return 1
    elif name_1 in user:
        return 2
    else:
        return 3
    
pg.init()

font = pg.font.SysFont(None, 32)
    
current_time = pg.time.get_ticks()
cursor_timer = pg.time.get_ticks()
cursor_blink = True

name_rect = pg.Rect(250, 205, 400, 32)
pass_rect = pg.Rect(250, 255, 400, 32)
check_pass_rect = pg.Rect(250, 305, 400, 32)
sign_up_rect = pg.Rect(350, 370, 100, 32)

color_active = pg.Color('lightskyblue3')
color_passive = pg.Color('chartreuse4')

if current_time - cursor_timer > 50:  # Thời gian nháy là 500ms
    cursor_blink = not cursor_blink
    cursor_timer = current_time

class Input_Button():
    def __init__(self, rect):
        self.rect = rect
        self.active = False
        self.input = ''
        self.color = color_passive
        
    def update(self, position):
        self.active = self.rect.collidepoint(position)

        if self.active:
            self.color = color_active
        else:
            self.color = color_passive
    
    def draw(self):
        text = font.render(self.input, True, black)
        pg.draw.rect(window, self.color, self.rect)
        window.blit(text, (self.rect.x + 5, self.rect.y + 5))
        # pg.display.update()
            
name = Input_Button(name_rect)
password = Input_Button(pass_rect)
re_password = Input_Button(check_pass_rect)

window.fill(white)

while True:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                name.update(event.pos)
                password.update(event.pos)
                re_password.update(event.pos)
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    if name.active:
                        name.input = name.input[:-1]
                    elif password.active:
                        password.input = password.input[:-1]
                    elif re_password.active:
                        re_password.input = re_password.input[:-1]
                else:
                    if name.active:
                        name.input += event.unicode
                    elif password.active:
                        password.input += event.unicode
                    elif re_password.active:
                        re_password.input += event.unicode
    
    name.draw()
    password.draw()
    re_password.draw()
    
    pg.draw.rect(window, light_blue, sign_up_rect)
    
    text_surface3 = font.render('Username:', True, black)
    window.blit(text_surface3, (130, 210))
    text_surface4 = font.render(' Password:', True, black)
    window.blit(text_surface4, (130, 260))
    text_surface4_check = font.render(' Re_password:', True, black)
    window.blit(text_surface4_check, (93, 310))
    text_surface5 = font.render(' SIGN UP', True, black)
    window.blit(text_surface5,(sign_up_rect.left,sign_up_rect.y+5))
    pg.display.flip()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            pg.sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if name_rect.collidepoint(event.pos):
                active1 = True
                active2 = False
                active3 = False
            elif pass_rect.collidepoint(event.pos):
                active2 = True
                active1 = False
                active3 = False
            elif check_pass_rect.collidepoint(event.pos):
                active3 = True
                active1 = False
                active2 = False
            else:
                active1 = False
                active2 = False
                active3 = False
            if sign_up_rect.collidepoint(event.pos):
                if check_pass_input == pass_input:
                    user_text3 = sign_up(name_input, pass_input)
                else:
                    user_text3 = 'Wrong re-password'
                text_surface6 = font.render(user_text3, True, black)
                window.blit(text_surface6, (130, 340))
                pg.display.update()
                pg.time.wait(2000)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                if active1:
                    name_input = name_input[:-1]
                if active2:
                    pass_input = pass_input[:-1]
                if active3:
                    check_pass_input = check_pass_input[:-1]
            else:
                if active1:
                    name_input += event.unicode
                if active2:
                    pass_input +=event.unicode
                if active3:
                    check_pass_input +=event.unicode
    if active1 and not active2 and not active3:
        color1 = color_active
    else:
        color1 = color_passive
    if active2 and not active1 and not active3:
        color2 = color_active
    else:
        color2 = color_passive
    if active3 and not active1 and not active2:
        color3 = color_active
    else:
        color3 = color_passive
        
    window.fill(white)
    pg.draw.rect(window, color1, name_rect)
    pg.draw.rect(window, color2, pass_rect)
    pg.draw.rect(window, color3, check_pass_rect)
    pg.draw.rect(window,light_blue,sign_up_rect)
    text_surface = font.render(name_input, True, white)
    text_surface2 = font.render(pass_input, True, white)
    text_surface2_check = font.render(check_pass_input, True, white)
    window.blit(text_surface, (name_rect.x + 5, name_rect.y + 5))
    window.blit(text_surface2, (pass_rect.x + 5, pass_rect.y + 5))
    window.blit(text_surface2_check, (check_pass_rect.x + 5, check_pass_rect.y + 5))
    name_rect.w = max(100, text_surface.get_width() + 10)
    pass_rect.w = max(100, text_surface2.get_width() + 10)
    check_pass_rect.w = max(100, text_surface2_check.get_width() + 10)
    if active1 and cursor_blink:
        pg.draw.rect(window, black,
    (name_rect.x + text_surface.get_width() + 5, name_rect.y + 5, 2, text_surface.get_height()))
    if active2 and cursor_blink:
        pg.draw.rect(window, black,
    (pass_rect.x + text_surface2.get_width() + 5, pass_rect.y + 5, 2, text_surface2.get_height()))
    if active3 and cursor_blink:
        pg.draw.rect(window, black,
    (check_pass_rect.x + text_surface2_check.get_width() + 5, check_pass_rect.y + 5, 2, text_surface2_check.get_height()))
    text_surface3 = font.render('Username:', True, black)
    window.blit(text_surface3, (130, 210))
    text_surface4 = font.render(' Password:', True, black)
    window.blit(text_surface4, (130, 260))
    text_surface4_check = font.render(' Re_password:', True, black)
    window.blit(text_surface4_check, (93, 310))
    text_surface5 = font.render(' SIGN UP', True, black)
    window.blit(text_surface5,(sign_up_rect.left,sign_up_rect.y+5))
    pg.display.flip()



    
