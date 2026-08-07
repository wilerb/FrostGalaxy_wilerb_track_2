from pathlib import Path


class Settings:
    """Store the game settings and asset paths."""

    def __init__(self) -> None:
        """Initialize the game settings."""

        self.name = "Frost Galaxy"

        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60

        self.bg_file = (
            Path.cwd() / "Assets" / "images" / "bg-img.png"
        )

        self.ship_file = (
            Path.cwd() / "Assets" / "images" / "new-ship.png"
        )

        self.bullet_file = (
            Path.cwd() / "Assets" / "images" / "bullet.png"
        )

        self.ship_w = 65
        self.ship_h = 90
        self.ship_speed = 5

        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_speed = 7
        self.bullet_amount = 5