"""Main file of the game."""

import sys

import pygame

from src.canvas import build_canvas, get_canvas
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
        main_sound.set_volume(0.01)
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

            # Build layout screen + command line
            build_canvas(self.canvas, self.screen, self.cmd_line)

            # Draw and update on screen and command line
            self.screen.surface.fill(WATER_COLOR)
            self.level.run(events)

            # Update
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
