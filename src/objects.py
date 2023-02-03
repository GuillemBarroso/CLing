"""Module containing the different object the user will interact with."""

import pygame

from src.colors import BLACK, GREY


class Wall:
    """Wall object."""

    def __init__(self, x, y, width, height):
        """Initialize object."""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK

    def look_at(self):
        """Return message when the Wall is being looked at."""
        return "You see a rock solid wall."


class Door:
    """Door object."""

    def __init__(self, x, y, width, height, name):
        """Initialize object."""
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.color = GREY


class BreakableWall:
    """Wall that can be broken."""

    def __init__(self, x, y, width, height, name):
        """Initialize object."""
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.is_broken = False
        self.color = BLACK

    def look_at(self):
        """Return message when the BreakableWall is being looked at."""
        return (
            "This wall looks slightly different than the others. You notice a small "
            "crak. Maybe you could break that wall and scape from this damn hole!"
        )

    def break_wall(self):
        """Break wall so it becomes a door."""
        self.is_broken = True
        self.color = GREY
