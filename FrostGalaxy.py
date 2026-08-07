"""
Module: alien_invasion.py

Runs the Frost Galaxy game.
This milestone demonstrates the custom ship, laser, and background.

Author: Wilerb Andre
Course: Python Programming
Assignment: Final Project - Milestone 1
Date: August 7, 2026
"""

import sys
import pygame

from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet


class AlienInvasion:
    """Manage the main game resources and game loop."""

    def __init__(self):
        """Initialize the game resources."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )

        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(
            self.settings.bg_file
        ).convert()

        self.bg = pygame.transform.scale(
            self.bg,
            (self.settings.screen_w, self.settings.screen_h)
        )

        self.running = True
        self.clock = pygame.time.Clock()

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)

    def run_game(self):
        """Run the main game loop."""
        while self.running:
            self._check_events()

            self.ship.update()
            self.alien_fleet.update_fleet()
            self._check_collisions()

            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _update_screen(self):
        """Draw the background, ship, and lasers."""
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()

        pygame.display.flip()

    def _check_collisions(self):
        """Check collisions between game objects."""
        self.alien_fleet.check_collisions(
            self.ship.arsenal.arsenal
        )

        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._reset_level()

    def _reset_level(self):
        """Reset the bullets and alien fleet."""
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
        

    def _check_events(self):
        """Respond to keyboard and quit events."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self._quit_game()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond when a key is pressed."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            self.ship.fire()

        elif event.key == pygame.K_q:
            self._quit_game()

    def _check_keyup_events(self, event):
        """Respond when a movement key is released."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _quit_game(self):
        """Close the game."""
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()