"""Module with functions that determine the interaction of the player with the room objects."""

from src.command_line import write_command_response
from src.objects import BreakableWall, Door, Wall


def get_closest_object_requested_by_user(cmd_line, args, player):
    """Return the closest user-requested object to the player."""
    closest_objects, distances = player.get_closest_object_in_room()
    if not closest_objects:
        cmd_line.input.value = "No nearby objects to interact with."
        write_command_response(cmd_line)
    else:
        (
            closest_objects,
            distances,
        ) = find_user_object_among_closest_objects(closest_objects, distances, args[0])
        if not closest_objects:
            cmd_line.input.value = f"You do not see a {args[0]} nearby."
            write_command_response(cmd_line)
        else:
            closest_object = get_clostest_object_from_player(closest_objects, distances)
    return closest_object


def find_user_object_among_closest_objects(closest_objects, distances, user_obj):
    """Filter closest_objects list with only the types that the user requested."""
    # TODO: IMPROVE THIS IF CONDITIONS THAT WILL GROW FOR ALL OBJECTS!!!!!
    if user_obj == "wall":
        for i, obj in enumerate(closest_objects):
            if not type(obj) == Wall or type(obj) == BreakableWall:
                closest_objects.remove(obj)
                distances.pop(i)
    elif user_obj == "door":
        for i, obj in enumerate(closest_objects):
            if not type(obj) == Door:
                closest_objects.remove(obj)
                distances.pop(i)
    return closest_objects, distances


def get_clostest_object_from_player(closest_objects, distances):
    """From a list of objects, return the closest one."""
    min_distance = 1e5
    for i, obj in enumerate(closest_objects):
        if min_distance > distances[i]:
            closest_object = obj
    return closest_object
