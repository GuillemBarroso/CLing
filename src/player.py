"""Module containing the player class."""

import math

import pygame
import pygame.locals as locals

from src.entity import Entity
from src.events_definition import ENTRY_CAVE
from src.settings import HITBOX_OFFSET, magic_data, weapon_data
from src.tile_interaction import PLAYER_ACTION_RADIUS, TILE_PRIORITY
from src.utils import import_folder


class Player(Entity):
    """Player object that will control the player in the game."""

    def __init__(
        self,
        pos,
        groups,
        obstacle_sprites,
        door_sprites,
        create_attack,
        destroy_attack,
        create_magic,
    ):
        """Initialize player object."""
        super().__init__(groups)
        self.sprite_type = "player"
        self.image = pygame.image.load("src/images/player/S/S_0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["player"])

        # Player graphics setup
        self.import_player_assets()
        self.status = "S"
        self.aim_angle = 90

        # Movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.door_sprites = door_sprites
        self.rotating = False
        self.ROTATION_SPEED = 4  # units: degrees [º]

        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Stats
        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 5}
        self.max_stats = {
            "health": 300,
            "energy": 140,
            "attack": 20,
            "magic": 10,
            "speed": 10,
        }
        self.upgrade_cost = {
            "health": 100,
            "energy": 100,
            "attack": 100,
            "magic": 100,
            "speed": 100,
        }
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.exp = 5000

        # Damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerablility_duration = 500

        # Sound effects
        self.weapon_attack_sound = pygame.mixer.Sound("src/audio/sword.wav")
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        """Import player images to construct walking animations."""
        character_path = "src/images/player"
        self.animations = {
            "N": [],
            "S": [],
            "W": [],
            "E": [],
            "NW": [],
            "NE": [],
            "SW": [],
            "SE": [],
            "N_idle": [],
            "S_idle": [],
            "W_idle": [],
            "E_idle": [],
            "NW_idle": [],
            "NE_idle": [],
            "SW_idle": [],
            "SE_idle": [],
            "N_attack": [],
            "S_attack": [],
            "W_attack": [],
            "E_attack": [],
            "NW_attack": [],
            "NE_attack": [],
            "SW_attack": [],
            "SE_attack": [],
        }

        for animation in self.animations.keys():
            full_path = character_path + "/" + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """Get user's input from keyboard."""
        if not self.attacking:
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[locals.K_RIGHT] or keys_pressed[locals.K_LEFT]:
                self.rotating = True
            else:
                self.rotating = False

            # Move input
            if keys_pressed[locals.K_w] and keys_pressed[locals.K_a]:
                self.move_direction.y = -1
                self.status = "NW"
                if not self.rotating:
                    self.aim_angle = -135
            elif keys_pressed[locals.K_w] and keys_pressed[locals.K_d]:
                self.move_direction.y = -1
                self.status = "NE"
                if not self.rotating:
                    self.aim_angle = -45
            elif keys_pressed[locals.K_s] and keys_pressed[locals.K_a]:
                self.move_direction.y = 1
                self.status = "SW"
                if not self.rotating:
                    self.aim_angle = 135
            elif keys_pressed[locals.K_s] and keys_pressed[locals.K_d]:
                self.move_direction.y = 1
                self.status = "SE"
                if not self.rotating:
                    self.aim_angle = 45
            elif keys_pressed[locals.K_w]:
                self.move_direction.y = -1
                self.status = "N"
                if not self.rotating:
                    self.aim_angle = -90
            elif keys_pressed[locals.K_s]:
                self.move_direction.y = 1
                self.status = "S"
                if not self.rotating:
                    self.aim_angle = 90
            else:
                self.move_direction.y = 0

            if keys_pressed[locals.K_w] and keys_pressed[locals.K_a]:
                self.move_direction.x = -1
                self.status = "NW"
                if not self.rotating:
                    self.aim_angle = -135
            elif keys_pressed[locals.K_w] and keys_pressed[locals.K_d]:
                self.move_direction.x = 1
                self.status = "NE"
                if not self.rotating:
                    self.aim_angle = -45
            elif keys_pressed[locals.K_s] and keys_pressed[locals.K_a]:
                self.move_direction.x = -1
                self.status = "SW"
                if not self.rotating:
                    self.aim_angle = 135
            elif keys_pressed[locals.K_s] and keys_pressed[locals.K_d]:
                self.move_direction.x = 1
                self.status = "SE"
                if not self.rotating:
                    self.aim_angle = 45
            elif keys_pressed[locals.K_a]:
                self.move_direction.x = -1
                self.status = "W"
                if not self.rotating:
                    self.aim_angle = 180
            elif keys_pressed[locals.K_d]:
                self.move_direction.x = 1
                self.status = "E"
                if not self.rotating:
                    self.aim_angle = 0
            else:
                self.move_direction.x = 0

            # Aim input
            if keys_pressed[locals.K_RIGHT]:
                self.aim_angle += self.ROTATION_SPEED % 360
            elif keys_pressed[locals.K_LEFT]:
                self.aim_angle -= self.ROTATION_SPEED % 360

            self.aim_direction.x += math.cos(math.radians(self.aim_angle))
            self.aim_direction.y += math.sin(math.radians(self.aim_angle))

            # Attack input
            if keys_pressed[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            # Magic input
            if keys_pressed[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = (
                    list(magic_data.values())[self.magic_index]["strength"]
                    + self.stats["magic"]
                )
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)

            # Switch weapon
            if keys_pressed[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # Switch magic
            if keys_pressed[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        """Get player status based on move_direction."""
        # idle
        if self.move_direction.x == 0 and self.move_direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        # attack
        if self.attacking:
            # TODO: do we want this?? not able to move while attacking?
            self.move_direction.x = 0
            self.move_direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def cooldowns(self):
        """Set attack cooldowns."""
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if (
                current_time - self.attack_time
                >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]
            ):
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerablility_duration:
                self.vulnerable = True

    def animate(self):
        """Animate player movement."""
        animation = self.animations[self.status]

        # Loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Add flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        """Get full damage = base + weapon damage."""
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        """Get full damage = base + spell damage."""
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]["strength"]
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        """Return stat value by index."""
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        """Return stat cost by index."""
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        """Set energy recovery system."""
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def check_doors(self):
        """Check if the player collides with a door."""
        for sprite in self.door_sprites:
            if sprite.rect.colliderect(self.hitbox):
                pygame.event.post(pygame.event.Event(ENTRY_CAVE))

    def rotate_surface_with_pivot_offset(self, surface, pivot, offset):
        """Return the rotated image and rectangle given a pivot point and an offset."""
        rotated_image = pygame.transform.rotozoom(surface, -self.aim_angle, 1)
        rotated_offset = offset.rotate(self.aim_angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect

    def draw_aim(self, surf, player_offset):
        """Draw aiming arrow pointing to the aiming direction of the player."""
        aim_surface = pygame.Surface((20, 10), pygame.SRCALPHA)
        pivot = self.rect.center - player_offset
        pygame.draw.polygon(
            aim_surface, (255, 0, 0), ((0, 5), (20, 0), (15, 5), (20, 10))
        )
        # pygame.draw.polygon(
        #     aim_surface, (255, 0, 0), ((5, 0), (0, 20), (5, 15), (10, 20))
        # )

        offset = pygame.math.Vector2(30, 0)
        # offset = pygame.math.Vector2(0, -30)
        rotated_image, rect = self.rotate_surface_with_pivot_offset(
            aim_surface, pivot, offset
        )
        surf.blit(rotated_image, rect)

    def update(self):
        """Update player but not its movement."""
        self.cooldowns()
        self.energy_recovery()

    def player_movement(self):
        """Apply player movement from keyboard input."""
        self.input()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.check_doors()

    def get_closest_sprites(self, sprites):
        """Find closest interactable sprites to the player."""
        closest_sprites = []
        distances = []
        cx = self.rect.centerx
        cy = self.rect.centery
        for sprite in sprites:
            obj_x = sprite.rect.centerx
            obj_y = sprite.rect.centery
            tile_priority = TILE_PRIORITY[sprite.sprite_type]
            distance = math.sqrt(abs(cx - obj_x) ** 2 + abs(cy - obj_y) ** 2)
            distance /= tile_priority
            if PLAYER_ACTION_RADIUS > distance:
                closest_sprites.append(sprite)
                distances.append(distance)
        return closest_sprites, distances
