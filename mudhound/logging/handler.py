"""
Styled log handler for MudHound.

This module provides a custom log handler that outputs styled log messages
to the terminal and optionally to files with rotation support.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from mudhound.logging.formatter import StyledLogFormatter


class StyledLogHandler(logging.StreamHandler):
    """Custom log handler with styled output.
    
    Outputs log messages to stderr with level-based styling including
    glyphs and colors.
    
    Attributes:
        formatter: StyledLogFormatter instance
    """
    
    def __init__(self, use_color: bool = True):
        """Initialize the handler.
        
        Args:
            use_color: Whether to apply ANSI color codes
        """
        super().__init__(stream=sys.stderr)
        self.setFormatter(StyledLogFormatter(use_color=use_color))


def setup_file_logging(
    log_file: Path,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> RotatingFileHandler:
    """Set up file logging with rotation support.
    
    Args:
        log_file: Path to log file
        level: Logging level for file handler
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        
    Returns:
        Configured RotatingFileHandler instance
    """
    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create rotating file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    
    # Set level
    file_handler.setLevel(level)
    
    # Use formatter without color for file output
    file_handler.setFormatter(StyledLogFormatter(use_color=False))
    
    return file_handler


def configure_logging(
    level: int = logging.INFO,
    use_color: bool = True,
    log_file: Optional[Path] = None,
    file_level: Optional[int] = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """Configure the MudHound logger.
    
    Args:
        level: Console logging level
        use_color: Whether to use colored output
        log_file: Optional path to log file
        file_level: Logging level for file (defaults to level)
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup files to keep
        
    Returns:
        Configured logger instance
    """
    # Get or create logger
    logger = logging.getLogger("mudhound")
    logger.setLevel(logging.TRACE if hasattr(logging, 'TRACE') else logging.DEBUG)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Add console handler
    console_handler = StyledLogHandler(use_color=use_color)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_file:
        if file_level is None:
            file_level = level
        
        file_handler = setup_file_logging(
            log_file,
            level=file_level,
            max_bytes=max_bytes,
            backup_count=backup_count,
        )
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


__all__ = [
    "StyledLogHandler",
    "setup_file_logging",
    "configure_logging",
]
