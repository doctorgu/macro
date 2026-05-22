"""util"""

import math
import time
import pyautogui
from pyscreeze import Point


def get_location(img_full_path: str, conf=0.9) -> Point | None:
    """True if image exists"""

    try:
        location = pyautogui.locateCenterOnScreen(img_full_path, confidence=conf)
        return location
    except (pyautogui.ImageNotFoundException, OSError):
        return None


def click_imgs(img_full_paths: list[str], conf=0.9) -> bool:
    """click images"""

    for img_full_path in img_full_paths:
        location = get_location(img_full_path, conf)
        if not location:
            continue

        x, y = location
        pyautogui.click(x, y)
        return True

    return False


def move_mouse_parabolic(
    *,
    x_to: int,
    y_to: int,
    height: float = 100.0,
    duration: float = 0.8,
    steps: int = 40,
    ease: bool = True,
) -> None:
    """
    Moves the mouse pointer from its current position to (x1, y1) in a parabolic path.

    :param x1: Target X coordinate.
    :param y1: Target Y coordinate.
    :param height: Curve height/offset perpendicular to the direct path.
                   Positive value curves in one direction, negative in the opposite.
    :param duration: Total duration of the movement in seconds.
    :param steps: Number of interpolation steps (higher is smoother).
    :param ease: If True, uses smoothstep (ease-in-ease-out) velocity instead of linear speed.
    """
    x_from, y_from = pyautogui.position()

    # Vector from P0 to P2
    dx = x_to - x_from
    dy = y_to - y_from
    dist = math.hypot(dx, dy)

    if dist < 1.0:
        pyautogui.moveTo(x_to, y_to)
        return

    # Midpoint of path
    mx = (x_from + x_to) / 2.0
    my = (y_from + y_to) / 2.0

    # Perpendicular unit vector (N) to the movement line
    # (nx, ny) is perpendicular to (dx, dy)
    nx = -dy / dist
    ny = dx / dist

    # Control point for quadratic Bezier (P1 = Midpoint + N * height)
    cx = mx + nx * height
    cy = my + ny * height

    # Calculate delay per step to hit target duration
    step_delay = duration / steps

    for i in range(steps + 1):
        t = i / steps
        if ease:
            # Smoothstep easing: 3t^2 - 2t^3
            t = 3 * (t**2) - 2 * (t**3)

        # Quadratic Bezier formula: (1-t)^2 * P0 + 2(1-t)t * P1 + t^2 * P2
        mt = 1 - t
        px = (mt**2) * x_from + 2 * mt * t * cx + (t**2) * x_to
        py = (mt**2) * y_from + 2 * mt * t * cy + (t**2) * y_to

        pyautogui.moveTo(int(px), int(py))
        time.sleep(step_delay)
