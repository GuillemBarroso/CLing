"""Module containing the Fog object."""

import math

import numpy as np
import pygame

from src.settings import HEIGHT, WIDTH


class Fog:
    """Fog object."""

    def __init__(self):
        """Initialize object."""
        # self.map_state = map_state
        self.fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.AWARENESS_RADIUS = 100
        self.VISION_ANGLE = 22.5
        self.VISION_LENGTH = 400

    @staticmethod
    def _get_slope_from_direction_vector(vector):

        vector = vector.normalize()
        try:
            if vector[0] < vector.epsilon:
                vector[0] = 0
            elif vector[1] < vector.epsilon:
                vector[1] = 0
            elif vector[0] > vector.epsilon:
                vector[0] = 1
            elif vector[1] > vector.epsilon:
                vector[1] = 1
            return vector[1] / vector[0]
        except ZeroDivisionError:
            return vector[1]

    def get_pixel_alpha(self, x, y, player, player_center):
        """Compute pixel alpha given x, y and the player's aim direction."""
        # Get aiming y position
        aim_vect = pygame.Vector2(
            math.cos(player.aim_angle * math.pi / 180),
            math.sin(player.aim_angle * math.pi / 180),
        )
        aim_dir = self._get_slope_from_direction_vector(aim_vect)
        y_aim = aim_dir * (x - player_center[0])

        # Get vision direction
        vision_vect = pygame.Vector2(
            math.cos(self.VISION_ANGLE * math.pi / 180),
            math.sin(self.VISION_ANGLE * math.pi / 180),
        )
        vision_dir = self._get_slope_from_direction_vector(vision_vect)
        if float(y) - abs(player_center[1]) > y_aim:
            y_upper = (aim_dir + vision_dir) * (
                x - player_center[0]
            ) + self.AWARENESS_RADIUS
            return (float(y) - abs(player_center[1])) / y_upper
        elif float(y) - abs(player_center[1]) < y_aim:
            y_lower = (
                (aim_dir - vision_dir) * (x - player_center[0])
                - self.AWARENESS_RADIUS
                - player_center.y
            )
            return (y_aim - float(y)) / abs(y_aim - y_lower)
        else:
            return 0

    def draw(self, surface, player, offset):
        """Draw fog on surface."""
        player_center = player.rect.center - offset

        self.fog.fill((0, 0, 0, 255))
        delta_alpha_circle = 255 / float(self.AWARENESS_RADIUS)
        delta_alpha_cone = 255 / float(self.VISION_LENGTH)

        for delta_circle in range(self.AWARENESS_RADIUS, 1, -1):
            pygame.draw.circle(
                self.fog,
                (0, 0, 0, delta_circle * delta_alpha_circle),
                player_center,
                delta_circle,
            )

        vision_rect_right = pygame.Rect((0, 0), (0, 0))
        # vision_rect_left = pygame.Rect((0,0), (0,0))
        for delta_cone in np.linspace(self.VISION_LENGTH, 0, num=50):
            vision_rect_right.width = delta_cone * (
                self.AWARENESS_RADIUS / self.VISION_LENGTH
            )
            vision_rect_right.height = delta_cone
            vision_rect_right.bottomleft = player_center
            pygame.draw.rect(
                self.fog,
                (0, 0, 0, delta_cone * delta_alpha_cone),
                vision_rect_right,
            )

            # vision_rect_left.width = delta_cone*(self.AWARENESS_RADIUS/self.VISION_LENGTH)
            # vision_rect_left.height = delta_cone
            # vision_rect_left.bottomright = player_center
            # pygame.draw.rect(
            #     self.fog,
            #     (0, 0, 0, delta_cone*delta_alpha_cone),
            #     vision_rect_left,
            # )

        surface.blit(self.fog, (0, 0))
