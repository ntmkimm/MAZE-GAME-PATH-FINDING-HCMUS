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
    name_2 = name2
    user_password_pairs = list(zip(user,password))
    if name_1 in user:
        return 1
    else:
        with open('text.txt','a') as f2:
            f2.write('\n'+name1)
            f2.write('\n'+name2)
        return 2


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
    name_2 = name2
    user_password_pairs = list(zip(user,password))
    print(user_password_pairs)
    checka = True
    if (name1,name2) in user_password_pairs:
        return 1
    elif name_1 in user:
        return 2
    else:
        return 3
    
current_time = pg.time.get_ticks()
cursor_timer = pg.time.get_ticks()
cursor_blink = True

name_rect = pg.Rect(250, 205, 300, 32)
pass_rect = pg.Rect(250, 255, 300, 32)
check_pass_rect = pg.Rect(250, 305, 300, 32)
sign_up_rect = pg.Rect(350,370,100,32)

color_active = pg.Color('lightskyblue3')
color_passive = pg.Color('chartreuse4')

font = ui.font(32)

if current_time - cursor_timer > 500:  # Thời gian nháy là 500ms
    cursor_blink = not cursor_blink
    cursor_timer = current_time
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
                if user_text2_check == user_text2:
                    check = sign_up(user_text1,user_text2)
                    if check == 1:
                        user_text3 = 'name already existed'
                        print(check)
                    elif check == 2:
                        user_text3 = 'registered successfully'
                else:
                    user_text3 = 'wrong Re_password'
                text_surface6 = font.render(user_text3, True, black)
                window.blit(text_surface6, (130, 340))
                pg.display.update()
                pg.time.wait(2000)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                if active1:
                    user_text1 = user_text1[:-1]
                if active2:
                    user_text2 = user_text2[:-1]
                if active3:
                    user_text2_check = user_text2_check[:-1]
            else:
                if active1:
                    user_text1 += event.unicode
                if active2:
                    user_text2 +=event.unicode
                if active3:
                    user_text2_check +=event.unicode
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
    text_surface = font.render(user_text1, True, white)
    text_surface2 = font.render(user_text2, True, white)
    text_surface2_check = font.render(user_text2_check, True, white)
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



    
