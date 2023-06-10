"""Module containing the rooms' descriptions and how they are displayed."""

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

    def update_room_first_entry(self):
        """Check if current room has been already accessed in the past."""
        if self.room_first_entry[self.cmd_line.map_state]:
            self.display_text_on_cl()
            self.room_first_entry[self.cmd_line.map_state] = False

    def display_text_on_cl(self):
        """Display room's description."""
        room_name = self.cmd_line.map_state.upper().replace("_", " ")
        room_text = self.room_text_dict[self.cmd_line.map_state]
        self.cmd_line.input.value = room_text
        self.cmd_line.write_command_response(prompt=f"{room_name}: ")
