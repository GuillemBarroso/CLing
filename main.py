"""Main module of the game. Run this module to start the game."""


# Importing pygame module
import pygame

from src.canvas import get_canvas
from src.colors import BLACK
from src.player import Player
from src.terminal import Terminal

# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# Add caption in the window
pygame.display.set_caption("Game")

# Initializing the clock. Clocks are used to track and control the frame-rate of a game
clock = pygame.time.Clock()

# Initialize objects
canvas = get_canvas()
player = Player()
terminal = Terminal(canvas=canvas)

# Creating an Infinite loop
run = True
while run:
    # Set the frame rates to 60 fps
    clock.tick(60)

    canvas.fill((255, 255, 255))

    # Iterate over the list of Event objects that was returned by pygame.event.get() method.
    events = pygame.event.get()
    for event in events:
        # Closing the window and program if the type of the event is QUIT
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        # Changing the value of the direction variable
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.direction = "E"
            elif event.key == pygame.K_LEFT:
                player.direction = "W"
            elif event.key == pygame.K_UP:
                player.direction = "N"
            elif event.key == pygame.K_DOWN:
                player.direction = "S"

    player.move()
    player.draw(canvas)

    user_input = terminal.input.update(events)

    canvas.blit(terminal.surface, (0, canvas.get_height() - terminal.height))
    terminal.surface.fill(BLACK)
    terminal.input.draw(terminal.surface)

    terminal.draw_history()

    if user_input:
        terminal.reset_after_enter(user_input)

    # Draws the surface object to the screen.
    pygame.display.update()
