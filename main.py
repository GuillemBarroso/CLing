"""Main module of the game. Run this module to start the game."""


# Importing pygame module
import pygame

from src.canvas import build_canvas, get_canvas
from src.colors import BLACK, WHITE
from src.command_line import CL
from src.events_definition import CMD_FULL_SCREEN, CMD_REGULAR_SIZE
from src.player import Player
from src.room import Room
from src.screen import Screen

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

        # Enter CL full screen mode
        if event.type == CMD_FULL_SCREEN:
            cmd_line.maximize()

        # Return to regular CL view
        if event.type == CMD_REGULAR_SIZE:
            cmd_line.minimize()

    # Build layout
    build_canvas(canvas=canvas, screen=screen, cmd_line=cmd_line)

    # Draw elements on screen
    if not cmd_line.full_screen:
        screen.surface.fill(WHITE)
        player.move(room_map.walls)
        player.draw(screen.surface)
        room_map.draw(screen.surface)

    # Post user defined events coming from CL
    if cmd_line.user_input == "max":
        pygame.event.post(pygame.event.Event(CMD_FULL_SCREEN))
    elif cmd_line.user_input == "min":
        pygame.event.post(pygame.event.Event(CMD_REGULAR_SIZE))

    # Enable scrolling when CL in full screen mode
    if cmd_line.full_screen == True:
        if len(cmd_line.history) > cmd_line.n_rows_shown:
            cmd_line.scrolling()
            print(cmd_line._scroll_id)
            cmd_line.draw_scroll_bar()

    # Draw elements on cmd_line
    cmd_line.surface.fill(BLACK)
    cmd_line.input.draw(cmd_line.surface)
    cmd_line.draw_history()
    cmd_line.reset_after_enter(events)

    # Draws the surface object to the screen.
    pygame.display.update()
