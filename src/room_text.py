"""Module containing the rooms' descriptions and how they are displayed."""

from random import randint

import pygame

ENTRY_CAVE_TEXT = (
    "As you awaken in a dimly lit room, confusion sets in. Your surroundings are unfamiliar "
    "and disorienting, leaving you feeling lost and unsure of what to do next. You quickly "
    "realize that you need to find a way out of this place. A faint whisper echoes in your "
    "mind, urging you to 'look at' the walls. Perhaps they hold a clue to your escape. It's "
    "time to start searching and uncovering the secrets of this mysterious room."
)

VALLEY_TEXT = (
    "As you step out of the dark and confining room, you're greeted by "
    "the sight of an expansive green area. The soft blades of grass tickle "
    "your feet as you take in your surroundings. The area is dotted with tall "
    "trees, providing shade and a sense of tranquility. However, you quickly "
    "remember the task at hand - to find a way to survive. You'll need to explore "
    "the area and take advantage of the resources it has to offer. The fresh air "
    "and open space invigorate you, giving you the energy to tackle whatever "
    "challenges lay ahead."
)


class RoomText:
    """Room text object displaying the room's description."""

    def __init__(self, cmd_line):
        """Initialize object."""
        self.cmd_line = cmd_line

        self.room_text_dict = {
            "entry_cave": ENTRY_CAVE_TEXT,
            "valley": VALLEY_TEXT,
        }
        self.room_first_entry = dict.fromkeys(self.room_text_dict.keys(), True)
        self.update_text = False
        self.past_updated_text = 0
        self.update_text_speed = 20
        self.letter_counter = 0
        self.line_counter = 0
        self.keyboard_sound = pygame.mixer.Sound("src/audio/mech_keyboard.wav")
        self.enter_sound = pygame.mixer.Sound("src/audio/mech_keyboard_enter.wav")
        self.enter_sound.set_volume(0.1)

    def update_text_cooldowns(self):
        """Update cooldowns to type the next letter."""
        current_time = pygame.time.get_ticks()
        if not self.update_text:
            if current_time - self.past_updated_text >= (
                self.update_text_speed - randint(-20, 20)
            ):
                self.update_text = True

    def update_room_first_entry(self):
        """Check if current room has been already accessed in the past."""
        if self.room_first_entry[self.cmd_line.map_state]:
            self.cmd_line.active_player = False
            self.room_name = self.cmd_line.map_state.upper().replace("_", " ")
            self.room_text = self.room_text_dict[self.cmd_line.map_state]
            self.room_text = self.cmd_line.split_long_user_input(self.room_text)
            self.update_text_cooldowns()
            self.display_animated_text()

    def display_animated_text(self):
        """Set text in a for loop."""
        if self.update_text == True:
            self.play_keyboard_sound()
            self.letter_counter += 1
            self.cmd_line.input.value = self.room_text[self.line_counter][
                : self.letter_counter
            ]
            self.display_text_on_cl()
            self.past_updated_text = pygame.time.get_ticks()
            self.update_text = False
            if self.letter_counter == len(self.room_text[self.line_counter]) + 2:
                self.cmd_line._history.append(self.room_text[self.line_counter])
                self.line_counter += 1
                self.letter_counter = 0
                if self.line_counter == len(self.room_text):
                    self.line_counter = 0
                    self.room_first_entry[self.cmd_line.map_state] = False
                    self.keyboard_sound.stop()
                    self.cmd_line.input.value = ""
                    self.cmd_line.active_player = True
                    self.enter_sound.play()

    def play_keyboard_sound(self):
        """Play the sound of a mechanical keyboard typing."""
        if self.letter_counter == 0:
            self.keyboard_sound.play(loops=-1)

    def display_text_on_cl(self):
        """Display room's description."""
        # self.cmd_line.input.value = self.room_text
        self.cmd_line._input.draw(self.cmd_line._surface)
