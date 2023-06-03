"""Module containing Room class."""

import pygame

from src.commands import write_command_response
from src.objects import NPC, BreakableWall, Door, Wall


class Room:
    """Room class."""

    def __init__(self, screen, cmd_line, room=None):
        """Initialize map class."""
        self.walls = []
        self.doors = []
        self.hidden_doors = []
        self.npcs = []
        self.cmd_line = cmd_line
        self.room_map = room[0]
        self.room_description = room[1]
        self.cells_size = room[2]
        self.room_name = room[3]
        self.n_cells_x = screen.surface.get_width() // self.cells_size[0]
        self.n_cells_y = screen.surface.get_height() // self.cells_size[1]
        ## TODO: move the loading image and scale it properly
        self.img_guide = pygame.image.load(
            "src/images/NPCs/npc_guide.jpg"
        ).convert_alpha()
        self.img_guide = pygame.transform.scale(self.img_guide, (30, 30))
        # self._check_map_size()
        self._build()
        self._display_room_description()

    def _build(self):
        """Build room map creating walls."""
        x, y = 0, 0
        for raw in self.room_map:
            for i in range(0, len(raw), 3):
                cell = raw[i : i + 3]
                if cell == "XXX":
                    self.walls.append(
                        Wall(x, y, self.cells_size[0], self.cells_size[1])
                    )
                if cell == "D01":
                    self.doors.append(
                        Door(x, y, self.cells_size[0], self.cells_size[1], cell)
                    )
                if cell == "D00":
                    self.hidden_doors.append(
                        BreakableWall(
                            x, y, self.cells_size[0], self.cells_size[1], cell
                        )
                    )
                if cell == "g01":
                    self.npcs.append(
                        NPC(
                            x,
                            y,
                            self.cells_size[0],
                            self.cells_size[1],
                            "test",
                            self.img_guide,
                        )
                    )
                x += self.cells_size[0]
            x = 0
            y += self.cells_size[1]

    def _check_map_size(self):
        if not len(self.room_map) == self.n_cells_y:
            text = (
                f"Number of raws of the room's map ({len(self.room_map)}) "
                + f"does not match the number of y cells of the screen ({self.n_cells_y})."
            )
            raise ValueError(text)

        for i_raw, raw in enumerate(self.room_map):
            if not len(raw) // 3 == self.n_cells_x:
                text = (
                    f"Number of columns ({len(raw)}) in raw {i_raw} does not "
                    + f"match the number of the x cells of the screen ({self.n_cells_x})"
                )
                raise ValueError(text)

    def _display_room_description(self):
        self.cmd_line.input.value = self.room_description
        write_command_response(self.cmd_line, prompt=f"{self.room_name}: ")
        self.cmd_line.input.value = ""
        write_command_response(self.cmd_line)

    def draw(self, canvas):
        """Draw walls of the room."""
        for wall in self.walls:
            pygame.draw.rect(canvas, wall.color, wall.rect)
        for door in self.doors:
            pygame.draw.rect(canvas, door.color, door.rect)
        for door in self.hidden_doors:
            pygame.draw.rect(canvas, door.color, door.rect)
        for npc in self.npcs:
            canvas.blit(npc.image, (npc.rect.x, npc.rect.y))
