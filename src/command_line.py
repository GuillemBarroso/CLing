"""Module containing the command line class."""
import pygame

from src.colors import WHITE
from src.eztext import Input


class CL:
    """Class containing all the interactions with the game's command line."""

    def __init__(self, canvas):
        """Initialize command line class."""
        self._width = canvas.get_width()
        self._height = 160
        self._line_height = 30
        self._n_rows_shown = 4
        self._history = []
        self._surface = pygame.Surface((self._width, self._height))
        self._input = Input(
            maxlength=80,
            color=(255, 255, 255),
            y=self._height - self._line_height,
            prompt="> ",
        )
        self._input.focus = True
        # This allows to always be able to type. This can be changed in the future.

    @property
    def surface(self):
        """Return surface of the command line."""
        return self._surface

    @property
    def input(self):
        """Return user input of the command line."""
        return self._input

    @property
    def width(self):
        """Return width of the command line."""
        return self._width

    @property
    def height(self):
        """Return height of the command line."""
        return self._height

    @property
    def line_height(self):
        """Return the height of the command line's line."""
        return self._line_height

    @property
    def history(self):
        """Return the historty of the command line."""
        return self._history

    def draw_history(self):
        """Draw command line's history on command line."""
        for i_line in range(self._n_rows_shown):
            try:
                text = self._input.font.render(self._history[-(i_line + 1)], True, WHITE)
            except IndexError:
                break
            text_rect = text.get_rect()
            text_rect.y = self._height - self._line_height * (i_line + 2)
            self._surface.blit(text, text_rect)

    def reset_after_enter(self, events):
        """Store user input and reset command line with an empty string."""
        user_input = self._input.update(events)
        if user_input:
            # Add input to the command line history
            self._history.append(f"{self._input.prompt}{user_input}")

            # Reset input and print
            self._input.value = ""
            self._input.draw(self._surface)

    def maximize(self, canvas):
        """Maximize command line to fill the entire screen."""
        self._height = canvas.get_width()
        self.draw_history()