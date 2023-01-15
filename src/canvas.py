"""Module containing the canvas class."""
import pygame


def get_canvas(WIDTH=1280, HEIGHT=720):
    """Return canvas with a certain width and height."""
    return pygame.display.set_mode((WIDTH, HEIGHT))
