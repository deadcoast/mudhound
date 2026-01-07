"""
Theme engine for MudHound.

This module provides the Theme class and ThemeEngine for loading and applying
color themes to terminal UI components.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Handle Python 3.11+ where tomllib is built-in
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from mudhound.core.exceptions import ConfigError

# ANSI color codes
ANSI_COLORS = {
    # Basic colors (0-15)
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
    # Reset
    "reset": "\033[0m",
}

# Default theme definition
DEFAULT_THEME = {
    "name": "default",
    "colors": {
        "primary": "bright_cyan",
        "secondary": "cyan",
        "accent": "bright_magenta",
        # Semantic colors
        "success": "bright_green",
        "error": "bright_red",
        "warning": "bright_yellow",
        "info": "bright_blue",
        # Frame colors
        "frame_border": "bright_cyan",
        "frame_title": "bright_white",
        "frame_content": "white",
        # Content colors
        "text": "white",
        "text_dim": "bright_black",
        "highlight": "bright_yellow",
    },
    "animation": {
        "color_scheme": None,  # None means use default from config
    },
}


class Theme:
    """Represents a color theme for the terminal UI.

    Attributes:
        name: Theme name
        colors: Dictionary mapping semantic color names to ANSI color names
        animation_scheme: Optional animation color scheme override
    """

    def __init__(self, name: str, colors: Dict[str, str], animation_scheme: Optional[str] = None):
        """Initialize a Theme.

        Args:
            name: Theme name
            colors: Dictionary mapping semantic names to ANSI color names
            animation_scheme: Optional animation color scheme override
        """
        self.name = name
        self.colors = colors
        self.animation_scheme = animation_scheme

    def get_color(self, semantic_name: str) -> str:
        """Get ANSI escape code for a semantic color name.

        Args:
            semantic_name: Semantic color name (e.g., "success", "error")

        Returns:
            ANSI escape code string
        """
        # Get the ANSI color name from the theme
        ansi_color_name = self.colors.get(semantic_name, "white")

        # Resolve to ANSI escape code
        return ANSI_COLORS.get(ansi_color_name, ANSI_COLORS["white"])

    def apply(self, text: str, semantic_name: str) -> str:
        """Apply theme color to text.

        Args:
            text: Text to colorize
            semantic_name: Semantic color name

        Returns:
            Text with ANSI color codes applied
        """
        color_code = self.get_color(semantic_name)
        reset_code = ANSI_COLORS["reset"]
        return f"{color_code}{text}{reset_code}"

    @classmethod
    def from_dict(cls, theme_dict: Dict[str, Any]) -> "Theme":
        """Create a Theme from a dictionary (typically loaded from TOML).

        Args:
            theme_dict: Dictionary containing theme definition

        Returns:
            Theme instance
        """
        name = theme_dict.get("name", "unnamed")
        colors = theme_dict.get("colors", {})
        animation_scheme = theme_dict.get("animation", {}).get("color_scheme")

        return cls(name, colors, animation_scheme)


class ThemeEngine:
    """Manages theme loading and application.

    The ThemeEngine loads theme definitions from TOML files and provides
    methods to apply themes to UI components.

    Attributes:
        themes_dir: Directory containing theme files
        themes: Dictionary of loaded themes
        active_theme: Currently active theme
    """

    def __init__(self, themes_dir: Optional[Path] = None):
        """Initialize the ThemeEngine.

        Args:
            themes_dir: Directory containing theme TOML files
                       (defaults to mudhound/data/themes/)
        """
        if themes_dir is None:
            # Default to package data directory
            package_dir = Path(__file__).parent.parent
            themes_dir = package_dir / "data" / "themes"

        self.themes_dir = Path(themes_dir)
        self.themes: Dict[str, Theme] = {}
        self.active_theme: Theme = Theme.from_dict(DEFAULT_THEME)

        # Load default theme
        self.themes["default"] = self.active_theme

    def load_theme(self, theme_name: str) -> Theme:
        """Load a theme from a TOML file.

        Args:
            theme_name: Name of the theme (without .toml extension)

        Returns:
            Loaded Theme instance

        Raises:
            ConfigError: If theme file cannot be loaded or parsed
        """
        theme_path = self.themes_dir / f"{theme_name}.toml"

        if not theme_path.exists():
            # Return default theme as fallback
            return self.themes["default"]

        try:
            with open(theme_path, "rb") as f:
                theme_dict = tomllib.load(f)

            theme = Theme.from_dict(theme_dict)
            self.themes[theme_name] = theme
            return theme

        except Exception as e:
            raise ConfigError(
                f"Failed to load theme '{theme_name}': {e}") from e

    def set_active_theme(self, theme_name: str) -> None:
        """Set the active theme.

        Args:
            theme_name: Name of the theme to activate
        """
        # Try to load the theme if not already loaded
        if theme_name not in self.themes:
            theme = self.load_theme(theme_name)
        else:
            theme = self.themes[theme_name]

        self.active_theme = theme

    def get_color(self, semantic_name: str) -> str:
        """Get ANSI escape code for a semantic color name from active theme.

        Args:
            semantic_name: Semantic color name

        Returns:
            ANSI escape code string
        """
        return self.active_theme.get_color(semantic_name)

    def apply(self, text: str, semantic_name: str) -> str:
        """Apply active theme color to text.

        Args:
            text: Text to colorize
            semantic_name: Semantic color name

        Returns:
            Text with ANSI color codes applied
        """
        return self.active_theme.apply(text, semantic_name)

    def get_animation_scheme(self) -> Optional[str]:
        """Get animation color scheme override from active theme.

        Returns:
            Animation color scheme name or None if no override
        """
        return self.active_theme.animation_scheme


# Global theme engine instance
_theme_engine: Optional[ThemeEngine] = None


def get_theme_engine() -> ThemeEngine:
    """Get the global ThemeEngine instance.

    Returns:
        Global ThemeEngine instance
    """
    global _theme_engine
    if _theme_engine is None:
        _theme_engine = ThemeEngine()
    return _theme_engine


def set_theme(theme_name: str) -> None:
    """Set the active theme globally.

    Args:
        theme_name: Name of the theme to activate
    """
    engine = get_theme_engine()
    engine.set_active_theme(theme_name)


def apply_theme(text: str, semantic_name: str) -> str:
    """Apply active theme color to text (convenience function).

    Args:
        text: Text to colorize
        semantic_name: Semantic color name

    Returns:
        Text with ANSI color codes applied
    """
    engine = get_theme_engine()
    return engine.apply(text, semantic_name)
