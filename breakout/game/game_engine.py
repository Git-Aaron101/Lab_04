
"""
GameEngine: owns the paddle, ball, bricks, lives, and scoring.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 82

STARTING_LIVES = 3
POINTS_PER_BRICK = 10
MAX_MULTIPLIER = 5


class GameEngine:
    def __init__(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.lives = STARTING_LIVES
        self.score = 0
        self.combo = 0
        self.multiplier = 1
        self.game_over = False
        self.bricks = self._build_bricks()

    def _build_bricks(self):
        bricks = []
        total_width = (
            BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        )
        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)

                # Mix the three types across the board.
                if row == 0 and col % 3 == 1:
                    brick_type = "unbreakable"
                elif row <= 1 or (row == 2 and col % 3 == 0):
                    brick_type = "strong"
                else:
                    brick_type = "normal"

                bricks.append(
                    Brick(
                        x, y, BRICK_WIDTH, BRICK_HEIGHT,
                        brick_type=brick_type,
                    )
                )

        return bricks

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

    def _reset_combo(self):
        self.combo = 0
        self.multiplier = 1

    def restart(self):
        """Restart the game after game over."""
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self._reset_ball()
        self.bricks = self._build_bricks()
        self.lives = STARTING_LIVES
        self.score = 0
        self._reset_combo()
        self.game_over = False

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.restart()

    def update(self):
        if self.game_over:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if (
            self.ball.get_rect().colliderect(self.paddle.get_rect())
            and self.ball.vy > 0
        ):
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        # Iterate over a copy because a destroyed brick is removed.
        for brick in self.bricks[:]:
            if handle_ball_brick_collision(self.ball, brick):
                destroyed = brick.take_hit()

                if destroyed:
                    self.bricks.remove(brick)

                    self.combo += 1
                    self.multiplier = min(
                        self.combo, MAX_MULTIPLIER
                    )
                    self.score += (
                        POINTS_PER_BRICK * self.multiplier
                    )

                # Only process one brick per frame.
                break

        if self.ball.is_below(HEIGHT):
            self.lives -= 1
            self._reset_combo()

            if self.lives <= 0:
                self.lives = 0
                self.game_over = True
            else:
                self._reset_ball()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface, self.paddle, self.ball, self.bricks
        )

        renderer.draw_text(
            surface, font, f"Bricks left: {len(self.bricks)}",
            (10, 8),
        )
        renderer.draw_text(
            surface, font, f"Lives: {self.lives}",
            (10, 30),
        )
        renderer.draw_text(
            surface, font, f"Score: {self.score}",
            (200, 8),
        )
        renderer.draw_text(
            surface, font, f"Combo: x{self.multiplier}",
            (200, 30),
        )

        if self.game_over:
            renderer.draw_banner(
                surface, font, "GAME OVER"
            )
            renderer.draw_text(
                surface, font, "Press R to restart",
                (WIDTH // 2 - 100, HEIGHT // 2 + 25),
            )
