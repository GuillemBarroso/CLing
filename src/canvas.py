"""Module containing the canvas class."""
import pygame

WIDTH, HEIGHT = 1300, 900


def get_canvas(WIDTH=1300, HEIGHT=900):
    """Return canvas with a certain width and height."""
    return pygame.display.set_mode((WIDTH, HEIGHT))
