import pygame as pg
from color import *

pg.init()
screen = pg.display.set_mode((720, 720))
pg.display.set_caption("Menu")

bg = screen.fill(white)

PLAY_MOUSE_POS = None

class Button:
    pass

def get_font(size):
    pass

def play():
    pg.display.set_caption("Play")
    while True:
        screen.fill(orange)
        text = get_font(45).render("This is PLAY screen", True, white)
        rect = text.get_rect(center=(640, 260))
        screen.blit(text, rect)
        back = Button(image=None, pos=(640, 640), text_input='BACK',
                    font=get_font(75), base_color=white, hovering_color=green)
        back.changeColor(PLAY_MOUSE_POS)
        back.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTOTNDOWN:
                if back.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
        
        pg.display.update()
                
    
def options():
    pass
def main_menu():
    pg.display.set_caption("Menu")
    while True:
        screen.fill(white)
        MENU_MOUSE_POS = pg.mouse.get_pos()
        
        MENU
        
main_menu()