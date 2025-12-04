"""Animation system components."""

from mudhound.ui.animation.timing import TimingEngine, EasingFunction
from mudhound.ui.animation.schemes import (
    ColorScheme,
    RAINBOW_COLORS_256,
    DARK_RAINBOW_COLORS_256,
    LIGHT_RAINBOW_COLORS_256,
    WHITE_COLORS,
    generate_rainbow_frame,
)
from mudhound.ui.animation.engine import AnimationRenderer

__all__ = [
    "TimingEngine",
    "EasingFunction",
    "ColorScheme",
    "RAINBOW_COLORS_256",
    "DARK_RAINBOW_COLORS_256",
    "LIGHT_RAINBOW_COLORS_256",
    "WHITE_COLORS",
    "generate_rainbow_frame",
    "AnimationRenderer",
]
