import pygame as pg

def transition(window, color, duration, fade_out=True):
    """
    Perform a fade-out or fade-in transition.

    Args:
        window: The Pygame window surface.
        color: The color of the transition (e.g., (0, 0, 0) for black).
        duration: Duration of the transition in milliseconds.
        fade_out: True for fade-out, False for fade-in.
    """
    fade_surface = pg.Surface(window.get_size())
    fade_surface.fill(color)
    
    clock = pg.time.Clock()
    alpha = 255 if fade_out else 0
    alpha_step = 255 / duration * clock.tick() if duration != 0 else 1  # Use a default value to prevent division by zero

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        
        if fade_out:
            alpha -= alpha_step
            if alpha <= 0:
                running = False
        else:
            alpha += alpha_step
            if alpha >= 255:
                running = False
        
        fade_surface.set_alpha(max(0, min(255, int(alpha))))
        window.blit(fade_surface, (0, 0))
        pg.display.update()
        clock.tick(60)

    # Ensure the final state
    if fade_out:
        fade_surface.set_alpha(0)
    else:
        fade_surface.set_alpha(255)
    window.blit(fade_surface, (0, 0))
    pg.display.update()

# Example usage in a game
def run_game():
    pg.init()
    window = pg.display.set_mode((1200, 820))
    pg.display.set_caption("Maze - Path Finding")
    white = (255, 255, 255)
    black = (0, 0, 0)
    pink = (255, 192, 203)
    
    # Initial game setup here...

    transition(window, black, 2000, fade_out=False)  # Fade in at the start of the game

    # Main game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                running = False
                break

        # Game logic and rendering here...

        pg.display.update()

    transition(window, black, 2000, fade_out=True)  # Fade out at the end of the game
    pg.quit()

if __name__ == "__main__":
    run_game()
