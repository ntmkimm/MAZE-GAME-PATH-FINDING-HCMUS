import os
import random
import math
import pygame as pg
from cell import *
from color import *
            
class Player(pg.sprite.Sprite, Cell): # sprite make it easy to fit pixel perfect

    ANIMATION_DELAY = 3
    # define our initialization area
    
    def __init__(self, grid_cells, init_pos, goal_pos, tile):
        # position of the player
        self.grid_cells = grid_cells
        self.rows = len(self.grid_cells)
        self.cols = self.rows
        self.TILE = tile
        self.cell = self.grid_cells[init_pos[0]][init_pos[1]]
        self.x = self.cell.x # col
        self.y = self.cell.y # row
        self.init_maze_x = self.grid_cells[0][0].init_maze_x
        self.init_maze_y = self.grid_cells[0][0].init_maze_y
        self.rect = pg.Rect(self.init_maze_x + self.x * self.TILE, self.init_maze_y + self.y * self.TILE, self.TILE, self.TILE)
        self.x_step = 0
        self.y_step = 0
        self.sliding = False
        self.SPRITES = self.load_sprite_sheeets("MainCharacters", "MaskDude", 32, 32)
    
        self.mask = None
        self.x_direction = 'right'
        self.y_direction = ''
        self.step_count = 0
        self.animation_count = 0
        
    def move(self, dx=0, dy=0):
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
    
    def update_player(self):
        #update cell of player
        self.cell.is_start = False
        self.cell = self.grid_cells[self.y][self.x]
        self.cell.is_start = True
        self.get_dynamic()
    
    def handle_move(self):
        self.x_step = 0
        self.y_step = 0
        key = pg.key.get_pressed()
        # set to 0 cause we just want the player move when we pressed the key
        if (key[pg.K_LEFT] or key[pg.K_a]) and self.cell.bars['left'] == False:
            self.move(dx = -1)
        elif (key[pg.K_RIGHT] or key[pg.K_d]) and self.cell.bars['right'] == False:
            self.move(dx = 1)
        elif (key[pg.K_UP] or key[pg.K_w]) and self.cell.bars['top'] == False:
            self.move(dy = -1)
        elif (key[pg.K_DOWN] or key[pg.K_s]) and self.cell.bars['bottom'] == False:
            self.move(dy = 1)
    
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
        window.blit(self.sprite, (self.rect.x, self.rect.y))
        
    def flip(self, sprites):
        return [pg.transform.flip(sprite, True, False) for sprite in sprites]

    def load_sprite_sheeets(self, dir1, dir2, width, height):
        path = os.path.join("assets", dir1, dir2)
        lst_img = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        all_sprites = {}
        
        if self.rows == 100: size = (8, 8)
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
        