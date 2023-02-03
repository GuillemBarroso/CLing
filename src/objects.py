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
