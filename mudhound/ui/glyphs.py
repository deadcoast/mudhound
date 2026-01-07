"""
Glyph registry for MudHound terminal UI.

This module defines all text-based symbols (glyphs) used throughout the application
for status indicators, progress displays, selection markers, decorative elements,
and data flow visualization.
"""

from typing import Dict, List, Union

# Type alias for glyph values (can be str or list of str)
GlyphValue = Union[str, List[str]]
GlyphCategory = Dict[str, GlyphValue]

# Main glyph registry dictionary
GLYPHS: Dict[str, GlyphCategory] = {
    # Status indicators - used for log messages and status displays
    "status": {
        "success": "[+]",  # Successful operation
        "error": "[!]",  # Error condition
        "warning": "[~]",  # Warning message
        "info": "[*]",  # Informational message
        "debug": "[.]",  # Debug message
        "question": "[?]",  # Question or prompt
    },
    # Progress glyphs - used for progress indicators and animations
    "progress": {
        "spinner": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],  # Braille spinner frames
        "blocks": ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"],  # Progress blocks
        "bullet": "•",  # Bullet point
        "arrow": "→",  # Arrow indicator
        "pointer": "▶",  # Pointer/play symbol
    },
    # Selection glyphs - used for menus and interactive selections
    "selection": {
        "checked": "[x]",  # Checked checkbox
        "unchecked": "[ ]",  # Unchecked checkbox
        "radio_selected": "(*)",  # Selected radio button
        "radio_unselected": "( )",  # Unselected radio button
        "cursor": ">>>",  # Menu cursor indicator
    },
    # Decorative glyphs - used for visual separation and feedback
    "decorative": {
        "divider": "─",  # Horizontal divider line
        "ellipsis": "…",  # Ellipsis for truncation
        "check": "✓",  # Checkmark
        "cross": "✗",  # Cross/X mark
        "dot": "·",  # Middle dot
    },
    # Data flow glyphs - used for showing data movement and operations
    "dataflow": {
        "input": "←",  # Input indicator
        "output": "→",  # Output indicator
        "pipe": "│",  # Pipe/vertical connector
        "chain": "⇒",  # Chain/sequence indicator
    },
}


def get_glyph(category: str, name: str) -> str:
    """
    Retrieve a glyph from the registry.

    Args:
        category: The glyph category (e.g., "status", "progress")
        name: The specific glyph name within the category

    Returns:
        The glyph string, or a fallback character if not found

    Examples:
        >>> get_glyph("status", "success")
        '[+]'
        >>> get_glyph("progress", "bullet")
        '•'
    """
    try:
        value = GLYPHS[category][name]
        # Most glyphs are strings; spinner/blocks are lists (handled by other functions)
        return str(value) if isinstance(value, str) else "?"
    except KeyError:
        # Fallback to a generic indicator if glyph not found
        return "?"


def get_spinner_frame(frame_index: int) -> str:
    """
    Get a specific frame from the spinner animation.

    Args:
        frame_index: The frame number (will wrap around if out of bounds)

    Returns:
        The spinner character for the given frame

    Examples:
        >>> get_spinner_frame(0)
        '⠋'
        >>> get_spinner_frame(5)
        '⠴'
    """
    spinner = GLYPHS["progress"]["spinner"]
    if isinstance(spinner, list):
        return spinner[frame_index % len(spinner)]
    return "?"


def get_progress_block(level: int) -> str:
    """
    Get a progress block character for a given fill level.

    Args:
        level: Fill level from 0-7 (0 = empty, 7 = full)

    Returns:
        The appropriate progress block character

    Examples:
        >>> get_progress_block(0)
        '▏'
        >>> get_progress_block(7)
        '█'
    """
    blocks = GLYPHS["progress"]["blocks"]
    # Clamp level to valid range
    level = max(0, min(7, level))
    if isinstance(blocks, list):
        return blocks[level]
    return "?"


__all__ = [
    "GLYPHS",
    "get_glyph",
    "get_spinner_frame",
    "get_progress_block",
]
