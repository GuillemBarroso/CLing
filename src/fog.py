"""Module containing the Fog object."""

import math

import pygame

from src.settings import HEIGHT, WIDTH


class Fog:
    """Fog object."""

    def __init__(self):
        """Initialize object."""
        self.fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Vision camp parameters
        self.AWARENESS_RADIUS = 100
        self.VISION_ANGLE = 75
        self.VISION_LENGTH = 500

        self.FOG_OPACITY = 200
        self.SCALE_FACTOR = 0.996
        self.NUM_POLYGONS = 100

    @staticmethod
    def get_polygon_centroid(vertices):
        """Return the centroid of a polygon defined with a list of vertices."""
        return (
            sum(x for x, _ in vertices) / len(vertices),
            sum(y for _, y in vertices) / len(vertices),
        )

    def center_polygons(self, polygon_ref, polygons_list):
        """Center a list of polygons with respect to a reference polygon."""
        # Get centroid of the reference polygon
        centroid_ref = self.get_polygon_centroid(polygon_ref)

        centered_polygons = []
        centered_polygons.append(polygon_ref)
        for polygon in polygons_list:
            # Get centroid of the polygon
            centroid = self.get_polygon_centroid(polygon)

            # Calculate the offset required to center the polygon
            offset_x = centroid_ref[0] - centroid[0]
            offset_y = centroid_ref[1] - centroid[1]

            # Compute and store the vertices of the centered polygon
            centered_polygons.append(
                [(int(x + offset_x), int(y + offset_y)) for x, y in polygon]
            )
        return centered_polygons

    @staticmethod
    def get_scaled_polygons(polygon, scale_factor, num_polygons):
        """Scale polygon a number of times using a scale factor."""
        scaled_polygons = []
        for _ in range(num_polygons):
            scaled_polygons.append(polygon)
            scaled_polygon = [
                (vertex[0] * scale_factor, vertex[1] * scale_factor)
                for vertex in polygon
            ]
            polygon = scaled_polygon
        return scaled_polygons

    def get_circle_vertices(self, player_pos, player_angle):
        """Return list of vertices in the circle behind the player."""
        vertices = []
        angle_ini = player_angle - self.VISION_ANGLE + 90
        angle_end = player_angle + 180 + self.VISION_ANGLE - 90
        for angle in range(angle_ini, angle_end, 5):
            circle_offset_x = math.sin(math.radians(angle)) * self.AWARENESS_RADIUS
            circle_offset_y = math.cos(math.radians(angle)) * self.AWARENESS_RADIUS

            vertices.append(
                (player_pos[0] - circle_offset_x, player_pos[1] + circle_offset_y)
            )
        return vertices

    def draw(self, surface, player, offset):
        """Draw fog object to visualize the player's vision camp."""
        # Fill surface with black color and alpha = fog_opacity
        self.fog.fill((0, 0, 0, self.FOG_OPACITY))

        # Get current player's parameters
        player_pos = player.rect.center - offset
        player_angle = player.aim_angle

        circle_vertices = self.get_circle_vertices(player_pos, player_angle)
        vision_vertices = [
            (
                player_pos[0]
                + math.cos(math.radians(player_angle - self.VISION_ANGLE / 2))
                * self.VISION_LENGTH,
                player_pos[1]
                + math.sin(math.radians(player_angle - self.VISION_ANGLE / 2))
                * self.VISION_LENGTH,
            ),
            (
                player_pos[0]
                + math.cos(math.radians(player_angle + self.VISION_ANGLE / 2))
                * self.VISION_LENGTH,
                player_pos[1]
                + math.sin(math.radians(player_angle + self.VISION_ANGLE / 2))
                * self.VISION_LENGTH,
            ),
        ]
        vision_vertices = vision_vertices + circle_vertices

        polygons = self.get_scaled_polygons(
            vision_vertices, self.SCALE_FACTOR, self.NUM_POLYGONS
        )
        polygons = self.center_polygons(polygons[0], polygons[1:])

        for i in range(self.NUM_POLYGONS):
            alpha = self.FOG_OPACITY - i / self.NUM_POLYGONS * self.FOG_OPACITY
            pygame.draw.polygon(self.fog, (0, 0, 0, alpha), polygons[i])

        surface.blit(self.fog, (0, 0))
