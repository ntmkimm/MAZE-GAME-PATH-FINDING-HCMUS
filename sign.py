import pygame as pg
from game import *
import ui
from color import *
from button import *

pg.init()

def read_data():
    with open('text.txt','r') as f:
        data = f.readlines()
    users = []
    passwords = []
    for i in range(0, len(data), 2):
        users.append(data[i].strip())
    for j in range(1, len(data), 2):
        passwords.append(data[j].strip())
        
    return users, passwords

def sign_up(name, password, re_password):
    users, _ = read_data()
    if name == '':
        return 'username is empty'
    elif password == '':
        return 'password is empty'
    elif re_password == '':
        return 're_password is empty'
    elif not name.isalnum() or name[0].isdigit():
        return 'username must contain alphabet'
    elif len(name) <= 2:
        return 'username too short'
    elif len(name) >= 10:
        return 'username too long'
    elif name in users:
        return 'name already existed'
    elif password != re_password:
        return 'wrong password'
    
    if users == []:
        with open('text.txt','a') as f:
            f.write(name + '\n' + password)
    else:
        with open('text.txt','a') as f:
            f.write('\n' + name + '\n' + password)
    print('done')
    return 'registered successfully'

def sign_in(name, password):
    users, passwords = read_data()
    
    user_password_pairs = list(zip(users, passwords))
    
    if (name, password) in user_password_pairs:
        return 1
    elif name in users:
        return 2
    else:
        return 3
    
font = ui.font(text_size=32)
    
current_time = pg.time.get_ticks()
cursor_timer = pg.time.get_ticks()
cursor_blink = True

if current_time - cursor_timer > 50:  # Thời gian nháy là 500ms
    cursor_blink = not cursor_blink
    cursor_timer = current_time

class Input_Button(Button):
    # def __init__(self, img, pos_center, content, font, hide=False):
    def __init__(self, rect, hide=False):
        self.rect = rect
        self.active = False
        self.input = ''
        self.color = color_passive
        self.hide = hide
        self.font = font
        
    def update(self, position):
        self.active = self.rect.collidepoint(position)

        if self.active:
            self.color = color_active
        else:
            self.color = color_passive
    
    def draw(self):
        if self.hide:
            text = font.render('*' * len(self.input), True, black)
        else:
            text = font.render(self.input, True, black)
        pg.draw.rect(window, self.color, self.rect)
        window.blit(text, (self.rect.x + 5, self.rect.y + 5))

def sign_up_menu():
    
    name_rect = pg.Rect(250, 205, 400, 32)
    pass_rect = pg.Rect(250, 255, 400, 32)
    check_pass_rect = pg.Rect(250, 305, 400, 32)
    sign_up_rect = pg.Rect(350, 370, 100, 32)
    
    name = Input_Button(name_rect, hide=False)
    password = Input_Button(pass_rect, hide=True)
    re_password = Input_Button(check_pass_rect, hide=True)
    text = ''
    
    while True:
        window.fill(white)
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    name.update(event.pos)
                    password.update(event.pos)
                    re_password.update(event.pos)
                    
                    if sign_up_rect.collidepoint(event.pos):
                        if re_password.input == password.input:
                            text = sign_up(name.input, password.input, re_password.input)
                
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
                            
        if text != '':
            text_surface = font.render(text, True, black)
            window.blit(text_surface, (130, 340))
        
        name.draw()
        password.draw()
        re_password.draw()
        
        pg.draw.rect(window, light_blue, sign_up_rect)
        
        name_text = font.render('Username:', True, black)
        window.blit(name_text, (130, 210))
        pass_text = font.render(' Password:', True, black)
        window.blit(pass_text, (130, 260))
        re_pass_text = font.render(' Re_password:', True, black)
        window.blit(re_pass_text, (93, 310))
        SIGN_UP_text = font.render(' SIGN UP', True, black)
        window.blit(SIGN_UP_text, (sign_up_rect.left, sign_up_rect.y + 5))
        pg.display.update()
        
sign_up_menu()



    
