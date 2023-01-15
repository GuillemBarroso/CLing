"""Module containing the command line class."""
import pygame

from src.colors import WHITE
from src.eztext import Input


class CL:
    """Class containing all the interactions with the game's command line."""

    def __init__(self, canvas):
        """Initialize command line class."""
        self._width = canvas.get_width()
        self._canvas_height = canvas.get_height()
        self._height = 160
        self._line_height = 30
        self._n_rows_shown = self._get_n_rows_shown(self._height, self._line_height)
        self._n_rows_shown_ref = self._n_rows_shown
        self._height_ref = self._height
        self._history = []
        self._surface = self._get_surface(self._width, self._height)
        self._input = self._get_input(self._height)
        self._input.focus = True
        # This allows to always be able to type. This can be changed in the future.
        self._full_screen = False
        self._user_input = ''

    def _get_input(self, vertical_location):
        """Return text Input object."""
        return Input(
            maxlength=80,
            color=WHITE,
            y=(vertical_location - self._line_height),
            prompt="> ",
        )

    @staticmethod
    def _get_surface(width, height):
        """Return pygame Surface with a certain width and height."""
        return pygame.Surface((width, height))

    @staticmethod
    def _get_n_rows_shown(height, line_height):
        """Return the number of lines that fit the space of the terminal.
        Subtract 1 because of the active input line used by the user."""
        return height // line_height - 1

    @property
    def surface(self):
        """Return surface of the command line."""
        return self._surface

    @property
    def input(self):
        """Return user input of the command line."""
        return self._input

    @property
    def user_input(self):
        """Return command line user input after pressing return key."""
        return self._user_input

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

    @property
    def full_screen(self):
        """Return a boolean indicating if the command line is in full screen mode."""
        return self._full_screen

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
        self._user_input = self._input.update(events)
        if self._user_input:
            # Add input to the command line history
            self._history.append(f"{self._input.prompt}{self._user_input}")

            # Reset input and print
            self._input.value = ""
            self._input.draw(self._surface)

    def maximize(self):
        """Maximize command line to fill the entire screen."""
        self._height = self._canvas_height
        self._n_rows_shown = self._get_n_rows_shown(self._height, self._line_height)
        self._full_screen = True
        self._surface = self._get_surface(self._width, self._canvas_height)
        self._input = self._get_input(self._height)
        self._input.focus = True

    def minimize(self):
        """Minimise command line to its original size."""
        self._height = self._height_ref
        self._n_rows_shown = self._n_rows_shown_ref
        self._full_screen = False
        self._surface = self._get_surface(self._width, self._height)
        self._input = self._get_input(self._height)
        self._input.focus = True