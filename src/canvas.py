"""Module containing the canvas class."""
import pygame

from src.settings import HEIGHT, WIDTH


def get_canvas():
    """Return canvas with a certain width and height."""
    return pygame.display.set_mode((WIDTH, HEIGHT))


def build_canvas(canvas, screen, cmd_line):
    """Stick screen and cmd_line surfaces to canvas."""
    canvas.blit(screen.surface, (0, 0))
    canvas.blit(cmd_line.surface, (0, canvas.get_height() - cmd_line.height))
