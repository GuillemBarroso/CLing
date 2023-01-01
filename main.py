"""Main module of the game. Run this module to start the game."""


# Importing pygame module
import pygame

from src.canvas import build_canvas, get_canvas
from src.colors import BLACK, WHITE
from src.player import Player
from src.room import Room
from src.screen import Screen
from src.terminal import Terminal

# Initiate pygame and give permission to use pygame's functionality.
pygame.init()

# Add caption in the window
pygame.display.set_caption("Game")

# Initializing the clock. Clocks are used to track and control the frame-rate of a game
clock = pygame.time.Clock()

# Initialize objects
canvas = get_canvas()
player = Player()
terminal = Terminal(canvas=canvas)
screen = Screen(canvas, terminal)
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
    build_canvas(canvas, screen, terminal)
    screen.surface.fill(WHITE)
    terminal.surface.fill(BLACK)

    # Draw elements on screen
    player.move(room_map.walls)
    player.draw(screen.surface)
    room_map.draw(screen.surface)

    # Draw elements on terminal
    terminal.input.draw(terminal.surface)
    terminal.draw_history()
    terminal.reset_after_enter(events)

    # Draws the surface object to the screen.
    pygame.display.update()
