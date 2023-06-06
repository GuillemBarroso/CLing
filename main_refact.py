"""Main file of the game."""

import sys

import pygame

from src.canvas import build_canvas, get_canvas
from src.colors import BLACK
from src.command_line import CL
from src.execute_commands import activate_cl_commands
from src.level import Level
from src.screen import Screen
from src.settings import FPS, WATER_COLOR


class Game:
    """Game object."""

    def __init__(self):
        """Initialize pygame and set caption."""
        pygame.init()
        pygame.display.set_caption("CLing")
        self.clock = pygame.time.Clock()

        # Create canvas with a screen and a command line
        self.canvas = get_canvas()
        self.cmd_line = CL(canvas=self.canvas)
        self.screen = Screen(self.canvas, self.cmd_line)

        # Initialize Level object with all game interactions
        self.level = Level(self.screen, self.cmd_line)

        # Sound effect
        main_sound = pygame.mixer.Sound("src/audio/main.ogg")
        main_sound.set_volume(0.1)
        main_sound.play(loops=-1)

    def run(self):
        """Run game."""
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check for events interacting with the CL
                activate_cl_commands(event, self.cmd_line)
                self.cmd_line.check_focus(event)

                # Pause game and toggle menu screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            # Build layout
            build_canvas(self.canvas, self.screen, self.cmd_line)

            # Draw on screen
            self.screen.surface.fill(WATER_COLOR)
            self.level.run()

            # Enable scrolling when CL in full screen mode
            if self.cmd_line.full_screen == True:
                if len(self.cmd_line.history) > self.cmd_line.n_rows_shown:
                    self.cmd_line.scrolling()
                    self.cmd_line.draw_scroll_bar()

            # Draw on command line
            self.cmd_line.surface.fill(BLACK)
            self.cmd_line.input.draw(self.cmd_line.surface)
            self.cmd_line.draw_history()
            self.cmd_line._user_input = self.cmd_line._input.update(events)
            if self.cmd_line._user_input:
                self.cmd_line.reset_after_enter(self.cmd_line._user_input)
                # trigger_user_commands(self.cmd_line, player)

            # Update
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
