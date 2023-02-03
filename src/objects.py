"""Module containing the different object the user will interact with."""

import pygame

from src.colors import BLACK, GREY


class Wall:
    """Wall object."""

    def __init__(self, x, y, width, height):
        """Initialize object."""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK


class Door:
    """Door object."""

    def __init__(self, x, y, width, height, name):
        """Initialize object."""
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.color = GREY


class BreakableDoor:
    """Wall that can be broken."""

    def __init__(self, x, y, width, height, breakable):
        """Initialize object."""
        self.rect = pygame.Rect(x, y, width, height)
        self.is_breakable = breakable
        self.is_broken = False

    def break_door(self):
        """Break door and allow to pass through."""
        self.is_broken = True
