"""Module containing the upgrade menu."""

import pygame

from src.settings import (
    BAR_COLOR,
    BAR_COLOR_SELECTED,
    TEXT_COLOR,
    TEXT_COLOR_SELECTED,
    UI_BG_COLOR,
    UI_BORDER_COLOR,
    UI_FONT,
    UI_FONT_SIZE,
    UPGRADE_BG_COLOR_SELECTED,
)


class Upgrade:
    """Upgrade class."""

    def __init__(self, player):
        """Initialize object."""
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_num = len(player.stats)
        self.attribuite_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Item dimensions
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6

        # Item creation
        self.create_items()

        # Selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        """Capture user input."""
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_num - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        """Add cooldown on selection."""
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        """Create upgrade menu items."""
        self.item_list = []
        full_width = self.display_surface.get_size()[0]
        top = self.display_surface.get_size()[1] * 0.1

        for index, item in enumerate(range(self.attribute_num)):
            increment = full_width // self.attribute_num
            left = (item * increment) + (increment - self.width) // 2

            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        """Display upgrade menu."""
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            # Get attributes
            name = self.attribuite_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(
                self.display_surface, self.selection_index, name, value, max_value, cost
            )


class Item:
    """Upgrade Item class."""

    def __init__(self, left, top, width, height, index, font):
        """Initialize object."""
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        """Display stats names."""
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # Title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(
            midtop=self.rect.midtop + pygame.math.Vector2(0, 20)
        )
        # Cost
        cost_surf = self.font.render(f"{int(cost)}", False, color)
        cost_rect = cost_surf.get_rect(
            midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20)
        )

        # Draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        """Display stat bar."""
        # Drawing
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # Bar setup
        full_height = bottom[1] - top[1]
        relative_num = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_num, 30, 10)

        # Draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        """Trigger upgrade with user input."""
        upgrade_attribute = list(player.stats.keys())[self.index]

        if (
            player.exp >= player.upgrade_cost[upgrade_attribute]
            and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]
        ):
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        """Display upgrade menu."""
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)
