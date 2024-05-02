import pygame as pg 
from maze_generator import *

class Recursive:
    def __init__(self, init_pos: int, maze, player):
        self.init_pos = init_pos # 
        self.maze = maze # class maze from maze_generator
        self.player = player # class player
        
    def find_way(self):
        self.grid
        res = []
        