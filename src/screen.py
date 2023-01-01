"""Module containing the screen class."""

import pygame


class Screen:
    """Screen class.

    The screen is the section of the canvas that is not covered by the terminal.

    """

    def __init__(self, canvas, terminal):
        """Initialize screen class."""
        canvas_height = canvas.get_height()
        terminal_height = terminal.height
        self._surface = pygame.Surface(
            (canvas.get_width(), canvas_height - terminal_height)
        )

    @property
    def surface(self):
        """Return surface of the screen."""
        return self._surface
