import os
import random
import math
import pygame as pg
from cell import *
from color import *

PLAYER_VEL = 1 #player velocity
# create a block for player, create animations 
# inherit from the pygame sprite class
# so we could using a method: if the sprites are colliding with each other
window = pg.display.set_mode(RES)

def flip(sprites):
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheeets(dir1, dir2, width, height):
    path = os.path.join("assets", dir1, dir2)
    lst_img = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    all_sprites = {}
    
    if ROW == 100: size = (8, 8)
    elif ROW == 40: size = (16, 16)
    elif ROW == 20: size = (32, 32)
    
    
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
            
class Player(pg.sprite.Sprite): # sprite make it easy to fit pixel perfect

    COLOR = red
    SPRITES = load_sprite_sheeets("MainCharacters", "MaskDude", 32, 32)
    ANIMATION_DELAY = 3
    # define our initialization area
    
    def __init__(self, grid_cells, i, width, height):
        # position of the player
        self.grid_cells = grid_cells
        self.cell = grid_cells[i]
        self.x = self.cell.x
        self.y = self.cell.y
        self.rect = pg.Rect(self.y * TILE, self.x * TILE, width, height) 
        self.x_step = 0
        self.y_step = 0
        self.sliding = False
        
        # denote how fast we move our player
        self.mask = None # ?
        self.x_direction = 'right'
        self.y_direction = ''
        # using times frames re-generate to calc how long have been ?
        #when we start sliding through Ox axis
        self.step_count = 0
        #when we start sliding through Oy axis
        self.animation_count = 0
        
    def move(self, dx=0, dy=0):
        if dx < 0:
            self.x_direction = "left"
            self.x_step = -TILE
            self.x -= 1
        elif dx > 0:
            self.x_direction = "right"
            self.x_step = TILE
            self.x += 1
        if dy < 0:
            self.y_direction = "up"
            self.y_step = -TILE
            self.y -= 1
        elif dy > 0:
            self.y_direction = "down"
            self.y_step = TILE
            self.y += 1
        self.rect.x += self.x_step
        self.rect.y += self.y_step
    
    def update_player(self):
        #update cell of player
        self.cell = self.grid_cells[self.x + self.y * COL]
        #make player look dynamic
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
    
    #function update the correct direction and move 
    # of the player every single frame
    # def update_move(self):
    #     # falling move using gravity cheat :D
    #     self.get_dynamic()
    #     self.fall_count += 1
    
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
        # pg.draw.rect(window, self.COLOR, self.rect)
            
    # def handle_vertical_bar(self, objects, dy):
    #     collided_onj = []
    #     for obj in objects:
    #         if pg.sprite.collide_mask(player, obj)
            
# class Object(pg.sprite.Sprite):
#     def __init__(self, x, y, width, height, name=None):
#         self.rect = pg.Rect(x, y, width, height)
#         self.img = pg.Surface((width, height), pg.SRCALPHA)
#         self.width = width
#         self.height = height
#         self.name = name
    
#     def draw(self, window):
#         window.blit(self.img, (self.rect.x, self.rect.y))

# class Block(Object):
#     def __init__(self, x, y, size):
#         block = get_block(size)
#         self.img.blit(block, (0, 0))
#         self.mask = pg.mask.from_surface(self.img)
        