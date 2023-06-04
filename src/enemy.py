"""Module containin the enemy mechanics."""

import pygame

from src.entity import Entity
from src.settings import monster_data
from src.utils import import_folder


class Enemy(Entity):
    """Class containing the Enemey information."""

    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        """Initialize Enemy object."""
        super().__init__(groups)
        self.sprite_type = "enemy"

        # Graphics setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]

        # Player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400  # TODO: move to monster data
        self.damage_player = damage_player

        # Invencibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invencibility_duration = 300

    def import_graphics(self, name):
        """Import graphics to animate enemies."""
        self.animations = {"idle": [], "move": [], "attack": []}
        main_path = f"src/images/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        """Compute distance and direction from player to enemy."""
        enemy_vect = pygame.math.Vector2(self.rect.center)
        player_vect = pygame.math.Vector2(player.rect.center)
        distance = (player_vect - enemy_vect).magnitude()
        if distance > 0:
            direction = (player_vect - enemy_vect).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        """Get enemy status."""
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        """Define enemy actions."""
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        """Animate enemies."""
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Flicker when being hit
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        """Enemy attack cooldown."""
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invencibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        """Get player damage to enemies."""
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                pass  # magic damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        """Check if enemies are dead."""
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        """Backwards reaction of enemies upon being hit."""
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        """Update enemies actions."""
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        """Update enemy."""
        self.get_status(player)
        self.actions(player)
