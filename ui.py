from color import *
import os
import pygame as pg

tiny_size = 15
min_size = 25
small_size = 30
normal_size = 35
big_size = 45
title_size = 150
pg.init()

def font(text_size, font='font.ttf'):
    return pg.font.Font("assets/Font/" + font, text_size)

def shader_text(content, font, pos_center, color, color_shader):
    text = font.render(content, True, color)
    rect = text.get_rect(center=pos_center)
    shader_content = font.render(content, True, color_shader)
    shader_rect = text.get_rect(center=(pos_center[0] + 4, pos_center[1] + 4))
    return text, rect, shader_content, shader_rect

def get_text(content, font, pos_center, color=green):
    text = font.render(content, True, color)
    rect = text.get_rect(center=pos_center)
    return text, rect

def flip(sprites):
        return [pg.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheeets(dir1, dir2, width, height, size_maze):
    path = os.path.join("assets", dir1, dir2)
    lst_img = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    all_sprites = {}
    
    if size_maze== 100: size = (8, 8)
    elif size_maze == 40: size = (16, 16)
    elif size_maze == 20: size = (32, 32)
    
    for f in lst_img:
        sprite_sheet = pg.image.load(os.path.join(path, f)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            #SRCALPHA is a flag 
            # surface with 32 * 32 pixel to blit onto the main program
            surface = pg.Surface((width, height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            
            sprites.append(pg.transform.scale(surface, size))
            
            
        all_sprites[f.replace(".png", "") + "_right"] = sprites
        all_sprites[f.replace(".png", "") + "_left"] = flip(sprites)

    return all_sprites

