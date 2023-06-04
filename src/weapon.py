"""Module containing the Weapon class."""

import pygame


class Weapon(pygame.sprite.Sprite):
    """Weapon class that uses weapon images and weapon data."""

    def __init__(self, player, groups):
        """Initialize weapon."""
        super().__init__(groups)
        direction = player.status.split("_")[0]

        # graphic
        full_path = f"src/images/weapons/{player.weapon}/{direction}.png"
        self.image = pygame.image.load(full_path)

        # placement
        if direction == "right":
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pygame.math.Vector2(0, 16)
            )
        elif direction == "left":
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pygame.math.Vector2(0, 16)
            )
        elif direction == "up":
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pygame.math.Vector2(10, 0)
            )
        elif direction == "down":
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0)
            )
