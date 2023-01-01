"""Module containing the player class."""

import os

import pygame
import pygame.locals as locals


class Player:
    """Player class."""

    def __init__(self, x=100, y=100):
        """Initialize player class."""
        self.velocity = 5
        self.x = x
        self.y = y
        self.player_size = (50, 50)
        self.image_dir = "src/images"
        self.image_name = "player.jpg"
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(self.image_dir, self.image_name)),
            self.player_size,
        )
        self.direction = "N"

    def move(self):
        """Move player around when pressing arrow keys."""
        # Storing the key pressed using key.get_pressed() method
        key_pressed_is = pygame.key.get_pressed()

        # Changing the coordinates of the player
        if key_pressed_is[locals.K_LEFT]:
            self.x -= self.velocity
        if key_pressed_is[locals.K_RIGHT]:
            self.x += self.velocity
        if key_pressed_is[locals.K_UP]:
            self.y -= self.velocity
        if key_pressed_is[locals.K_DOWN]:
            self.y += self.velocity

    def draw(self, canvas):
        """Draw player on canvas."""
        if self.direction == "N":
            canvas.blit(self.image, (self.x, self.y))
        elif self.direction == "W":
            canvas.blit(pygame.transform.rotate(self.image, 90), (self.x, self.y))
        elif self.direction == "E":
            canvas.blit(pygame.transform.rotate(self.image, -90), (self.x, self.y))
        elif self.direction == "S":
            canvas.blit(pygame.transform.flip(self.image, True, True), (self.x, self.y))
        elif self.direction == "NE":
            canvas.blit(pygame.transform.rotate(self.image, -45), (self.x, self.y))
