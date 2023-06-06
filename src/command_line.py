"""Module containing the command line class."""
import pygame
import pygame.locals as locals

from src.colors import BLACK, WHITE
from src.commands import cmd_dict
from src.eztext import Input


class CL:
    """Class containing all the interactions with the game's command line."""

    def __init__(self, canvas):
        """Initialize command line class."""
        self._canvas = canvas
        self._width = canvas.get_width()
        self._canvas_height = canvas.get_height()
        self._height = 160
        self._line_height = 25
        self._n_rows_shown = self._get_n_rows_shown(self._height, self._line_height)
        self._n_rows_shown_ref = self._n_rows_shown
        self._height_ref = self._height
        self._history = []
        self._surface = self._get_surface(self._width, self._height)
        self._input = self._get_input(self._height)
        self._input.focus = False
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
            prompt="",
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

    def check_prompt(self):
        """Check the CL prompt."""
        if self._input.focus:
            self._input.prompt = "> "
        else:
            self._input.prompt = ""

    def check_focus(self, event):
        """Check whether CL is on focus mode or not."""
        if not self.full_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self._input.focus == False:
                    self._input.focus = True
                elif (
                    event.key == pygame.K_RETURN
                    and self._input.focus == True
                    and self._input.value == ""
                ):
                    self._input.focus = False
                if event.key == pygame.K_ESCAPE:
                    self._input.focus = False
                    self._input.value = ""

        self.check_prompt()

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
            self._input.prompt = ""

        # Reset input and print
        self._input.value = ""
        if not self.full_screen:
            self._input.focus = False
        self.check_prompt()
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

    @staticmethod
    def get_command_from_user_input(user_input):
        """Return main command and the arguments introduced by the user."""
        for command in cmd_dict.keys():
            index_ini = user_input.find(command)
            if not index_ini == -1:
                break
        else:
            message = f"Command '{user_input}' is not a valid command"
            return None, None, message
        assert index_ini == 0, "The command must be introduced in the first place"
        index_end = len(command)
        return user_input[index_ini:index_end], user_input[index_end:], ""

    def trigger_user_commands(self, player):
        """Capture user inputs that require a response message in the CL."""
        input = self.input

        user_command, arguments, message = self.get_command_from_user_input(
            self.user_input
        )
        if message:
            input.value = message
            self.reset_after_enter(self.input.value)
        else:
            command = cmd_dict[user_command]
            command.execute(self, arguments, player)

    def scrolling_full_screen(self):
        """Enable scrolling when CL in full screen mode."""
        if self.full_screen == True:
            if len(self.history) > self.n_rows_shown:
                self.scrolling()
                self.draw_scroll_bar()

    def draw(self):
        """Draw on command line."""
        self.surface.fill(BLACK)
        self.input.draw(self.surface)
        self.draw_history()

    def resolve_user_commands(self, events, player):
        """Resolve commands introduced by the user via command line."""
        self._user_input = self._input.update(events)
        if self._user_input:
            self.reset_after_enter(self._user_input)
            self.trigger_user_commands(player)
