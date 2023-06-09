"""Module containing the tile object."""

import pygame

from src.settings import HITBOX_OFFSET, TILESIZE
from src.tile_interaction import BREAK_IT_MESSAGE, LOOK_AT_MESSAGE


class Tile(pygame.sprite.Sprite):
    """Tile object to create a sprite with some groups."""

    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((TILESIZE, TILESIZE)),
    ):
        """Initialize Tile object."""
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.look_at_msg = LOOK_AT_MESSAGE[sprite_type]
        self.break_it_msg = BREAK_IT_MESSAGE[sprite_type]

        # Offset for a better visualization in "object" sprites
        y_offset = HITBOX_OFFSET[sprite_type]
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)

    def look_at(self):
        """Look at a tile."""
        return self.look_at_msg

    def break_it(self):
        """Break a tile."""
        return self.break_it_msg
