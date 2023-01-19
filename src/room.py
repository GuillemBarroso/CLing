"""Module containing Room class."""

import pygame

from src.colors import BLACK


class Room:
    """Room class."""

    def __init__(self, screen, ROOM_MAP=None, ROOM_NAME=None):
        """Initialize map class."""
        self.cells_size = (10, 10)
        self.walls = []
        self.doors = []
        self.map = ROOM_MAP
        self.name = ROOM_NAME
        self.n_cells_x = screen.surface.get_width() // self.cells_size[0]
        self.n_cells_y = screen.surface.get_height() // self.cells_size[1]
        self._check_map_size()
        self._build()

    def _build(self):
        """Build room map creating walls."""
        x, y = 0, 0
        for raw in self.map:
            for cell in raw:
                if cell == "X":
                    self.walls.append(
                        pygame.Rect(x, y, self.cells_size[0], self.cells_size[1])
                    )
                if cell == "D":
                    self.doors.append(
                        pygame.Rect(x, y, self.cells_size[0], self.cells_size[1])
                    )
                x += self.cells_size[0]
            x = 0
            y += self.cells_size[1]

    def _check_map_size(self):
        if not len(self.map) == self.n_cells_y:
            text = (
                f"Number of raws of the room's map ({len(self.map)}) "
                + f"does not match the number of y cells of the screen ({self.n_cells_y})."
            )
            raise ValueError(text)

        for i_raw, raw in enumerate(self.map):
            if not len(raw) == self.n_cells_x:
                text = (
                    f"Number of columns ({len(raw)}) in raw {i_raw} does not "
                    + f"match the number of the x cells of the screen ({self.n_cells_x})"
                )
                raise ValueError(text)

    def draw(self, canvas):
        """Draw walls of the room."""
        for wall in self.walls:
            pygame.draw.rect(canvas, BLACK, wall)
