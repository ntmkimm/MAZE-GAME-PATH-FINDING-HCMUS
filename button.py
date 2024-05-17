from color import *
from ui import *

class Button:
    #auto set text at the center of the box
    def __init__(self, img, pos_center, content, font, line_base_color=gray, corner_radius=5):
        self.img = img
        self.rect = self.img.get_rect(center=(pos_center[0], pos_center[1]))
        self.line_thick = 2
        self.font = font
        self.text_color = white
        self.shader_color = black
        self.text, self.text_rect, self.shader_text, self.shader_text_rect \
            = shader_text(content, self.font, (pos_center[0], pos_center[1] - 7), white, black)
        self.line_color = gray
        self.content = content
        self.line_base_color = line_base_color
        self.line_color = line_base_color
        self.corner_radius = corner_radius
        self.dragging = False
        self.de = 4
        
    def update(self, window):
        # right
        pg.draw.line(window, self.line_color, (self.rect.right, self.rect.top + self.corner_radius), (self.rect.right, self.rect.bottom - self.corner_radius), self.line_thick)
        # left
        pg.draw.line(window, self.line_color, (self.rect.left, self.rect.top + self.corner_radius), (self.rect.left, self.rect.bottom - self.corner_radius), self.line_thick)
        # top
        pg.draw.line(window, self.line_color, (self.rect.left + self.corner_radius, self.rect.top), (self.rect.right - self.corner_radius, self.rect.top), self.line_thick)
        # bottom
        pg.draw.line(window, self.line_color, (self.rect.left + self.corner_radius, self.rect.bottom), (self.rect.right - self.corner_radius, self.rect.bottom), self.line_thick)
        # dia
        pg.draw.line(window, self.line_color, (self.rect.left + self.corner_radius + self.de, self.rect.top - 4),(self.rect.left, self.rect.top + self.corner_radius), self.line_thick)
        pg.draw.line(window, self.line_color, (self.rect.right - self.corner_radius - self.de, self.rect.top - 4),(self.rect.right, self.rect.top + self.corner_radius), self.line_thick)
        pg.draw.line(window, self.line_color, (self.rect.left, self.rect.bottom - self.corner_radius),(self.rect.left + self.corner_radius + self.de, self.rect.bottom + 4), self.line_thick)
        pg.draw.line(window, self.line_color, (self.rect.right, self.rect.bottom - self.corner_radius),(self.rect.right - self.corner_radius - self.de, self.rect.bottom + 4), self.line_thick)
        window.blit(self.img, self.rect)
        window.blit(self.shader_text, self.shader_text_rect)
        window.blit(self.text, self.text_rect)
    
    def drag(self, pos, vol):
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0]:
                self.dragging = True
        if self.dragging and pos[0] > 365 and pos[0] < 820:
            self.rect[0] = pos[0]
            vol = (pos[0] - 592) / 455
            if pos[0] == 366:
                vol = -0.5
        if not pg.mouse.get_pressed()[0]:
            self.dragging = False
        return vol
    
    def is_pointed(self, position):
        if self.rect.collidepoint(position):
            return True 
        return False
   
    def update_color_line(self, position):
        if self.is_pointed(position):
            self.line_color = black
        else:
            self.line_color = self.line_base_color