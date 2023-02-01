"""Module containnt the connections across the different rooms in the game."""


# The CONNECTIONS list contains an entry for each door in the game. The information
# for each door is the following:
#    0. Name of the entering door
#    1. Name of the exiting door
#    2. Name of the room of the entering door
#    3. Name of the room of the existing door
#    4. Shift in the x position of the player when appearing in the new room
#    5. Shift in the y position of the player when appearing in the new room
# Note that the position shitfs (4 and 5) are required so the player does not appear
# on top of the door itself, which would return it back to the previous room.
CONNECTIONS = [
    ("D00", "D01", "start_room", "city_map", 0, -50),
    ("D01", "D00", "city_map", "start_room", 0, 50),
]
