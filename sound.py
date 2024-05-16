import pygame as pg
import os
from button import *

class Sound():
    def __init__(self):
        self.op2 = 0
        self.op = 0
        self.sound1 = pg.mixer.Sound(os.path.join("sound", "walk.mp3"))
        self.sound2 = pg.mixer.Sound(os.path.join("sound", "select.mp3"))
        self.sound = pg.mixer.music.load(os.path.join("sound", "Background_Sound.mp3"))
        self.sound3 = pg.mixer.Sound(os.path.join("sound", "victory.mp3"))
        self.vol1 = 0
        self.vol2 = 0
        self.pos1 = 570
        self.pos2 = 570
        self.sound1.set_volume(0.5)
        self.sound2.set_volume(0.5)
        self.sound3.set_volume(0.5)
        self.steps = 0
        self.start = 0
        self.time = 0

    def sound_effect(self, mark):
        if self.op % 2 == 0:
            if mark == 1:
                self.sound1.set_volume(self.sound1.get_volume() + self.vol1)
                self.sound1.play()
            elif mark == 2:
                self.sound2.set_volume(self.sound2.get_volume() + self.vol1)
                self.sound2.play()
            elif mark == 3:
                self.sound3.set_volume(self.sound2.get_volume() + self.vol1)
                self.sound3.play()

    def sound_select(self, lis):
        mouse_pos = pg.mouse.get_pos()
        for i in lis:
            if i.is_pointed(mouse_pos):
                self.sound_effect(2)


    def background_sound(self, mark):
        if mark == 0:
            pg.mixer.music.load(os.path.join("sound", "Background_Sound.mp3"))
            pg.mixer.music.set_volume(0.5)
            pg.mixer.music.play(-1)
        if mark % 2 == 1:
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()