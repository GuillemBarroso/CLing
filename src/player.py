"""Module containing the player class."""

import os

import pygame
import pygame.locals as locals


class Player:
    """Player class."""

    def __init__(self, x=100, y=100):
        """Initialize player class."""
        self.velocity = 5
        # self.x = x
        # self.y = y
        self.player_size = (50, 50)
        self.image_dir = "src/images"
        self.image_name = "player.jpg"
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(self.image_dir, self.image_name)),
            self.player_size,
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "N"

    def apply_event(self, event):
        """Change the value of the direction variable according to event."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.direction = "E"
            elif event.key == pygame.K_LEFT:
                self.direction = "W"
            elif event.key == pygame.K_UP:
                self.direction = "N"
            elif event.key == pygame.K_DOWN:
                self.direction = "S"

    def move(self, walls=None):
        """Move player around when pressing arrow keys."""
        # Storing the key pressed using key.get_pressed() method
        key_pressed_is = pygame.key.get_pressed()

        old_x, old_y = self.rect.x, self.rect.y

        # Changing the coordinates of the player
        if key_pressed_is[locals.K_LEFT]:
            self.rect.x -= self.velocity
            self.direction = "W"
        if key_pressed_is[locals.K_RIGHT]:
            self.rect.x += self.velocity
            self.direction = "E"
        if key_pressed_is[locals.K_UP]:
            self.rect.y -= self.velocity
            self.direction = "N"
        if key_pressed_is[locals.K_DOWN]:
            self.rect.y += self.velocity
            self.direction = "S"

        # Check for illegal movements colliding with walls
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.x = old_x
                    self.rect.y = old_y

    def draw(self, canvas):
        """Draw player on canvas."""
        if self.direction == "N":
            canvas.blit(self.image, (self.rect.x, self.rect.y))
        elif self.direction == "W":
            canvas.blit(
                pygame.transform.rotate(self.image, 90), (self.rect.x, self.rect.y)
            )
        elif self.direction == "E":
            canvas.blit(
                pygame.transform.rotate(self.image, -90), (self.rect.x, self.rect.y)
            )
        elif self.direction == "S":
            canvas.blit(
                pygame.transform.flip(self.image, True, True),
                (self.rect.x, self.rect.y),
            )
        elif self.direction == "NE":
            canvas.blit(
                pygame.transform.rotate(self.image, -45), (self.rect.x, self.rect.y)
            )
