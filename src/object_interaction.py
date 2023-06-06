"""Module with functions that determine the interaction of the player with the room objects."""


def get_closest_object_requested_by_user(cmd_line, args, player, accepted_types):
    """Return the closest user-requested object to the player."""
    closest_objects, distances = player.get_closest_object_in_room()
    if not closest_objects:
        cmd_line.input.value = "No nearby objects to interact with."
        cmd_line.write_command_response(cmd_line)
        closest_object = None
    else:
        (closest_objects, distances,) = find_user_object_among_closest_objects(
            closest_objects, distances, accepted_types
        )
        if not closest_objects:
            cmd_line.input.value = f"You do not see a {args[0]} nearby."
            cmd_line.write_command_response(cmd_line)
        else:
            closest_object = get_clostest_object_from_player(closest_objects, distances)
    return closest_object


def find_user_object_among_closest_objects(closest_objects, distances, accepted_types):
    """Filter closest_objects list with only the types that the user requested."""
    for i, obj in enumerate(closest_objects):
        if not type(obj) in accepted_types:
            closest_objects.remove(obj)
            distances.pop(i)
    return closest_objects, distances


def get_clostest_object_from_player(closest_objects, distances):
    """From a list of objects, return the closest one."""
    min_distance = 1e5
    for i, obj in enumerate(closest_objects):
        if min_distance > distances[i]:
            min_distance = distances[i]
            closest_object = obj
    return closest_object
