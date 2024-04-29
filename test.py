from maze_generator import *
from player import *
from color import *
import pygame as pg

class Game():
    def __init__(self, window):
        self.window = window
        self.grid = Grid(ROW, COL)
        self.maze = Maze_Generator(self.grid)
        self.player = Player(self.grid.grid_cells, 0, TILE, TILE)
        # self.block_size = 96
        # self.blocks = [Block(0, HEIGHT - TILE, self.block_size)]
    def main(self):
        pg.init()  # Initialize pygame
        clock = pg.time.Clock() 
        pg.display.set_caption("Maze - Path Finding") 
        # background, bg_img = self.get_background("Gray")
        run = True
        while run:
            # this line ensure the frame is run 60fps, 
            # set this down if ur computer get bad performance with this fps
            # clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT: #the x red at right top of the window
                    run = False
                    break
            self.loop()
            
        pg.quit() # quit pygame program
        quit() # quit python program

    def loop(self):
            
        self.maze.draw(self.window)
        self.player.update_player()
        self.player.handle_move()
        self.player.draw(self.window)
        
        # for obj in self.blocks:
        #     obj.draw(window)
        pg.display.update()
    
    # generate background
    # def get_background(colorBG):
    #     #load image
    #     img = pg.image.load((os.path.join("assets", "Background", colorBG + ".png")))
    #     _, _, width, height = img.get_rect() #_, _ mean: x, y
    #     background = []
        
    #     for i in range(WIDTH // width + 1):
    #         for j in range(HEIGHT // height + 1):
    #             #denote the position of the top left corner of each tile
    #             pos = (i * width, j * height) # tuple
    #             background.append(pos)
                
    #     return background, img
    
    #handle the move with keys pressed from keyboard 



if __name__ == "__main__":
    window = pg.display.set_mode(RES)  # Set up window
    game = Game(window)
    game.main()
    
