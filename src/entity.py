"""Module containing a generic entity."""

from math import sin

import pygame


class Entity(pygame.sprite.Sprite):
    """Generic Entity class."""

    def __init__(self, groups):
        """Initialize object."""
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.move_direction = pygame.math.Vector2()
        self.aim_direction = pygame.math.Vector2()
        self.aim_angle = 0

    def move(self, speed):
        """Move player rectangle and hitbox (used for overlapping)."""
        if not self.move_direction.magnitude() == 0:
            self.move_direction = self.move_direction.normalize()

        self.hitbox.x += self.move_direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.move_direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, move_direction):
        """Check for horizontal and vertigal collisions."""
        if move_direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.move_direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.move_direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        if move_direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.move_direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.move_direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        """Sign wave going from 0 to 255 several times."""
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
