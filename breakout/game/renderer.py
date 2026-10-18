
"""Renderer: all Pygame drawing lives here."""

import pygame

WIDTH, HEIGHT = 640, 520
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (20, 20, 30)
COLOR_PADDLE = (80, 180, 255)
COLOR_BALL = (240, 240, 240)
COLOR_TEXT = (255, 255, 255)
COLOR_BORDER = (10, 10, 15)


def draw_scene(surface, paddle, ball, bricks):
    surface.fill(COLOR_BG)

    for brick in bricks:
        rect = brick.get_rect()

        pygame.draw.rect(
            surface, brick.color, rect, border_radius=3
        )
        pygame.draw.rect(
            surface, COLOR_BORDER, rect, 1, border_radius=3
        )

        # Strong bricks show their remaining durability.
        if brick.brick_type == "strong":
            for hit in range(brick.hits_remaining):
                marker_x = rect.left + 8 + hit * 10
                pygame.draw.circle(
                    surface, (255, 245, 210),
                    (marker_x, rect.centery), 2
                )

        # Unbreakable bricks have a visible cross pattern.
        elif brick.brick_type == "unbreakable":
            pygame.draw.line(
                surface, (225, 205, 255),
                rect.topleft, rect.bottomright, 2
            )
            pygame.draw.line(
                surface, (225, 205, 255),
                rect.topright, rect.bottomleft, 2
            )

    pygame.draw.rect(
        surface, COLOR_PADDLE, paddle.get_rect(),
        border_radius=4
    )
    pygame.draw.circle(
        surface, COLOR_BALL,
        (int(ball.x), int(ball.y)), ball.radius
    )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    banner = font.render(text, True, (255, 220, 80))
    rect = banner.get_rect(
        center=(surface.get_width() // 2,
                surface.get_height() // 2)
    )
    surface.blit(banner, rect)
