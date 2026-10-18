
"""Brick: a destructible or unbreakable block."""

import pygame


class Brick:
    COLORS = {
        "normal": (200, 90, 90),
        "strong": (235, 150, 55),
        "unbreakable": (150, 90, 220),
    }

    def __init__(
        self,
        x,
        y,
        width,
        height,
        hits_remaining=None,
        color=None,
        brick_type="normal",
    ):
        if brick_type not in self.COLORS:
            raise ValueError(f"Unknown brick type: {brick_type}")

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type

        if brick_type == "unbreakable":
            self.hits_remaining = None
        elif hits_remaining is not None:
            self.hits_remaining = hits_remaining
        elif brick_type == "strong":
            self.hits_remaining = 2
        else:
            self.hits_remaining = 1

        self.color = color or self.COLORS[brick_type]

    def get_rect(self):
        return pygame.Rect(
            int(self.x), int(self.y), self.width, self.height
        )

    def take_hit(self):
        """Apply one hit. Return True if this brick is destroyed."""
        if self.brick_type == "unbreakable":
            return False

        self.hits_remaining -= 1

        # Show damage on strong bricks.
        if self.brick_type == "strong" and self.hits_remaining == 1:
            self.color = (255, 205, 100)

        return self.hits_remaining <= 0
