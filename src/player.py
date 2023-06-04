"""Module containing the player class."""

# import math

import pygame
import pygame.locals as locals

from src.settings import weapon_data
from src.utils import import_folder

# from src.connections import CONNECTIONS
# from src.maps import rooms_dict
# from src.room import Room


class Player(pygame.sprite.Sprite):
    """Player object that will control the player in the game."""

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        """Initialize player object."""
        super().__init__(groups)
        self.image = pygame.image.load("src/images/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Player graphics setup
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

    def import_player_assets(self):
        """Import player images to construct walking animations."""
        character_path = "src/images/player_test"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_attack": [],
            "down_attack": [],
            "left_attack": [],
            "right_attack": [],
        }

        for animation in self.animations.keys():
            full_path = character_path + "/" + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """Get user's input from keyboard."""
        if not self.attacking:
            keys_pressed = pygame.key.get_pressed()
            # Move input
            if keys_pressed[locals.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif keys_pressed[locals.K_s]:
                self.status = "down"
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys_pressed[locals.K_a]:
                self.direction.x = -1
                self.status = "left"
            elif keys_pressed[locals.K_d]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            # Attack input
            if keys_pressed[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # Attack input
            if keys_pressed[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

    def get_status(self):
        """Get player status based on direction."""
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        # attack
        if self.attacking:
            # TODO: do we want this?? not able to move while attacking?
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def move(self, speed):
        """Move player rectangle and hitbox (used for overlapping)."""
        if not self.direction.magnitude() == 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Check for horizontal and vertigal collisions."""
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        """Set attack cooldowns."""
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

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

    def update(self):
        """Update player."""
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)


# class Player:
#     """Player class."""

#     def __init__(self, screen, cmd_line, room=rooms_dict["start_room"]):
#         """Initialize player class."""
#         self.velocity = 3
#         self.player_size = (50, 50)
#         self.image_dir = "src/images/player"
#         self.vel_x = 0
#         self.vel_y = 0
#         self.player_frames = 0
#         self.vel_tolerance = 0.1
#         self.screen = screen
#         self.cmd_line = cmd_line
#         self.current_room = Room(self.screen, self.cmd_line, room)
#         self.rect = pygame.Rect((0, 0), self.player_size)
#         self.rect.x = room[4][0]
#         self.rect.y = room[4][1]
#         self._load_images()

#     def _load_images(self):
#         n_images_walking = 5
#         self.player_images_north = [
#             pygame.image.load(f"{self.image_dir}/north_{i}.jpg").convert_alpha()
#             for i in range(n_images_walking)
#         ]
#         self.player_images_south = [
#             pygame.image.load(f"{self.image_dir}/south_{i}.jpg").convert_alpha()
#             for i in range(n_images_walking)
#         ]
#         self.player_images_east = [
#             pygame.image.load(f"{self.image_dir}/east_{i}.jpg").convert_alpha()
#             for i in range(n_images_walking)
#         ]
#         self.player_images_west = [
#             pygame.transform.flip(image, True, False)
#             for image in self.player_images_east
#         ]
#         self.player_images_north_east = [
#             pygame.image.load(f"{self.image_dir}/north_east_{i}.jpg").convert_alpha()
#             for i in range(n_images_walking)
#         ]
#         self.player_images_south_east = [
#             pygame.image.load(f"{self.image_dir}/south_east_{i}.jpg").convert_alpha()
#             for i in range(n_images_walking)
#         ]
#         self.player_images_north_west = [
#             pygame.transform.flip(pygame.transform.rotate(image, 180), False, True)
#             for image in self.player_images_north_east
#         ]
#         self.player_images_south_west = [
#             pygame.transform.flip(pygame.transform.rotate(image, 180), False, True)
#             for image in self.player_images_south_east
#         ]

#     def _get_player_image_per_frame(self, player_images, state):
#         if self.player_frames < 50:
#             self.player_frames += 1
#         if state == "walking":
#             if self.player_frames >= 30:
#                 self.player_frames = 1
#             if self.player_frames < 5:
#                 player_image = player_images[0]
#             elif self.player_frames < 10:
#                 player_image = player_images[1]
#             elif self.player_frames < 15:
#                 player_image = player_images[2]
#             elif self.player_frames < 20:
#                 player_image = player_images[3]
#             elif self.player_frames < 30:
#                 player_image = player_images[4]
#         elif state == "standing":
#             player_image = player_images[0]
#         return player_image

#     def apply_event(self, event):
#         """Change the value of the direction variable according to event."""
#         ## TODO: change this to ASDW
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 self.direction = "E"
#             elif event.key == pygame.K_LEFT:
#                 self.direction = "W"
#             elif event.key == pygame.K_UP:
#                 self.direction = "N"
#             elif event.key == pygame.K_DOWN:
#                 self.direction = "S"

#     def move(self):
#         """Move player around when pressing arrow keys."""
#         # Storing the key pressed using key.get_pressed() method
#         key_pressed_is = pygame.key.get_pressed()

#         old_x, old_y = self.rect.x, self.rect.y
#         self.vel_x = 0
#         self.vel_y = 0
#         self.facing_N = False
#         self.facing_S = False
#         self.facing_E = False
#         self.facing_W = False
#         self.facing_NE = False
#         self.facing_NW = False
#         self.facing_SE = False
#         self.facing_SW = False

#         # Changing the coordinates of the player
#         if key_pressed_is[locals.K_a] and not key_pressed_is[locals.K_d]:
#             self.vel_x -= self.velocity
#             self.facing_W = True
#         if key_pressed_is[locals.K_d] and not key_pressed_is[locals.K_a]:
#             self.vel_x += self.velocity
#             self.facing_E = True
#         if key_pressed_is[locals.K_w] and not key_pressed_is[locals.K_s]:
#             self.vel_y -= self.velocity
#             self.facing_N = True
#         if key_pressed_is[locals.K_s] and not key_pressed_is[locals.K_w]:
#             self.vel_y += self.velocity
#             self.facing_S = True

#         # Update coordinates of the player
#         self.rect.x += self.vel_x
#         self.rect.y += self.vel_y

#         # Get 45 angle facing components
#         if self.facing_N and self.facing_E:
#             self.facing_NE = True
#             self.facing_N = False
#             self.facing_E = False
#         if self.facing_N and self.facing_W:
#             self.facing_NW = True
#             self.facing_N = False
#             self.facing_W = False
#         if self.facing_S and self.facing_E:
#             self.facing_SE = True
#             self.facing_S = False
#             self.facing_E = False
#         if self.facing_S and self.facing_W:
#             self.facing_SW = True
#             self.facing_S = False
#             self.facing_W = False

#         # facing = [
#         #     self.facing_N,
#         #     self.facing_S,
#         #     self.facing_E,
#         #     self.facing_W,
#         #     self.facing_NE,
#         #     self.facing_NW,
#         #     self.facing_SE,
#         #     self.facing_SW,
#         # ]
#         # if sum([face == True for face in facing]) > 1:
#         #     raise RuntimeError("Player is facing more than one direction at the same time.")

#         # Check for illegal movements colliding with walls
#         limit_is_x = False
#         limit_is_y = False
#         all_walls = (
#             self.current_room.walls
#             + self.current_room.hidden_doors
#             + self.current_room.npcs
#         )
#         for wall in all_walls:
#             if wall.is_open == False:
#                 if self.rect.colliderect(wall.rect):
#                     self.rect.x -= self.vel_x
#                     if self.rect.colliderect(wall.rect):
#                         limit_is_y = True
#                     self.rect.x += self.vel_x
#                     self.rect.y -= self.vel_y
#                     if self.rect.colliderect(wall.rect):
#                         limit_is_x = True
#                     self.rect.y += self.vel_y
#                     if limit_is_x:
#                         self.rect.x = old_x
#                     if limit_is_y:
#                         self.rect.y = old_y

#         all_doors = self.current_room.doors + self.current_room.hidden_doors
#         for door in all_doors:
#             if door.is_open == True:
#                 if self.rect.colliderect(door.rect):
#                     if door.name == "D00":
#                         current_door = door
#                     elif door.name == "D01":
#                         current_door = door
#                     self.get_connection_door(current_door)

#     def draw(self, canvas):
#         """Draw player on canvas."""
#         if (
#             abs(self.vel_x) < self.vel_tolerance
#             and abs(self.vel_y) < self.vel_tolerance
#         ):
#             state = "standing"
#         else:
#             state = "walking"

#         facing = False
#         if self.facing_NE:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_north_east, state
#             )
#             facing = True
#         if self.facing_NW:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_north_west, state
#             )
#             facing = True
#         if self.facing_SE:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_south_east, state
#             )
#             facing = True
#         if self.facing_SW:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_south_west, state
#             )
#             facing = True
#         if self.facing_N:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_north, state
#             )
#             facing = True
#         if self.facing_W:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_west, state
#             )
#             facing = True
#         if self.facing_E:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_east, state
#             )
#             facing = True
#         if self.facing_S:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_south, state
#             )

#         if not facing:
#             player_image = self._get_player_image_per_frame(
#                 self.player_images_south, state
#             )

#         canvas.blit(player_image, (self.rect.x, self.rect.y))

#     def get_connection_door(self, door):
#         """Find the connection for a certain door and redirect the player there."""
#         door_found = False
#         for connection in CONNECTIONS:
#             if connection[0] == door.name:
#                 next_door = connection[1]
#                 next_room = connection[3]
#                 self.current_room = Room(
#                     self.screen, self.cmd_line, rooms_dict[next_room]
#                 )
#                 all_doors = self.current_room.doors + self.current_room.hidden_doors
#                 for door in all_doors:
#                     if door.name == next_door:
#                         self.rect.x, self.rect.y = (
#                             door.rect.x + connection[4],
#                             door.rect.y + connection[5],
#                         )
#                         door_found = True
#                         break
#             if door_found:
#                 break

#     def get_closest_object_in_room(self):
#         """Find closest interactable objects to the player."""
#         closest_objects = []
#         distances = []
#         dist = 100
#         cx = self.rect.centerx
#         cy = self.rect.centery
#         interact_objects = self.current_room.walls + self.current_room.hidden_doors
#         for obj in interact_objects:
#             obj_x = obj.rect.centerx
#             obj_y = obj.rect.centery
#             distance = math.sqrt(abs(cx - obj_x) ** 2 + abs(cy - obj_y) ** 2)
#             if dist > distance:
#                 closest_objects.append(obj)
#                 distances.append(distance)
#         return closest_objects, distances
