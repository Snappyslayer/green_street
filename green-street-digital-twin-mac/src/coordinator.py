"""Adaptive coordinator logic for the Green Street project."""

from src.config import (
    AMBIENT_DARK_THRESHOLD,
    BRIGHTNESS_HIGH,
    BRIGHTNESS_LOW,
    BRIGHTNESS_MEDIUM,
    BRIGHTNESS_SAFE_DEFAULT,
)


def decide_brightness(status: str, motion: bool, ambient: int) -> int:
    """Return the brightness command for one node.

    Rules:
    - offline/stale/unknown node -> safe default brightness
    - motion detected -> high brightness
    - no motion and dark ambient light -> medium brightness
    - no motion and bright ambient light -> low brightness
    """
    if status != "online":
        return BRIGHTNESS_SAFE_DEFAULT

    if motion:
        return BRIGHTNESS_HIGH

    if ambient < AMBIENT_DARK_THRESHOLD:
        return BRIGHTNESS_MEDIUM

    return BRIGHTNESS_LOW
