"""Module containing the particle creation."""

from random import choice

import pygame

from src.utils import import_folder


class AnimationPlayer:
    """Class that will load all the images."""

    def __init__(self):
        """Initialize object."""
        self.particles_path = "src/images/particles/"
        self.frames = {
            # Magic
            "flame": import_folder(self.particles_path + "flame/frames"),
            "aura": import_folder(self.particles_path + "aura"),
            "heal": import_folder(self.particles_path + "heal/frames"),
            # Attacks
            "claw": import_folder(self.particles_path + "claw"),
            "slash": import_folder(self.particles_path + "slash"),
            "sparkle": import_folder(self.particles_path + "sparkle"),
            "leaf_attack": import_folder(self.particles_path + "leaf_attack"),
            "thunder": import_folder(self.particles_path + "thunder"),
            # Monster deaths
            "squid": import_folder(self.particles_path + "smoke_orange"),
            "raccoon": import_folder(self.particles_path + "raccoon"),
            "spirit": import_folder(self.particles_path + "nova"),
            "bamboo": import_folder(self.particles_path + "bamboo"),
            # Leafs
            "leaf": (
                import_folder(self.particles_path + "leaf1"),
                import_folder(self.particles_path + "leaf2"),
                import_folder(self.particles_path + "leaf3"),
                import_folder(self.particles_path + "leaf4"),
                import_folder(self.particles_path + "leaf5"),
                import_folder(self.particles_path + "leaf6"),
                self.reflect_images(import_folder(self.particles_path + "leaf1")),
                self.reflect_images(import_folder(self.particles_path + "leaf2")),
                self.reflect_images(import_folder(self.particles_path + "leaf3")),
                self.reflect_images(import_folder(self.particles_path + "leaf4")),
                self.reflect_images(import_folder(self.particles_path + "leaf5")),
                self.reflect_images(import_folder(self.particles_path + "leaf6")),
            ),
        }

    def reflect_images(self, frames):
        """Reflect/flip images to have more varaiety."""
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        """Create particles for grass destruction."""
        animation_frames = choice(self.frames["leaf"])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        """Create generic particles."""
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    """Particles effect object."""

    def __init__(self, pos, animation_frames, groups):
        """Initialize object."""
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """Animate particles."""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        """Update particle animation."""
        self.animate()
