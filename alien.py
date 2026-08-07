"""
Module: alien.py

Creates and manages individual alien sprites.

Author: Wilerb Andre
Course: Python Programming
Assignment: Final Project - Milestone 1
Date: August 7, 2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet


class Alien(Sprite):
    """Manage one alien in the fleet."""

    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Initialize the alien and its position."""
        super().__init__()

        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(
            self.image,
            (self.settings.alien_w, self.settings.alien_h)
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien horizontally."""
        temp_speed = self.settings.fleet_speed
        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """Check whether the alien reached a screen edge."""
        return self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left

    def draw_alien(self):
        """Draw the alien on the screen."""
        self.screen.blit(self.image, self.rect)