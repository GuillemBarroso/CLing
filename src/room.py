"""Module containing Room class."""

import pygame

from src.colors import BLACK
from src.maps import ROOM_TEST


class Room:
    """Room class."""

    def __init__(self, canvas):
        """Initialize map class."""
        self.cells_size = (10, 10)
        self.walls = []

        n_cells_x = canvas.get_width() / self.cells_size[0]
        n_cells_y = canvas.get_height() / self.cells_size[1]

        self.room_map = ROOM_TEST
        self._build()

    def _build(self):
        """Build room map creating walls."""
        x, y = 0, 0
        for raw in self.room_map:
            for wall in raw:
                if wall == "X":
                    self.walls.append(
                        pygame.Rect(x, y, self.cells_size[0], self.cells_size[1])
                    )
                x += self.cells_size[0]
            x = 0
            y += self.cells_size[1]

    def draw(self, canvas):
        """Draw walls of the room."""
        for wall in self.walls:
            pygame.draw.rect(canvas, BLACK, wall)
