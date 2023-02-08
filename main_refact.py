"""Main module of the game. Run this module to start the game."""

import pygame

from src.canvas import build_canvas, get_canvas
from src.colors import WHITE
from src.command_line import CL
from src.execute_commands import activate_cl_commands
from src.player import Player
from src.screen import Screen


class Game:
    """Game class."""

    def __init__(self):
        """Initialize object."""
        pygame.init()
        pygame.display.set_caption("CLing")
        self.clock = pygame.time.Clock()
        self.canvas = get_canvas()
        self.running = True
        self.FPS = 60

    def main(self):
        """Main game loop."""
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def events(self):
        """Game loop events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            activate_cl_commands(event, self.cmd_line)

    def new(self):
        """Start a new game."""
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.hidden_doors = pygame.sprite.LayeredUpdates()

        self.cmd_line = CL(canvas=self.canvas)
        self.screen = Screen(self.canvas, self.cmd_line)
        self.player = Player(self)

        # Build layout
        build_canvas(self.canvas, self.screen, self.cmd_line)

    def update(self):
        """Game loop updates."""
        self.all_sprites.update()

    def draw(self):
        """Draw objects."""
        self.screen.surface.fill(WHITE)
        self.all_sprites.draw(self.screen.surface)
        self.clock.tick(self.FPS)
        pygame.display.update()


game = Game()
game.new()
while game.running:
    game.main()

pygame.quit()
