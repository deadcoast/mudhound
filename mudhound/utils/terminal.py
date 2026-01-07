"""Terminal utility functions for size detection and management."""

import shutil
from typing import Tuple


def get_terminal_size() -> Tuple[int, int]:
    """
    Get the current terminal size.

    Returns:
        Tuple[int, int]: (columns, rows) of the terminal
    """
    size = shutil.get_terminal_size(fallback=(80, 24))
    return (size.columns, size.lines)


def is_terminal_size_adequate(min_width: int = 60, min_height: int = 10) -> bool:
    """
    Check if terminal meets minimum size requirements.

    Args:
        min_width: Minimum required width in columns
        min_height: Minimum required height in rows

    Returns:
        bool: True if terminal meets minimum requirements
    """
    width, height = get_terminal_size()
    return width >= min_width and height >= min_height
