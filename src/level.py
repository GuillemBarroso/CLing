"""Level and Camera objects file."""

from random import choice

import pygame

from src.player import Player
from src.settings import TILESIZE
from src.tile import Tile
from src.ui import UI
from src.utils import import_csv_layout, import_folder
from src.weapon import Weapon


class Level:
    """Level object that will draw objects in a layered manner."""

    def __init__(self, screen):
        """Initialize Level object."""
        # Get displace surface
        self.display_surface = screen.surface

        # Sprite group setup
        self.visible_sprites = YsortedCameraGroup(self.display_surface)
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack sprites
        self.current_attack = None

        # Sprite setup
        self.create_map()

        # User interface
        self.ui = UI(screen)

    def create_map(self):
        """Create map from csv files."""
        layouts = {
            "boundary": import_csv_layout("src/images/map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("src/images/map/map_Grass.csv"),
            "object": import_csv_layout("src/images/map/map_Objects.csv"),
        }
        graphics = {
            "grass": import_folder("src/images/map/grass"),
            "objects": import_folder("src/images/map/objects"),
        }

        for style, layout in layouts.items():
            for i_row, row in enumerate(layout):
                for i_col, col in enumerate(row):
                    if col != "-1":
                        x = i_col * TILESIZE
                        y = i_row * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")

                        if style == "grass":
                            random_grass_img = choice(graphics["grass"])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "grass",
                                random_grass_img,
                            )

                        if style == "object":
                            surf = graphics["objects"][int(col)]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                surf,
                            )

        self.player = Player(
            (2000, 1200),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
        )

    def create_attack(self):
        """Create attack based on current attack."""
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        """Destroy current attack image."""
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        """Update and draw game."""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


class YsortedCameraGroup(pygame.sprite.Group):
    """Camera object sorting elements by its y coordinate."""

    def __init__(self, display_surface):
        """Initialize object."""
        super().__init__()
        self.display_surface = display_surface
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Create floor
        self.floor_surf = pygame.image.load("src/images/map/map_ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """Custom draw for sprites."""
        # Get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Draw sprites with offset
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
