"""
Log formatter with level-based formatting for MudHound.

This module provides a custom log formatter that applies glyphs and colors
based on log level.
"""

import logging
from datetime import datetime
from typing import Optional

from mudhound.logging.levels import get_level_style
from mudhound.ui.theme import get_theme_engine


class StyledLogFormatter(logging.Formatter):
    """Custom log formatter with level-based styling.
    
    Formats log messages with:
    - Timestamp
    - Level-appropriate glyph
    - Colored level name
    - Message
    
    Attributes:
        use_color: Whether to apply color codes
        datefmt: Date format string for timestamps
    """
    
    def __init__(
        self,
        use_color: bool = True,
        datefmt: Optional[str] = None,
    ):
        """Initialize the formatter.
        
        Args:
            use_color: Whether to apply ANSI color codes
            datefmt: Date format string (defaults to "%Y-%m-%d %H:%M:%S")
        """
        self.use_color = use_color
        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"
        
        super().__init__(datefmt=datefmt)
    
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record.
        
        Args:
            record: Log record to format
            
        Returns:
            Formatted log message string
        """
        # Get level style (glyph and color)
        style = get_level_style(record.levelno)
        glyph = style["glyph"]
        color_name = style["color"]
        
        # Format timestamp
        timestamp = self.formatTime(record, self.datefmt)
        
        # Format level name
        level_name = record.levelname
        
        # Apply color if enabled
        if self.use_color:
            theme_engine = get_theme_engine()
            glyph = theme_engine.apply(glyph, color_name)
            level_name = theme_engine.apply(level_name, color_name)
        
        # Format the message
        message = record.getMessage()
        
        # Construct final log line
        log_line = f"{timestamp} {glyph} {level_name}: {message}"
        
        # Add exception info if present
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        
        if record.exc_text:
            if log_line[-1:] != "\n":
                log_line = log_line + "\n"
            log_line = log_line + record.exc_text
        
        if record.stack_info:
            if log_line[-1:] != "\n":
                log_line = log_line + "\n"
            log_line = log_line + self.formatStack(record.stack_info)
        
        return log_line
    
    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        """Format the timestamp for a log record.
        
        Args:
            record: Log record
            datefmt: Date format string
            
        Returns:
            Formatted timestamp string
        """
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S")
        return s


__all__ = ["StyledLogFormatter"]
