"""
Status component for displaying log messages in the terminal.

This module provides the StatusComponent class for displaying styled
status messages with timestamps and level-appropriate glyphs.
"""

import logging
from datetime import datetime
from typing import Optional

from mudhound.logging.levels import SUCCESS, TRACE, get_level_style
from mudhound.ui.theme import get_theme_engine


class StatusComponent:
    """Component for displaying status messages.

    Displays log messages with:
    - Timestamp
    - Level-appropriate glyph
    - Colored level name
    - Message text

    Attributes:
        use_color: Whether to apply color codes
        show_timestamp: Whether to show timestamps
        datefmt: Date format string for timestamps
    """

    def __init__(
        self,
        use_color: bool = True,
        show_timestamp: bool = True,
        datefmt: str = "%Y-%m-%d %H:%M:%S",
    ):
        """Initialize the StatusComponent.

        Args:
            use_color: Whether to apply ANSI color codes
            show_timestamp: Whether to display timestamps
            datefmt: Date format string for timestamps
        """
        self.use_color = use_color
        self.show_timestamp = show_timestamp
        self.datefmt = datefmt

    def format_message(
        self,
        message: str,
        level: int = logging.INFO,
        timestamp: Optional[datetime] = None,
    ) -> str:
        """Format a status message.

        Args:
            message: Message text
            level: Logging level (e.g., logging.INFO, SUCCESS)
            timestamp: Optional timestamp (defaults to current time)

        Returns:
            Formatted status message string
        """
        # Get level style (glyph and color)
        style = get_level_style(level)
        glyph = style["glyph"]
        color_name = style["color"]

        # Format timestamp
        if timestamp is None:
            timestamp = datetime.now()

        timestamp_str = timestamp.strftime(self.datefmt)

        # Get level name
        level_name = logging.getLevelName(level)

        # Apply color if enabled
        if self.use_color:
            theme_engine = get_theme_engine()
            glyph = theme_engine.apply(glyph, color_name)
            level_name = theme_engine.apply(level_name, color_name)

        # Construct status line
        if self.show_timestamp:
            status_line = f"{timestamp_str} {glyph} {level_name}: {message}"
        else:
            status_line = f"{glyph} {level_name}: {message}"

        return status_line

    def display(
        self,
        message: str,
        level: int = logging.INFO,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Display a status message.

        Args:
            message: Message text
            level: Logging level
            timestamp: Optional timestamp
        """
        formatted = self.format_message(message, level, timestamp)
        print(formatted)

    def success(self, message: str, timestamp: Optional[datetime] = None) -> None:
        """Display a success message.

        Args:
            message: Message text
            timestamp: Optional timestamp
        """
        self.display(message, SUCCESS, timestamp)

    def info(self, message: str, timestamp: Optional[datetime] = None) -> None:
        """Display an info message.

        Args:
            message: Message text
            timestamp: Optional timestamp
        """
        self.display(message, logging.INFO, timestamp)

    def warning(self, message: str, timestamp: Optional[datetime] = None) -> None:
        """Display a warning message.

        Args:
            message: Message text
            timestamp: Optional timestamp
        """
        self.display(message, logging.WARNING, timestamp)

    def error(self, message: str, timestamp: Optional[datetime] = None) -> None:
        """Display an error message.

        Args:
            message: Message text
            timestamp: Optional timestamp
        """
        self.display(message, logging.ERROR, timestamp)

    def debug(self, message: str, timestamp: Optional[datetime] = None) -> None:
        """Display a debug message.

        Args:
            message: Message text
            timestamp: Optional timestamp
        """
        self.display(message, logging.DEBUG, timestamp)

    def trace(self, message: str, timestamp: Optional[datetime] = None) -> None:
        """Display a trace message.

        Args:
            message: Message text
            timestamp: Optional timestamp
        """
        self.display(message, TRACE, timestamp)


__all__ = ["StatusComponent"]
