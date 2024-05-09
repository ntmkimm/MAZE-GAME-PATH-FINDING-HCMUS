import os
import random
import math
import pygame as pg
from cell import *
from color import *
            
class Player(): # sprite make it easy to fit pixel perfect

    ANIMATION_DELAY = 3
    # define our initialization area
    
    def __init__(self, grid_cells, init_pos, tile):
        # inherit Cell class
        Cell.__init__(self, init_pos[0], init_pos[1])
        self.grid_cells = grid_cells
        self.rows = len(self.grid_cells)
        self.cols = self.rows
        self.TILE = tile
        self.rect = pg.Rect(self.init_maze_x + self.x * self.TILE, self.init_maze_y + self.y * self.TILE, self.TILE, self.TILE)
        self.x_step = 0
        self.y_step = 0

        self.SPRITES = self.load_sprite_sheeets("MainCharacters", "MaskDude", 32, 32)
    
        self.mask = None
        self.x_direction = 'right'
        self.y_direction = ''
        self.step_count = 0
        self.animation_count = 0
        
    def move(self, dx=0, dy=0):
        self.grid_cells[self.y][self.x].is_current == False
        if dx < 0:
            self.x_direction = "left"
            self.x_step = -self.TILE
            self.x -= 1
        elif dx > 0:
            self.x_direction = "right"
            self.x_step = self.TILE
            self.x += 1
        if dy < 0:
            self.y_direction = "up"
            self.y_step = -self.TILE
            self.y -= 1
        elif dy > 0:
            self.y_direction = "down"
            self.y_step = self.TILE
            self.y += 1
        self.rect.x += self.x_step
        self.rect.y += self.y_step
    
    def get_dynamic(self):
        #MAKING PLAYER LOOK DYNAMIC
        sprite_sheet = 'idle'
            
        sprite_type = sprite_sheet + "_" + self.x_direction
        sprites = self.SPRITES[sprite_type]
        index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.sprite = sprites[index]
        self.animation_count += 1    
        self.masking()
    
    def masking(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)
    
    # draw character everytime we update the position of the character
    def draw(self, window):
        self.get_dynamic()
        window.blit(self.sprite, (self.rect.x, self.rect.y))
        pg.display.update()
        
    def flip(self, sprites):
        return [pg.transform.flip(sprite, True, False) for sprite in sprites]

    def load_sprite_sheeets(self, dir1, dir2, width, height):
        path = os.path.join("assets", dir1, dir2)
        lst_img = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        all_sprites = {}
        
        if self.rows == 100: size = (8, 8)
        # if self.rows == 5: size = (8, 8)
        elif self.rows == 40: size = (16, 16)
        elif self.rows == 20: size = (32, 32)
        
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
            all_sprites[f.replace(".png", "") + "_left"] = self.flip(sprites)

        return all_sprites
        