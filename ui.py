from color import *
import pygame as pg

min_size = 25
small_size = 30
normal_size = 35
big_size = 45
title_size = 70

def font(text_size):
    return pg.font.Font("assets/Font/font.ttf", text_size)

def shader_text(content, font, pos_center, color, color_shader):
    text = font.render(content, True, color)
    rect = text.get_rect(center=pos_center)
    shader_content = font.render(content, True, color_shader)
    shader_rect = text.get_rect(center=(pos_center[0] + 4, pos_center[1] + 4))
    return text, rect, shader_content, shader_rect