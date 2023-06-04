"""Module containing the settings parameters of the game."""

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

weapon_data = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": "src/images/weapons/sword/full.png",
    },
    "lance": {
        "cooldown": 400,
        "damage": 30,
        "graphic": "src/images/weapons/lance/full.png",
    },
    "axe": {
        "cooldown": 300,
        "damage": 20,
        "graphic": "src/images/weapons/axe/full.png",
    },
    "rapier": {
        "cooldown": 50,
        "damage": 8,
        "graphic": "src/images/weapons/rapier/full.png",
    },
    "sai": {"cooldown": 80, "damage": 10, "graphic": "src/images/weapons/sai/full.png"},
}
