"""Module containing the command line class."""
import pygame
import pygame.locals as locals

from src.cl_text_input import Input
from src.colors import BLACK, WHITE
from src.commands import cmd_dict
from src.cursor import Cursor
from src.events_definition import CMD_FULL_SCREEN, CMD_REGULAR_SIZE, ENTRY_CAVE, VALLEY


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
        self.map_state = "entry_cave"
        self.entry_cave_opened = False
        self.active_player = True
        self.old_command_counter = 0
        self.cursor = Cursor(self._input)

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
        lines = self.split_long_user_input(user_input)

        for line in lines:
            # Add input to the command line history
            self._history.append(f"{self._input.prompt}{line}")
            self._input.prompt = ""

        # Reset input and print
        self._input.value = ""
        self._input.focus = False
        self.check_prompt()
        self.cursor.draw(self._surface)

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
        bar_height = self._height * self._n_rows_shown / len(self._history)
        x_pos = self._width - self._scroll_bar_width
        y_pos = (
            self._height
            - bar_height
            - (self._scroll_id / (self._n_rows_shown - len(self._history)))
            * (self._height - bar_height)
        )
        if not self._full_screen:
            y_pos += self._canvas_height - self._height
        scroll_bar = pygame.Rect((x_pos, y_pos), (self._scroll_bar_width, bar_height))

        pygame.draw.rect(self._canvas, WHITE, scroll_bar, 0, 3)

    def split_long_user_input(self, user_input):
        """Split user input if it is longer than MAX_CL_LENGTH."""
        if len(user_input) > self._MAX_CL_LENGTH:
            lines = []
            line = ""
            split_user_input = user_input.split(" ")
            for i, word in enumerate(split_user_input):
                if len(line) + len(word) > self._MAX_CL_LENGTH:
                    lines.append(line[1:])
                    line = ""
                line += f" {word}"
                if i == len(split_user_input) - 1:
                    lines.append(line[1:])
        else:
            lines = [user_input]
        return lines

    @staticmethod
    def get_command_from_user_input(user_input):
        """Return main command and the arguments introduced by the user."""
        for command in cmd_dict.keys():
            index_ini = user_input.find(command)
            if index_ini == 0:
                break
        else:
            message = f"Command '{user_input}' is not a valid command"
            return None, None, message
        assert index_ini == 0, "The command must be introduced in the first place"
        index_end = len(command)
        return user_input[index_ini:index_end], user_input[index_end + 1 :], ""

    def write_command_response(self, prompt="  "):
        """Write on CL the content of input.value and store it in CL history."""
        if self.input.value:
            self.input.focus = False
            self.input.prompt = prompt
            self.reset_after_enter(self.input.value)

    def trigger_user_commands(self, player, sprites):
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
            command.execute(self, arguments, player, sprites)

    def scroll_history(self):
        """Enable scrolling when CL in full screen mode."""
        if len(self.history) > self.n_rows_shown:
            if not self._input.focus:
                self.scrolling()
            self.draw_scroll_bar()

    def resolve_user_commands(self, player, sprites):
        """Resolve commands introduced by the user via command line."""
        self.reset_after_enter(self._user_input)
        self.trigger_user_commands(player, sprites)

    def get_command_history(self):
        """Get old commands from the entire CL history."""
        self._command_history = []
        for line in self._history:
            if line[0] == ">":
                self._command_history.append(line[2:])

    def recover_old_commands(self, event):
        """Use up and down keys to recover old commands stored in history."""
        if self._input.focus:
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_UP:
                    self.old_command_counter += 1
                elif event.key == locals.K_DOWN:
                    self.old_command_counter -= 1

        # Get only the commands from CL history
        self.get_command_history()

        # Check for incompatible indices
        if self.old_command_counter < 0:
            self._input.value = ""
            self.old_command_counter = 0
        elif self.old_command_counter > len(self._command_history):
            self.old_command_counter = len(self._command_history)

        # Apply index and display command
        if not self.old_command_counter == 0:
            self._input.value = self._command_history[-self.old_command_counter]

    def activate_cl_commands(self, event, level):
        """Activate CL commands coming from events."""
        # Enter CL full screen mode
        if event.type == CMD_FULL_SCREEN:
            self.maximize()
            self._full_screen = True

        # Return to regular CL view
        if event.type == CMD_REGULAR_SIZE:
            self.minimize()
            self._full_screen = False
            self.input.focus = False

        if event.type == VALLEY:
            self.previous_map_state = self.map_state
            self.map_state = "valley"
            level.sprites_setup(level.valley_path)
            level.create_map(level.valley_layouts, level.valley_graphics)

        if event.type == ENTRY_CAVE:
            self.previous_map_state = self.map_state
            self.map_state = "entry_cave"
            level.sprites_setup(level.entry_cave_path)
            level.create_map(level.entry_cave_layouts)

    def run(self, room_text):
        """Run CL methods."""
        # Run methods that control the CL behaviour
        self.scroll_history()

        # Run methods that draw in the CL
        self._surface.fill(BLACK)
        self.draw_history()
        # room_text.update_room_first_entry()

        # Run CL specific methods when in focus mode
        if self.input.focus:
            self.cursor.run()
            self.cursor.draw(self.surface)

    def run_event(self, event, level):
        """Run CL methods that interact with event."""
        if self.input.focus:
            self.cursor.run_event(event)
        self.activate_cl_commands(event, level)
        self.check_focus(event)
        self.recover_old_commands(event)
        self._user_input = self._input.update(event, self.cursor)
        if self._user_input and self.active_player:
            self.cursor.init_selection_variables()
            self.resolve_user_commands(level.player, level.interactable_sprites)
