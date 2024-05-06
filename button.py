from color import *
from ui import *

class Button:
    #auto set text at the center of the box
    def __init__(self, img, pos_center, content, font):
        self.img = img
        self.rect = self.img.get_rect(center=(pos_center[0], pos_center[1]))
        self.line_thick = 10
        self.font = font
        self.text_color = white
        self.shader_color = black
        self.text, self.text_rect, self.shader_text, self.shader_text_rect = shader_text(content, self.font, (pos_center[0], pos_center[1] - 7), white, black)
        self.line_color = gray
        self.content = content
        
    def update(self, window):
        # right
        pg.draw.line(window, self.line_color, (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom), self.line_thick)
        # left
        pg.draw.line(window, self.line_color, (self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), self.line_thick)
        # top
        pg.draw.line(window, self.line_color, (self.rect.left, self.rect.top), (self.rect.right, self.rect.top), self.line_thick)
        # bottom
        pg.draw.line(window, self.line_color, (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), self.line_thick)
        window.blit(self.img, self.rect)
        window.blit(self.shader_text, self.shader_text_rect)
        window.blit(self.text, self.text_rect)
    
    def is_pointed(self, position):
        if (position[0] in range(self.rect.left + self.line_thick, self.rect.right + self.line_thick)
            and position[1] in range(self.rect.top + self.line_thick, self.rect.bottom + self.line_thick)):
            return True 
        return False
   
    def update_color_line(self, position):
        if self.is_pointed(position):
            self.line_color = black
        else:
            self.line_color = gray