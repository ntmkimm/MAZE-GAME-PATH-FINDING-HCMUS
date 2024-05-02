import pygame as pg 
from maze_generator import *

class Recursive:
    def __init__(self, grid, maze, player):
        self.grid = grid # class grid
        self.maze = maze # class maze
        self.player = player # class player
        
        