"""Module containing the canvas class."""
import pygame


def get_canvas(WIDTH=1280, HEIGHT=720):
    """Return canvas with a certain width and height."""
    return pygame.display.set_mode((WIDTH, HEIGHT))


def build_canvas(canvas, screen, cmd_line):
    """Stick screen and cmd_line surfaces to canvas."""
    canvas.blit(screen.surface, (0, 0))
    canvas.blit(cmd_line.surface, (0, canvas.get_height() - cmd_line.height))