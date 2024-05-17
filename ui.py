from color import *
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

def get_text(content, font, pos_center, color):
    text = font.render(content, True, color)
    rect = text.get_rect(center=pos_center)
    return text, rect