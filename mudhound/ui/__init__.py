"""User interface and presentation layer."""

from mudhound.ui.frames import (
    BorderStyle,
    FrameRenderer,
    render_frame_with_header,
    render_simple_frame,
)
from mudhound.ui.layout import LayoutManager
from mudhound.ui.renderer import UIRenderer
from mudhound.ui.theme import Theme, ThemeEngine, apply_theme, get_theme_engine, set_theme

__all__ = [
    "LayoutManager",
    "BorderStyle",
    "FrameRenderer",
    "render_simple_frame",
    "render_frame_with_header",
    "Theme",
    "ThemeEngine",
    "get_theme_engine",
    "set_theme",
    "apply_theme",
    "UIRenderer",
]
