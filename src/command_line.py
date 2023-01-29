"""Module containing the command line class."""
import pygame
import pygame.locals as locals

from src.colors import WHITE
from src.eztext import Input


class CL:
    """Class containing all the interactions with the game's command line."""

    def __init__(self, canvas):
        """Initialize command line class."""
        self._canvas = canvas
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
        self._user_input = ""
        self._scroll_id = 0
        self._scroll_bar_width = 10
        self._MAX_CL_LENGTH = 160

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

        Subtract 1 because of the active input line used by the user.
        """
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

    @property
    def n_rows_shown(self):
        """Return number of shown rows for CL history."""
        return self._n_rows_shown

    def draw_history(self):
        """Draw command line's history on command line."""
        for i_line in range(self._n_rows_shown):
            try:
                text = self._input.font.render(
                    self._history[-(i_line + 1) + self._scroll_id], True, WHITE
                )
            except IndexError:
                break
            text_rect = text.get_rect()
            text_rect.y = self._height - self._line_height * (i_line + 2)
            self._surface.blit(text, text_rect)

    def reset_after_enter(self, user_input):
        """Store user input and reset command line with an empty string."""
        lines = self.split_long_user_input(user_input, self._MAX_CL_LENGTH)

        for line in lines:
            # Add input to the command line history
            self._history.append(f"{self._input.prompt}{line}")

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
        self._scroll_id = 0

    def minimize(self):
        """Minimise command line to its original size."""
        self._height = self._height_ref
        self._n_rows_shown = self._n_rows_shown_ref
        self._full_screen = False
        self._surface = self._get_surface(self._width, self._height)
        self._input = self._get_input(self._height)
        self._input.focus = True
        self._scroll_id = 0

    def scrolling(self):
        """Scroll up and down through CL history when in full scren mode."""
        key_pressed_is = pygame.key.get_pressed()
        if key_pressed_is[locals.K_UP] and not key_pressed_is[locals.K_DOWN]:
            if self._scroll_id > (self._n_rows_shown - len(self._history)):
                self._scroll_id -= 1
        if key_pressed_is[locals.K_DOWN] and not key_pressed_is[locals.K_UP]:
            if self._scroll_id < 0:
                self._scroll_id += 1

    def draw_scroll_bar(self):
        """Draw scroll bar indicating which part of the history is currently being displayed."""
        bar_height = self._canvas_height * self._n_rows_shown / len(self._history)
        y_pos = self._width - self._scroll_bar_width
        x_pos = (
            self._height
            - bar_height
            - (self._scroll_id / (self._n_rows_shown - len(self._history)))
            * (self._height - bar_height)
        )
        scroll_bar = pygame.Rect((y_pos, x_pos, self._scroll_bar_width, bar_height))

        pygame.draw.rect(self._canvas, WHITE, scroll_bar)

    @staticmethod
    def split_long_user_input(user_input, MAX_CL_LENGTH):
        """Split user input if it is longer than MAX_CL_LENGTH."""
        if len(user_input) > MAX_CL_LENGTH:
            # TODO: split only in spaces. Do not split words by half.
            lines = [
                user_input[i : i + MAX_CL_LENGTH]
                for i in range(0, len(user_input), MAX_CL_LENGTH)
            ]
        else:
            lines = [user_input]
        return lines
