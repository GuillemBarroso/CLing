"""Module containing the different object the user will interact with."""

import pygame

from src.colors import BLACK, GREY


class Wall(pygame.sprite.Sprite):
    """Wall object."""

    def __init__(self, game, x, y, width, height):
        """Initialize object."""
        self.color = BLACK
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._layer = 1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.is_open = False

    def update(self):
        """Update sprite."""
        pass

    def look_at(self):
        """Return message when the Wall is being looked at."""
        return "You see a rock solid wall."

    def break_wall(self):
        """Return message when the player tries to break a solid wall."""
        return "You cannot break a rock solid wall!"


class Door(pygame.sprite.Sprite):
    """Door object."""

    def __init__(self, game, x, y, width, height, name):
        """Initialize object."""
        self.color = GREY
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.is_open = True

        self._layer = 1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        """Update sprite."""
        pass


class BreakableWall(pygame.sprite.Sprite):
    """Wall that can be broken."""

    def __init__(self, game, x, y, width, height, name):
        """Initialize object."""
        self.color = BLACK
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.is_open = False

        self._layer = 1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        """Update sprite."""
        pass

    def look_at(self):
        """Return message when the BreakableWall is being looked at."""
        return (
            "This wall looks slightly different than the others. You notice a small "
            "crak. Maybe you could break that wall and scape from this damn hole!"
        )

    def break_wall(self):
        """Break wall so it becomes a door."""
        self.is_open = True
        self.color = GREY
        return "You manage to smash the wall and open a hole to pass through."
