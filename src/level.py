"""Level and Camera objects file."""

from random import choice, randint

import pygame

from src.enemy import Enemy
from src.magic import MagicPlayer
from src.particles import AnimationPlayer
from src.player import Player
from src.settings import TILESIZE
from src.tile import Tile
from src.ui import UI
from src.upgrade import Upgrade
from src.utils import import_csv_layout, import_folder
from src.weapon import Weapon


class Level:
    """Level object that will draw objects in a layered manner."""

    def __init__(self, screen, cmd_line):
        """Initialize Level object."""
        # Get displace surface
        self.display_surface = screen.surface
        self.game_paused = False

        # Get Command Line focus info
        self.cmd_line = cmd_line

        # Sprite group setup
        self.visible_sprites = YsortedCameraGroup(self.display_surface)
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Sprite setup
        self.create_map()

        # User interface
        self.ui = UI(screen)
        self.upgrade = Upgrade(self.player)

        # Particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        """Create map from csv files."""
        layouts = {
            "boundary": import_csv_layout("src/images/map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("src/images/map/map_Grass.csv"),
            "object": import_csv_layout("src/images/map/map_Objects.csv"),
            "entities": import_csv_layout("src/images/map/map_Entities.csv"),
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
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites,
                                ],
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

                        if style == "entities":
                            if col == "394":
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                )
                            else:
                                if col == "390":
                                    monster_name = "bamboo"
                                elif col == "391":
                                    monster_name = "spirit"
                                elif col == "392":
                                    monster_name = "raccoon"
                                elif col == "393":
                                    monster_name = "squid"
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp,
                                )

    def create_attack(self):
        """Create attack based on current attack."""
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites]
        )

    def create_magic(self, style, strength, cost):
        """Create magic spell based on current magic style."""
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "flame":
            self.magic_player.flame(
                self.player, cost, [self.visible_sprites, self.attack_sprites]
            )

    def destroy_attack(self):
        """Destroy current attack image."""
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        """Player attack logic."""
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for _ in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset, [self.visible_sprites]
                                )
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type
                            )

    def damage_player(self, amount, attack_type):
        """Apply damage to player and use particles."""
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            # Spawn particles
            self.animation_player.create_particles(
                attack_type, self.player.rect.center, [self.visible_sprites]
            )

    def trigger_death_particles(self, pos, particle_type):
        """Display particles upon monster death."""
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        """Gain player experience."""
        self.player.exp += amount

    def toggle_menu(self):
        """Open upgrade menu with the game being paused."""
        self.game_paused = not self.game_paused

    def run(self):
        """Update and draw game."""
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.player_update(self.cmd_line.input.focus)
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


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

    def enemy_update(self, player):
        """Update enemy sprites."""
        enemy_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def player_update(self, cl_focus):
        """Update player sprite."""
        player_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "player"
        ]
        for player in player_sprites:
            if not cl_focus:
                player.player_movement()
