import pygame as pg
from game import *
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
    elif name in users:
        return 'name already existed'
    elif password != re_password:
        return 'wrong password'
    
    if users == []:
        with open('text.txt','a') as f:
            f.write(name + '\n' + password)
    else:
        with open('text.txt','a') as f:
            f.write('\n' + name)
            f.write('\n' + password)
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
    
current_time = pg.time.get_ticks()
cursor_timer = pg.time.get_ticks()
cursor_blink = True

if current_time - cursor_timer > 50:  # Thời gian nháy là 500ms
    cursor_blink = not cursor_blink
    cursor_timer = current_time

class Input_Button(Button):
    def __init__(self, img, pos_center, content, font, line_base_color=dark_blue, hide=False):
        Button.__init__(self, img, pos_center, content, font, line_base_color)
        self.active = False
        self.hide = hide
        self.line_thick = 3
        self.input = ''
        
    def draw(self):
        if self.hide:
            text = self.font.render('*' * len(self.input), True, black)
        else:
            text = self.font.render(self.input, True, black)
            
        window.blit(text, (self.rect.x + 10, self.rect.y + 20))
