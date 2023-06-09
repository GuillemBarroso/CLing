"""Module containing the tile-player intraction information."""

PLAYER_ACTION_RADIUS = 100

TILE_PRIORITY = {"ocean": 1, "tree": 1, "grass": 1, "wall": 1, "wall_hole": 1.2}

LOOK_AT_MESSAGE = {
    "wall": "You see a rock solid wall.",
    "wall_hole": (
        "This wall looks slightly different than the others. You notice a small "
        "crak. Maybe you could break that wall and scape from this damn hole!"
    ),
    "ocean": "Water message",
    "grass": "Grass mesaage",
    "tree": "Tree msg",
}

BREAK_IT_MESSAGE = {
    "wall": "You cannot break a rock solid wall!",
    "wall_hole": (
        "You manage to smash the wall and open a hole to pass through. "
        "You may be able to crawl into it."
    ),
    "ocean": "Are you seriusly trying to break water?",
    "grass": "",
    "tree": "",
}
