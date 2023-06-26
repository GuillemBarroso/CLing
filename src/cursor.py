"""Module containing the Cursor class, controlling the CL cursor."""

import pygame
import pygame.locals as locals

from src.colors import BLACK, WHITE
from src.text import Text


class Cursor:
    """Cursor class that operates the CL cursor."""

    def __init__(self, input):
        """Initualize Cursor class."""
        self.input = input

        # Initialize
        self.delete_ini_pause = 0
        self.delete_fast_pause = 0
        self.move_ini_pause = 0
        self.move_fast_pause = 0
        self.position = 0
        self.blinking_active = False
        self.blinking_bool = False
        self.blinking_past = 0
        self.blinking_start = 0
        # self.remove_letters_bool = True
        self.left_position = 0
        self.prev_typing_len = 0
        self.new_typing_len = 0

        # Set constants
        self.BLINKING_WIDTH = 2
        self.BLINKING_SPEED = 200
        self.INI_PAUSE = 20
        self.FAST_PAUSE = 1

        self.init_selection_variables()

    def init_selection_variables(self):
        """Initialize selection variables so they are not polluted."""
        self.select_start = 0
        self.select_end = 0
        self.delta_typing = 0
        self.selection = ""
        self.past_ongoing = False
        self.select_mode = ""
        self.start = 0
        self.end = 0
        self.disp_start = 0
        self.disp_end = 0
        self.state_start = 0
        self.state_end = 0
        self.text_modes_list = [
            "shifted",
            "moving_arrows",
            "select_ongoing",
            "select_maintain",
            "select_substitute",
            "select_delete",
        ]
        self.text_modes = dict.fromkeys(self.text_modes_list, False)

    def set_cl_modes(self, boolean, *args):
        """Set CL modes to True or False."""
        for arg in args:
            if arg == "all":
                for mode in self.text_modes_list:
                    self.text_modes[mode] = boolean
            else:
                self.text_modes[arg] = boolean

    def blinking_cursor_cooldown(self):
        """Implement cooldowns for the blinking cursor."""
        current_time = pygame.time.get_ticks()
        if not self.blinking_active:
            if current_time - self.blinking_past >= self.BLINKING_SPEED:
                self.blinking_active = True

    def update_cooldowns(self):
        """Update blinking cursor cooldowns."""
        # Check blinking cooldowns
        if self.blinking_bool:
            self.blinking_start = pygame.time.get_ticks()
            self.blinking_bool = False

        # Reset after cooldowns
        current_time = pygame.time.get_ticks()
        if not (
            self.text_modes["select_maintain"] or self.text_modes["select_ongoing"]
        ):
            if current_time - self.blinking_start >= self.BLINKING_SPEED:
                self.blinking_past = pygame.time.get_ticks()
                self.blinking_active = False
                self.blinking_bool = True
                self.blinking_start = 0

    def fast_move(self, keys_pressed):
        """Enable pressing left and right keys to go through the user's input."""
        if self.move_ini_pause == self.INI_PAUSE and keys_pressed[locals.K_LEFT]:
            self.move_ini_pause = self.INI_PAUSE
            self.position -= 1
        elif self.move_ini_pause == self.INI_PAUSE and keys_pressed[locals.K_RIGHT]:
            self.move_ini_pause = self.INI_PAUSE
            self.position += 1
        elif self.move_fast_pause == self.FAST_PAUSE and keys_pressed[locals.K_LEFT]:
            self.move_fast_pause = 0
            self.position -= 1
        elif self.move_fast_pause == self.INI_PAUSE and keys_pressed[locals.K_RIGHT]:
            self.move_fast_pause = 0
            self.position += 1
        elif keys_pressed[locals.K_LEFT] or keys_pressed[locals.K_RIGHT]:
            self.move_ini_pause += 1
        elif self.move_ini_pause == self.INI_PAUSE and keys_pressed[locals.K_LEFT]:
            self.move_fast_pause += 1
        elif self.move_ini_pause == self.INI_PAUSE and keys_pressed[locals.K_RIGHT]:
            self.move_fast_pause += 1
        else:
            self.move_ini_pause = 0
            self.move_fast_pause = 0

    def fast_delete(self, keys_pressed):
        """Add ability to hold down delete key and delete text."""
        if self.delete_ini_pause == self.INI_PAUSE and keys_pressed[locals.K_BACKSPACE]:
            self.input.value, self.position = self.text.delete()
            self.delete_ini_pause = self.INI_PAUSE
            self.delete_fast_pause = 0
        elif (
            self.delete_fast_pause == self.FAST_PAUSE
            and keys_pressed[locals.K_BACKSPACE]
        ):
            self.input.value, self.position = self.text.delete()
            self.delete_fast_pause = 0
        # TODO: FIX THIS 5 BELOW: THE PROBLEM IS THAT AFTER THE EVENT select.delete is over
        # THE BACKSPACE KEY IS STILL BEING TRIGGERED. NOT SURE HOW TO FIX IT.
        elif keys_pressed[locals.K_BACKSPACE] and self.delete_ini_pause == 5:
            self.input.value, self.position = self.text.delete()
            self.delete_ini_pause += 1
        elif keys_pressed[locals.K_BACKSPACE]:
            self.delete_ini_pause += 1
        elif (
            self.delete_ini_pause == self.INI_PAUSE and keys_pressed[locals.K_BACKSPACE]
        ):
            self.delete_fast_pause += 1
        else:
            self.delete_ini_pause = 0
            self.delete_fast_pause = 0

    def track_cursor_movement(self):
        """Track the cursor on the CL."""
        # Get changes done by typing
        input_length = len(self.input.value)

        # Get changes done with the left and right arrows
        if self.position > 0:
            self.position = 0
        if self.position < -len(self.input.value):
            self.position = -len(self.input.value)

        left_position = input_length + self.position
        if left_position < 0:
            left_position = 0

        return left_position, input_length

    def running_selection(self, pressed):
        """Get pressed keys at each frame."""
        if (
            self.text_modes["select_maintain"]
            or self.text_modes["select_substitute"]
            or self.text_modes["select_delete"]
        ):
            # Trick to avoid overwriting the variables when selecting
            # characters in inverse mode (from left to right).
            # This happens due to the fact that "run_event" are executed
            # before, so we always go one iteration late.
            self.select_start = self.old_select_start
            self.select_end = self.old_select_end
        else:
            # Normal behaviour to obtain the selection positions
            if pressed[locals.K_LSHIFT] or pressed[locals.K_RSHIFT]:
                self.select_start = self.position
            else:
                self.select_end = self.position

        self.old_select_start = self.select_start
        self.old_select_end = self.select_end

    def run_event(self, event):
        """Update based on an event."""
        if event.type == locals.KEYDOWN:
            if event.key == locals.K_LSHIFT or event.key == locals.K_RSHIFT:
                # Enter shited mode
                self.set_cl_modes(True, "shifted")

            if event.key == locals.K_LEFT or event.key == locals.K_RIGHT:
                # Moving with left or right arrows
                self.set_cl_modes(True, "moving_arrows")

            if self.text_modes["shifted"] and self.text_modes["moving_arrows"]:
                # Start a selection by pressing shift and arrows
                self.set_cl_modes(True, "select_ongoing")
                self.set_cl_modes(False, "select_maintain")

            elif self.text_modes["select_maintain"] and self.text_modes["shifted"]:
                # Modify an maintained selection pressing shift
                self.set_cl_modes(True, "select_ongoing")
                self.set_cl_modes(False, "select_maintain")

            elif (
                self.text_modes["select_maintain"]
                and self.text_modes["moving_arrows"]
                and not self.text_modes["shifted"]
            ):
                # Remove maintained selection by moving arrows without shift
                self.set_cl_modes(False, "all")

            elif self.text_modes["select_maintain"] and event.key == locals.K_BACKSPACE:
                # Delete maintained selection with backspace
                self.set_cl_modes(True, "select_delete")
                self.set_cl_modes(
                    False, "select_substitute", "select_maintain", "select_substitute"
                )

            elif self.text_modes["select_maintain"] and self.text_modes["shifted"]:
                # Substitute maintained selection by an uppercase letter
                self.set_cl_modes(True, "select_substitute")
                self.set_cl_modes(
                    False, "select_delete", "select_maintain", "select_ongoing"
                )

            elif self.text_modes["select_maintain"]:
                # Substitute maintained selection by a lowercase letter
                self.set_cl_modes(True, "select_substitute")
                self.set_cl_modes(
                    False, "select_delete", "select_maintain", "select_ongoing"
                )

            elif (
                self.text_modes["select_maintain"]
                and self.text_modes["shifted"]
                and self.text_modes["moving_arrows"]
            ):
                # Start modifying a selection with shift and moving arrows
                self.set_cl_modes(True, "select_ongoing")
                self.set_cl_modes(
                    False, "select_delete", "select_maintain", "select_ongoing"
                )

        if event.type == locals.KEYUP:
            if event.key == locals.K_LSHIFT or event.key == locals.K_RSHIFT:
                # Release shift button
                self.set_cl_modes(False, "shifted")

            if event.key == locals.K_LEFT or event.key == locals.K_RIGHT:
                # Release arrows button
                self.set_cl_modes(False, "moving_arrows")

            if (
                self.text_modes["select_ongoing"]
                and not self.text_modes["shifted"]
                and not self.text.start == self.text.end == 0
            ):
                # Maintain selection when releasing shift
                self.set_cl_modes(True, "select_maintain")
                self.set_cl_modes(
                    False, "select_ongoing", "select_substitute", "select_delete"
                )
            elif (
                self.text_modes["select_ongoing"] or self.text_modes["select_maintain"]
            ) and self.text.start == self.text.end:
                # Turn off ongoing mode if there is no selection
                self.set_cl_modes(False, "select_ongoing")

    def create_rectangle(self):
        """Create white rectangle with thin width or with the select_text width if select."""
        # Get text based on cursor position
        delta_text = self.input.font.render(
            self.input.prompt + self.input.value[: self.left_position], 1, WHITE
        )

        # Render selection text, whether is a empty string or not
        select_text = self.input.font.render(self.selection, 1, WHITE)

        # Create rectangle
        if self.text_modes["select_maintain"] or self.text_modes["select_ongoing"]:
            if self.text.is_inverted:
                blinking_rect_x = (
                    self.input.x + delta_text.get_width() - select_text.get_width()
                )
            else:
                blinking_rect_x = self.input.x + delta_text.get_width()
        else:
            blinking_rect_x = self.input.x + delta_text.get_width()

        blinking_rect_y = self.input.y

        if self.text_modes["select_maintain"] or self.text_modes["select_ongoing"]:
            blinking_rect_width = select_text.get_width()
        else:
            blinking_rect_width = self.BLINKING_WIDTH

        blinking_rect_height = self.input.y - self.input.font_height

        return pygame.Rect(
            blinking_rect_x,  # x-coord from left
            blinking_rect_y,  # y-coord from top
            blinking_rect_width,
            blinking_rect_height,
        )

    def insert_letter_in_position(self):
        """Insert letter if typing in the middle of the string."""
        if self.position < 0 and self.delta_typing > 0:
            self.input.value = (
                self.input.value[: self.left_position - 1]
                + self.input.value[-1]
                + self.input.value[self.left_position - 1 : -1]
            )

    def run(self):
        """Execute all cursor methods."""
        # Some keys (arrows, cntrl, backspace, return) have to be runed outside the event loop
        pressed = pygame.key.get_pressed()
        self.fast_move(pressed)
        self.running_selection(pressed)
        if not self.text_modes["select_delete"]:
            self.fast_delete(pressed)

        self.text = Text(
            text=self.input.value,
            start=self.select_start,
            end=self.select_end,
            modes=self.text_modes,
        )

        # Check if letter has to be typed in the middle of the string
        self.insert_letter_in_position()

        if self.text_modes["select_substitute"]:
            self.input.value, self.position = self.text.substitute()
        elif self.text_modes["select_delete"]:
            self.input.value, self.position = self.text.delete()
        if self.text.has_selection:
            self.selection = self.text.get_selected_text()
        else:
            self.selection = ""

    def draw(self, surface):
        """Run all cursor methods that draw in the CL."""
        # Check cooldowns and display user input
        self.blinking_cursor_cooldown()

        # Check past vs current ongoing states
        if self.past_ongoing == True and self.text_modes["select_ongoing"] == False:
            if not self.disp_start == self.disp_end:
                self.state_start = self.disp_start
                self.state_end = self.disp_end

        if self.text_modes["select_maintain"]:
            # Use state variables to maintain the selection
            if self.state_end == 0:
                self.state_end = None
            self.selection = self.input.value[self.state_start : self.state_end]

        # Track cursor movement
        self.left_position, self.new_typing_len = self.track_cursor_movement()
        self.delta_typing = self.new_typing_len - self.prev_typing_len

        # Correct text indices for displaying purposes
        if self.text.has_selection:
            self.disp_start, self.disp_end = self.text.correct_idxs_for_display()

        # Create blinking rectangle
        blinking_rect = self.create_rectangle()

        # Display rectangle if needed and update cooldowns
        if self.blinking_active:
            pygame.draw.rect(surface, WHITE, blinking_rect)
            self.update_cooldowns()

        # Display input value
        if self.text_modes["select_maintain"] or self.text_modes["select_ongoing"]:
            # Display the total string in 3 chunks to display black letters in selection
            # First chunk
            text_1 = self.input.font.render(
                self.input.prompt + self.input.value[: self.disp_start], 1, WHITE
            )
            surface.blit(text_1, (self.input.x, self.input.y))

            # Second chunk if it exists
            if not self.disp_start == None:
                text_2 = self.input.font.render(
                    self.input.value[self.disp_start : self.disp_end], 1, BLACK
                )
                surface.blit(text_2, (self.input.x + text_1.get_width(), self.input.y))

            # Display 3rd chunk if it exists
            if not self.disp_end == None:
                text_3 = self.input.font.render(
                    self.input.value[self.disp_end :], 1, WHITE
                )
                surface.blit(
                    text_3,
                    (
                        self.input.x + text_1.get_width() + text_2.get_width(),
                        self.input.y,
                    ),
                )
        else:
            # Render and display the entire string
            text = self.input.font.render(
                self.input.prompt + self.input.value, 1, WHITE
            )
            surface.blit(text, (self.input.x, self.input.y))

        # Update variables
        self.prev_typing_len = self.new_typing_len
        self.past_ongoing = self.text_modes["select_ongoing"]
        if self.text_modes["select_substitute"] or self.text_modes["select_delete"]:
            self.text_modes["select_substitute"] = False
            self.text_modes["select_delete"] = False
