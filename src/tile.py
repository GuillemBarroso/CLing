"""Module containing the tile object."""

import pygame

from src.settings import TILESIZE


class Tile(pygame.sprite.Sprite):
    """Tile object to create a sprite with some groups."""

    def __init__(
        self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))
    ):
        """Initialize Tile object."""
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
