
"""Ball-versus-brick collision handling."""


def handle_ball_brick_collision(ball, brick):
    """Bounce vertically on contact and return whether a hit occurred."""
    ball_rect = ball.get_rect()
    brick_rect = brick.get_rect()

    if not ball_rect.colliderect(brick_rect):
        return False

    if ball.vy > 0:
        ball.y = brick_rect.top - ball.radius
        ball.vy = -abs(ball.vy)
    elif ball.vy < 0:
        ball.y = brick_rect.bottom + ball.radius
        ball.vy = abs(ball.vy)

    return True
