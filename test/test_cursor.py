"""Module containing tests for the Cursor class."""
# import sys

import pygame

from src.canvas import get_canvas
from src.command_line import CL

# import pygame.locals as locals


pygame.init()
canvas = get_canvas()
cl = CL(canvas=canvas)


def test_selection():
    """Test selection functionality."""
    cl.cursor.select_start = 0
    cl.cursor.select_start = 2
    cl.cursor.select = True
    cl.cursor.select_ongoing = True
    cl.input.value = "Jane_Joe"

    # Cannot force an event such as pressing backspace apparently
    # event = pygame.event.Event(locals.KEYDOWN, {"key": locals.K_BACKSPACE})
    # cl.cursor.run_event(event)
    cl.cursor.draw(canvas)
    assert cl.cursor.selection == "Ja"


# def test_create_rectangle():
