"""
Custom log levels for MudHound.

This module defines custom log levels beyond the standard Python logging levels,
including TRACE and SUCCESS levels.
"""

import logging

# Define custom log levels
TRACE = 5      # Below DEBUG (10)
SUCCESS = 25   # Between INFO (20) and WARNING (30)

# Add custom levels to logging module
logging.addLevelName(TRACE, "TRACE")
logging.addLevelName(SUCCESS, "SUCCESS")


def trace(self, message, *args, **kwargs):
    """Log a message with TRACE level."""
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)


def success(self, message, *args, **kwargs):
    """Log a message with SUCCESS level."""
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)


# Add methods to Logger class
logging.Logger.trace = trace
logging.Logger.success = success


# Level styles mapping: glyph and color per level
LEVEL_STYLES = {
    TRACE: {
        "glyph": "[.]",
        "color": "text_dim",
    },
    logging.DEBUG: {
        "glyph": "[.]",
        "color": "text_dim",
    },
    logging.INFO: {
        "glyph": "[*]",
        "color": "info",
    },
    SUCCESS: {
        "glyph": "[+]",
        "color": "success",
    },
    logging.WARNING: {
        "glyph": "[~]",
        "color": "warning",
    },
    logging.ERROR: {
        "glyph": "[!]",
        "color": "error",
    },
    logging.CRITICAL: {
        "glyph": "[!]",
        "color": "error",
    },
}


def get_level_style(level: int) -> dict:
    """Get the style (glyph and color) for a log level.
    
    Args:
        level: Logging level (e.g., logging.INFO, SUCCESS)
        
    Returns:
        Dictionary with 'glyph' and 'color' keys
    """
    return LEVEL_STYLES.get(level, {"glyph": "[?]", "color": "text"})


__all__ = [
    "TRACE",
    "SUCCESS",
    "LEVEL_STYLES",
    "get_level_style",
]
