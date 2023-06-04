"""Main file of the game."""

import sys

import pygame

from src.canvas import build_canvas, get_canvas
from src.colors import BLACK
from src.command_line import CL
from src.level import Level
from src.screen import Screen
from src.settings import FPS


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

        self.level = Level(self.screen)

    def run(self):
        """Run game."""
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.cmd_line.check_focus(event)

            # Build layout
            build_canvas(self.canvas, self.screen, self.cmd_line)

            # Draw on screen
            self.screen.surface.fill(BLACK)
            self.level.run()

            # Draw on command line
            self.cmd_line.surface.fill(BLACK)
            self.cmd_line.input.draw(self.cmd_line.surface)
            self.cmd_line.draw_history()
            self.cmd_line._user_input = self.cmd_line._input.update(events)
            if self.cmd_line._user_input:
                self.cmd_line.reset_after_enter(self.cmd_line._user_input)
                # trigger_user_commands(cmd_line, player)

            # Update
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()