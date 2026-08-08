"""
Module: alien_fleet.py

Creates, moves, and manages the alien fleet.

Author: Wilerb Andre
Course: Python Programming
Assignment: Final Project - Milestone 1
Date: August 7, 2026
"""

import pygame
from alien import Alien
from typing import TYPE_CHECKING
import math

if TYPE_CHECKING:
    from FrostGalaxy import AlienInvasion


class AlienFleet:
    """Manage the alien fleet."""

    def __init__(self, game: 'AlienInvasion'):
        """Initialize the alien fleet."""
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed
        self.formation = 0

        self.create_fleet()

    def create_fleet(self):
        """Create the next alien fleet formation."""
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        if self.formation == 0:
            self._create_diamond_fleet(alien_w, alien_h, screen_w)

        elif self.formation == 1:
            fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
            x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)

            self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

        elif self.formation == 2:
            self._create_circle_fleet(alien_w, alien_h, screen_w)

        self.formation = (self.formation + 1) % 3

    def _create_diamond_fleet(self, alien_w, alien_h, screen_w):
        """Create aliens in a diamond-shaped formation."""
        center_x = screen_w // 2
        start_y = 80

        spacing_x = alien_w * 2
        spacing_y = alien_h * 2

        rows = [6, 11, 14, 11, 6]

        for row, alien_count in enumerate(rows):
            current_y = start_y + row * spacing_y
            row_width = (alien_count - 1) * spacing_x
            start_x = center_x - row_width // 2

            for col in range(alien_count):
                current_x = start_x + col * spacing_x
                self._create_alien(current_x, current_y)

    def _create_circle_fleet(self, alien_w, alien_h, screen_w):
        """Create aliens in a filled circular formation."""
        center_x = screen_w // 2
        center_y = 230

        radius = 270
        spacing = 60

        current_radius = 0

        while current_radius <= radius:
            if current_radius == 0:
                self._create_alien(center_x, center_y)
            else:
                circumference = 2 * math.pi * current_radius
                alien_count = int(circumference // spacing)

                for i in range(alien_count):
                    angle = 2 * math.pi * i / alien_count

                    current_x = center_x + current_radius * math.cos(angle)
                    current_y = center_y + current_radius * math.sin(angle)

                    self._create_alien(int(current_x), int(current_y))

            current_radius += spacing

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """Create aliens in a rectangular formation."""
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset

                if col % 2 == 0 or row % 2 != 0:
                    continue

                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """Calculate the starting position of the fleet."""
        half_screen = self.settings.screen_h / 2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h

        x_offset = int((screen_w - fleet_horizontal_space) // 2)
        y_offset = int((half_screen - fleet_vertical_space) // 2)

        return x_offset, y_offset

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h) -> tuple[int, int]:
        """Calculate the size of the alien fleet."""
        fleet_w = screen_w // alien_w
        fleet_h = (screen_h // 2) // alien_h

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        return int(fleet_w), int(fleet_h)

    def _create_alien(self, current_x: int, current_y: int):
        """Create one alien."""
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Check whether the fleet reached a screen edge."""
        alien: Alien

        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break

    def _drop_alien_fleet(self):
        """Move the fleet down."""
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def update_fleet(self):
        """Update the alien fleet."""
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """Draw all aliens."""
        alien: Alien

        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """Check collisions between aliens and another sprite group."""
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_bottom(self) -> bool:
        """Check whether an alien reached the bottom of the screen."""
        alien: Alien

        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True

        return False

    def check_destroyed_status(self):
        """Return True when all aliens are destroyed."""
        return not self.fleet