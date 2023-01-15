"""Main module of the game. Run this module to start the game."""


# Importing pygame module
import pygame

from src.canvas import build_canvas, get_canvas
from src.colors import BLACK, WHITE
from src.player import Player
from src.room import Room
from src.screen import Screen
from src.command_line import CL

# Initiate pygame and give permission to use pygame's functionality.
pygame.init()

# Add caption in the window
pygame.display.set_caption("CLing")

# Initializing the clock. Clocks are used to track and control the frame-rate of a game
clock = pygame.time.Clock()

# Initialize objects
canvas = get_canvas()
player = Player()
cmd_line = CL(canvas=canvas)
screen = Screen(canvas, cmd_line)
room_map = Room(screen=screen)

# Creating an Infinite loop
run = True
while run:
    # Set the frame rates to 60 fps
    clock.tick(60)

    # Iterate over the list of Event objects that was returned by pygame.event.get() method.
    events = pygame.event.get()
    for event in events:
        # Closing the window and program if the type of the event is QUIT
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    # Build layout
    build_canvas(canvas=canvas, screen=screen, cmd_line=cmd_line)
    screen.surface.fill(WHITE)
    cmd_line.surface.fill(BLACK)

    # Draw elements on screen
    player.move(room_map.walls)
    player.draw(screen.surface)
    room_map.draw(screen.surface)

    # Draw elements on cmd_line
    cmd_line.maximize()
    cmd_line.input.draw(cmd_line.surface)
    cmd_line.draw_history()
    cmd_line.reset_after_enter(events)

    # Draws the surface object to the screen.
    pygame.display.update()
