"""Module containing the Cursor class, controlling the CL cursor."""

import pygame
import pygame.locals as locals

from src.colors import BLACK, WHITE


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
        self.remove_letters_bool = True
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
        self.select = False
        self.select_start = 0
        self.select_end = 0
        self.delta_typing = 0
        self.select_inverted = False
        self.selection = ""
        self.select_ongoing = False
        self.past_ongoing = False
        self.select_maintain = False
        self.select_substitute = False
        self.ini = 0
        self.end = 0
        self.old_ini = 0
        self.old_end = 0
        self.new_ini = 0
        self.new_end = 0
        self.state_ini = 0
        self.state_end = 0

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
        if not self.select:
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
            self.delete_ini_pause = self.INI_PAUSE
            self.delete_fast_pause = 0
            self.remove_letters()
        elif (
            self.delete_fast_pause == self.FAST_PAUSE
            and keys_pressed[locals.K_BACKSPACE]
        ):
            self.delete_fast_pause = 0
            self.remove_letters()
        elif keys_pressed[locals.K_BACKSPACE]:
            self.delete_ini_pause += 1
        elif (
            self.delete_ini_pause == self.INI_PAUSE and keys_pressed[locals.K_BACKSPACE]
        ):
            self.delete_fast_pause += 1
        else:
            self.delete_ini_pause = 0
            self.delete_fast_pause = 0
            self.remove_letters_bool = True

    def remove_letters(self):
        """Set conditions in order to remove letters from a string."""
        if self.remove_letters_bool:
            if len(self.input.value[: self.left_position - 1]) == 0:
                self.input.value = self.input.value[self.left_position :]
                self.remove_letters_bool = False
            else:
                self.input.value = (
                    self.input.value[: self.left_position - 1]
                    + self.input.value[self.left_position :]
                )

    def track_cursor_movement(self):
        """Track the cursor on the CL."""
        # Get changes done by typing
        input_length = len(self.input.value)

        # Correct self.position if removing a chunk of string (substitute)
        if self.select_substitute:
            if not self.select_inverted:
                self.position += len(self.substituted_text)

        # Get changes done with the left and right arrows
        if self.position > 0:
            self.position = 0
        if self.position < -len(self.input.value):
            self.position = -len(self.input.value)

        # Correct self.position if removing a chunk of string (substitute)
        # if self.select_substitute:
        #     if not self.select_inverted:
        #         self.position += len(self.substituted_text)
        #         if not self.left_position == 0:
        #             self.position -= 1

        left_position = input_length + self.position
        if left_position < 0:
            left_position = 0

        return left_position, input_length

    def get_select_indices(self):
        """Get the correct selection indices to slice the user's input."""
        if not self.select_start == self.select_end:
            if self.select_start > self.select_end:
                self.select_inverted = True
                ini = self.select_end
                end = self.select_start
            elif self.select_start < self.select_end:
                self.select_inverted = False
                ini = self.select_start
                end = self.select_end
            else:
                self.select_inverted = False
                ini = self.select_start
                end = self.select_end
            if end == 0:
                end = None
        else:
            self.select_inverted = False
            ini = self.select_start
            end = self.select_end
        return ini, end

    def running_selection(self, pressed):
        """Get pressed keys at each frame."""
        if self.select_maintain or self.select_substitute:
            # Trick to avoid overwriting the variables when selecting
            # characters in inverse mode (from left to right).
            # This happens due to the fact that "run_event" are executed
            # before, so we always go one iteration late.
            self.select_start = self.old_select_start
            self.select_end = self.old_select_end
        else:
            # Normal behaviour to obtain the selection positions
            if pressed[locals.K_LSHIFT]:
                self.select_start = self.position
            else:
                self.select_end = self.position

        self.old_select_start = self.select_start
        self.old_select_end = self.select_end

    def run_event(self, event):
        """Update based on an event."""
        if event.type == locals.KEYDOWN:
            if self.select_maintain and event.key == locals.K_LSHIFT:
                self.select_ongoing = True
                self.select_maintain = False
            elif event.key == locals.K_LSHIFT:
                self.select = True
                self.select_ongoing = True
            elif self.select_maintain and (
                event.key == locals.K_LEFT or event.key == locals.K_RIGHT
            ):
                self.select = False
                self.select_ongoing = False
                self.select_maintain = False
            elif self.select_maintain:
                self.select_substitute = True
                self.select = True
                self.select_maintain = False
                self.select_ongoing = False

        if event.type == locals.KEYUP:
            if event.key == locals.K_LSHIFT and self.old_ini == self.old_end:
                self.select = False
                self.select_ongoing = False
                self.select_maintain = False
            elif event.key == locals.K_LSHIFT:
                self.select_maintain = True
                self.select_ongoing = False
            elif not event.key == locals.K_LEFT and not event.key == locals.K_RIGHT:
                self.select = False
                self.select_ongoing = False
                self.select_maintain = False
                self.select_substitute = False

    def run(self):
        """Execute all cursor methods."""
        # Some keys (arrows, cntrl, backspace, return) have to be runed outside the event loop
        pressed = pygame.key.get_pressed()
        self.fast_delete(pressed)
        self.fast_move(pressed)
        self.running_selection(pressed)

    def create_rectangle(self, select_text):
        """Create white rectangle with thin width or with the select_text width if select."""
        # Get text based on cursor position
        delta_text = self.input.font.render(
            self.input.prompt + self.input.value[: self.left_position], 1, WHITE
        )

        # Create rectangle
        if self.select:
            if self.select_inverted:
                blinking_rect_x = (
                    self.input.x + delta_text.get_width() - select_text.get_width()
                )
            else:
                blinking_rect_x = self.input.x + delta_text.get_width()
        else:
            blinking_rect_x = self.input.x + delta_text.get_width()

        blinking_rect_y = self.input.y

        if self.select:
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

    def draw(self, surface):
        """Run all cursor methods that draw in the CL."""
        # Check cooldowns and display user input
        self.blinking_cursor_cooldown()

        # Reorder self.value if typing in the middle of the string
        self.input.reorder_value_if_modified(self)

        # Check past vs current ongoing states
        if self.past_ongoing == True and self.select_ongoing == False:
            if not self.ini == self.end:
                self.state_ini = self.ini
                self.state_end = self.end

        # Get indices to get selection
        self.ini, self.end = self.get_select_indices()

        if self.select:
            # print("state ini:", self.state_ini)
            # print("state end", self.state_end)
            if self.select_ongoing:
                self.selection = self.input.value[self.ini : self.end]
            elif self.select_maintain:
                self.selection = self.input.value[self.state_ini : self.state_end]
            # elif self.select_substitute:
            #     if self.select_inverted:
            #         self.old_ini = self.old_end
            #         self.old_end = self.old_end
            #     else:
            #         self.old_end = self.old_ini + len(self.selection) -1
            #         self.old_ini = self.old_ini + len(self.selection) -1
            elif self.select_substitute:
                # Substitute the selected region for the next letter introduced by the user
                original_input = self.input.value[:-1]
                self.substituted_text = original_input[self.old_ini : self.old_end]
                self.selection = ""
                self.input.value = self.input.substitute_selection(self)

            # print("Sel str", self.selection)

        # Track cursor movement
        self.left_position, self.new_typing_len = self.track_cursor_movement()
        self.delta_typing = self.new_typing_len - self.prev_typing_len
        print("ongoing", self.select_ongoing)
        print("select", self.select)
        print("maintain", self.select_maintain)
        print("substitute", self.select_substitute)
        print("Pos", self.left_position)
        if self.select_substitute:
            self.select = False
            self.select_substitute = False

        select_text = self.input.font.render(self.selection, 1, WHITE)

        # Create blinking rectangle
        blinking_rect = self.create_rectangle(select_text)

        # Display rectangle if needed and update cooldowns
        if self.blinking_active:
            pygame.draw.rect(surface, WHITE, blinking_rect)
            self.update_cooldowns()

        # Display input value
        if self.select:
            text_1 = self.input.font.render(
                self.input.prompt + self.input.value[: self.old_ini], 1, WHITE
            )
            surface.blit(text_1, (self.input.x, self.input.y))
            text_2 = self.input.font.render(
                self.input.value[self.old_ini : self.old_end], 1, BLACK
            )
            surface.blit(text_2, (self.input.x + text_1.get_width(), self.input.y))
            if not self.old_end == None:
                text_3 = self.input.font.render(
                    self.input.value[self.old_end :], 1, WHITE
                )
                surface.blit(
                    text_3,
                    (
                        self.input.x + text_1.get_width() + text_2.get_width(),
                        self.input.y,
                    ),
                )
        else:
            text = self.input.font.render(
                self.input.prompt + self.input.value, 1, WHITE
            )
            surface.blit(text, (self.input.x, self.input.y))

        # Update variables
        self.prev_typing_len = self.new_typing_len
        self.past_ongoing = self.select_ongoing
        if not self.select_maintain:
            self.old_ini = self.ini
            self.old_end = self.end
