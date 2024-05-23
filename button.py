from color import *
from ui import *
from sound import *

class Button:
    def __init__(self, img, pos_center, content, font, line_base_color=yellow, corner_radius=10):
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
        
        self.active = False
        
    def create_rounded_image(self):
        rounded_img = pg.Surface(self.img.get_size(), pg.SRCALPHA)
        mask = pg.Surface(self.img.get_size(), pg.SRCALPHA)
        rect = mask.get_rect()
        pg.draw.rect(mask, self.line_color, rect, border_radius=self.corner_radius)
        rounded_img.blit(self.img, (0, 0))
        rounded_img.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)
        return rounded_img
        
    def update(self, window):
        self.rounded_img = self.create_rounded_image()
        window.blit(self.rounded_img, self.rect.topleft)
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
        if self.is_pointed(position) or self.active:
            self.line_color = self.line_base_color
        else:
            self.line_color = white