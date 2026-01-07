"""
Color scheme definitions for animated elements.

This module provides color palettes and utilities for applying rainbow
color cycling effects to ASCII art and animated terminal graphics.
"""

from enum import Enum


class ColorScheme(Enum):
    """
    Defines available color schemes for animated elements.
    Each scheme maps to a set of ANSI 256-color palette values.
    """
    RAINBOW = "rainbow"           # Full spectrum cycling
    DARK_RAINBOW = "dark-rainbow" # Muted/darker rainbow
    LIGHT_RAINBOW = "light-rainbow" # Bright/pastel rainbow
    WHITE = "white"               # Monochrome white
    THEME = "theme"               # Use current theme colors


# ANSI 256-color palette definitions
# Each palette contains 8 colors for cycling through the spectrum

RAINBOW_COLORS_256 = [196, 208, 226, 46, 51, 21, 129, 201]
"""Full spectrum rainbow: red -> orange -> yellow -> green -> cyan -> blue -> purple -> magenta"""

DARK_RAINBOW_COLORS_256 = [88, 130, 136, 22, 23, 18, 54, 90]
"""Muted/darker rainbow spectrum for subtle animations"""

LIGHT_RAINBOW_COLORS_256 = [210, 216, 228, 120, 123, 111, 183, 219]
"""Bright/pastel rainbow spectrum for light backgrounds"""

WHITE_COLORS = [255]
"""Monochrome white for non-colored animations"""


def generate_rainbow_frame(
    base_art: str,
    color_offset: int,
    scheme: ColorScheme
) -> str:
    """
    Generate a single rainbow frame by applying color offset to base ASCII art.
    
    This function takes plain ASCII art and applies ANSI color codes to create
    a rainbow effect. The color_offset parameter allows cycling through colors
    to create animation frames.
    
    Algorithm:
    1. Parse base ASCII art into lines
    2. For each character, calculate color index: (char_index + offset) % len(colors)
    3. Wrap character with ANSI color escape sequence
    4. Join characters into complete frame
    
    Args:
        base_art: Plain ASCII art string (no ANSI codes)
        color_offset: Offset for color cycling (0 to len(colors)-1)
        scheme: ColorScheme enum value specifying which palette to use
        
    Returns:
        ASCII art string with ANSI color codes applied
        
    Example:
        >>> art = "HELLO"
        >>> frame = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)
        >>> # Returns art with each character in a different rainbow color
    """
    # Select color palette based on scheme
    colors = {
        ColorScheme.RAINBOW: RAINBOW_COLORS_256,
        ColorScheme.DARK_RAINBOW: DARK_RAINBOW_COLORS_256,
        ColorScheme.LIGHT_RAINBOW: LIGHT_RAINBOW_COLORS_256,
        ColorScheme.WHITE: WHITE_COLORS,
    }.get(scheme, RAINBOW_COLORS_256)

    if scheme == ColorScheme.THEME:
        # THEME scheme should use theme colors, but for now default to rainbow
        # This will be integrated with the theme engine later
        colors = RAINBOW_COLORS_256

    result_lines = []
    char_index = 0

    for line in base_art.split('\n'):
        colored_line = []

        for char in line:
            # Skip coloring whitespace to avoid visual artifacts
            if char in (' ', '\t'):
                colored_line.append(char)
            else:
                # Calculate color index with offset for animation
                color_idx = (char_index + color_offset) % len(colors)
                color_code = colors[color_idx]

                # Apply ANSI 256-color foreground code
                colored_char = f"\033[38;5;{color_code}m{char}"
                colored_line.append(colored_char)

                char_index += 1

        # Reset color at end of each line
        if colored_line:
            result_lines.append(''.join(colored_line) + "\033[0m")
        else:
            result_lines.append('')

    return '\n'.join(result_lines)
