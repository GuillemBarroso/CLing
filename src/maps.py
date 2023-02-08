"""Module containing the maps of the different rooms and its descriptions."""

start_room = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXD00XXXXXXXXXXXXXXXXXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXX                           XXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]
start_room_cell_size = (100, 50)
start_room_initial_position = (640, 360)
start_room_desription = (
    "As you awaken in the dimly lit room, confusion sets in. Your surroundings are unfamiliar "
    "and disorienting, leaving you feeling lost and unsure of what to do next. You quickly "
    "realize that you need to find a way out of this place. A faint whisper echoes in your "
    "mind, urging you to 'look at' the walls. Perhaps they hold a clue to your escape. It's "
    "time to start searching and uncovering the secrets of this mysterious room."
)

city_map = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXX                                                                                                                           XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                       T01                                                                                 XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                                               T01                                                         XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                    XXXXXXXXXXXX                                                                           XXX",
    "XXX                                    XXXXXXXXXXXX                                                                           XXX",
    "XXX                                    XXXXXXXXXXXX                                                                           XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                                                     T01                                                   XXX",
    "XXX         D01                                                                                                               XXX",
    "XXX                                                                                                                           XXX",
    "XXX                                                                                                                           XXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]
city_map_cell_size = (30, 30)

city_map_description = (
    "As you step out of the dark and confining room, you're greeted by "
    "the sight of an expansive green area. The soft blades of grass tickle "
    "your feet as you take in your surroundings. The area is dotted with tall "
    "trees, providing shade and a sense of tranquility. However, you quickly "
    "remember the task at hand - to find a way to survive. You'll need to explore "
    "the area and take advantage of the resources it has to offer. The fresh air "
    "and open space invigorate you, giving you the energy to tackle whatever "
    "challenges lay ahead."
)

# Create the dictionary with all the room maps and room descriptions
rooms_dict = {
    "start_room": (
        start_room,
        start_room_desription,
        start_room_cell_size,
        "CAVE",
        start_room_initial_position,
    ),
    "city_map": (city_map, city_map_description, city_map_cell_size, "VALLEY"),
}
