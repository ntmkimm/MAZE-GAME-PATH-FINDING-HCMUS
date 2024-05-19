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
    if name == '':
        return 'username is empty'
    elif password == '':
        return 'password is empty'
    if (name, password) in user_password_pairs:
        return 'login successfull'
    elif name in users:
        return 'wrong password. type again'
    else:
        return 'unregister'

class Input_Button(Button):
    def __init__(self, img, pos_center, content, font, line_base_color=white, hide=False):
        Button.__init__(self, img, pos_center, content, font, line_base_color)
        self.active = False
        self.hide = hide
        self.line_thick = 10
        self.input = ''
        
        self.cursor_visible = True
        self.last_toggle = time.time()
        
    def draw(self):
        if self.hide:
            text = self.font.render('*' * len(self.input), True, black)
        else:
            text = self.font.render(self.input, True, black)
            
        window.blit(text, (self.rect.x + 10, self.rect.y + 20))

        if self.active:
            if time.time() - self.last_toggle > 0.5:
                self.cursor_visible = not self.cursor_visible
                self.last_toggle = time.time()
            if self.cursor_visible:
                text_width, text_height = self.font.size(self.input)
                cursor_x = self.rect.x + 10 + text_width
                cursor_y = self.rect.y + 15
                cursor_width = 4
                cursor_height = text_height + 10
                cursor_rect = pg.Rect(cursor_x, cursor_y, cursor_width, cursor_height)
                pg.draw.rect(window, pg.Color('black'), cursor_rect)
