"""
Error display component for formatted error messages.

Provides error type classification, suggestions, and verbose mode support.
"""

import traceback
from typing import Dict, List, Optional

from mudhound.core.exceptions import (
    AdapterError,
    AdapterNotFoundError,
    AnimationError,
    ConfigError,
    ExportError,
    MudHoundError,
    NetworkError,
    RateLimitError,
    ValidationError,
)
from mudhound.ui.frames import BorderStyle, FrameRenderer
from mudhound.ui.glyphs import get_glyph
from mudhound.ui.theme import Theme


class ErrorHandler:
    """
    Handles error display formatting with classification and suggestions.

    Provides:
    - Error type classification
    - Formatted error messages with frames
    - Contextual suggestions for common errors
    - Verbose mode with stack traces
    - Special handling for RateLimitError
    """

    # Error type to display name mapping
    ERROR_TYPES: Dict[type, str] = {
        ConfigError: "Configuration Error",
        AdapterNotFoundError: "Adapter Not Found",
        RateLimitError: "Rate Limit Exceeded",
        NetworkError: "Network Error",
        ValidationError: "Validation Error",
        ExportError: "Export Error",
        AnimationError: "Animation Error",
        AdapterError: "Adapter Error",
        MudHoundError: "MudHound Error",
    }

    # Common error suggestions
    SUGGESTIONS: Dict[type, List[str]] = {
        ConfigError: [
            "Check that your configuration file is valid TOML format",
            "Verify all required configuration keys are present",
            "Try running 'mh config list' to see current configuration",
        ],
        AdapterNotFoundError: [
            "Check available adapters with 'mh adapters list'",
            "Verify the adapter name is spelled correctly",
            "Ensure the adapter plugin is installed",
        ],
        RateLimitError: [
            "Wait for the specified duration before retrying",
            "Consider reducing max_results to stay under rate limits",
            "Try using a different search engine adapter",
        ],
        NetworkError: [
            "Check your internet connection",
            "Verify firewall settings allow outbound connections",
            "Try again in a few moments",
        ],
        ValidationError: [
            "Check that your input matches the expected format",
            "Review the validation error message for specific requirements",
        ],
        ExportError: [
            "Verify you have write permissions for the output directory",
            "Check that sufficient disk space is available",
            "Ensure the output path is valid",
        ],
        AnimationError: [
            "Try disabling animations with --no-animation flag",
            "Check that asset files are present in the assets directory",
        ],
    }

    def __init__(self, theme: Optional[Theme] = None, verbose: bool = False):
        """
        Initialize error handler.

        Args:
            theme: Theme for color styling (optional)
            verbose: Enable verbose mode with stack traces
        """
        # Create a minimal default theme if none provided
        if theme is None:
            default_colors = {
                "error": "bright_red",
                "warning": "bright_yellow",
                "info": "bright_blue",
                "success": "bright_green",
            }
            theme = Theme(name="default", colors=default_colors)

        self.theme = theme
        self.verbose = verbose

    def classify_error(self, error: Exception) -> str:
        """
        Classify error type and return display name.

        Args:
            error: Exception to classify

        Returns:
            Human-readable error type name
        """
        # Check for exact type match first
        error_type = type(error)
        if error_type in self.ERROR_TYPES:
            return self.ERROR_TYPES[error_type]

        # Check for inheritance (most specific first)
        for exc_type in [
            AdapterNotFoundError,
            RateLimitError,
            NetworkError,
            ValidationError,
            ExportError,
            AnimationError,
            ConfigError,
            AdapterError,
            MudHoundError,
        ]:
            if isinstance(error, exc_type):
                return self.ERROR_TYPES[exc_type]

        # Fallback for unknown errors
        return "Error"

    def get_suggestions(self, error: Exception) -> List[str]:
        """
        Get contextual suggestions for error resolution.

        Args:
            error: Exception to get suggestions for

        Returns:
            List of suggestion strings
        """
        # Check for exact type match first
        error_type = type(error)
        if error_type in self.SUGGESTIONS:
            return self.SUGGESTIONS[error_type]

        # Check for inheritance
        for exc_type, suggestions in self.SUGGESTIONS.items():
            if isinstance(error, exc_type):
                return suggestions

        # No specific suggestions
        return []

    def format_error(self, error: Exception) -> str:
        """
        Format error message with type, description, and suggestions.

        Args:
            error: Exception to format

        Returns:
            Formatted error message string
        """
        lines = []

        # Error type and glyph
        error_type = self.classify_error(error)
        error_glyph = get_glyph("decorative", "cross")

        # Apply error color from theme
        error_color = self.theme.get_color("error")

        # Header with error type
        lines.append(f"{error_color}{error_glyph} {error_type}\033[0m")
        lines.append("")

        # Error message
        error_message = str(error)
        lines.append(f"  {error_message}")
        lines.append("")

        # Special handling for RateLimitError
        if isinstance(error, RateLimitError) and error.retry_after:
            lines.append(f"  Retry after: {error.retry_after} seconds")
            lines.append("")

        # Suggestions
        suggestions = self.get_suggestions(error)
        if suggestions:
            lines.append("  Suggestions:")
            for suggestion in suggestions:
                lines.append(f"    • {suggestion}")
            lines.append("")

        # Verbose mode: stack trace
        if self.verbose:
            lines.append("  Stack trace:")
            tb_lines = traceback.format_exception(type(error), error, error.__traceback__)
            for tb_line in tb_lines:
                for line in tb_line.rstrip().split("\n"):
                    lines.append(f"    {line}")
            lines.append("")

        return "\n".join(lines)

    def display_error(self, error: Exception, width: Optional[int] = None) -> str:
        """
        Display error in a framed box.

        Args:
            error: Exception to display
            width: Frame width (optional, auto-calculated if not provided)

        Returns:
            Framed error message string
        """
        error_message = self.format_error(error)

        # Calculate width if not provided
        if width is None:
            lines = error_message.split("\n")
            # Strip ANSI codes for width calculation
            import re

            ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
            max_line_length = max(len(ansi_escape.sub("", line)) for line in lines if line)
            width = min(max_line_length + 4, 80)  # Add padding, cap at 80

        # Render in frame
        error_type = self.classify_error(error)
        renderer = FrameRenderer(style=BorderStyle.SINGLE, width=width)

        # Split error message into lines
        content_lines = error_message.split("\n")

        # Build frame
        frame_lines = []
        frame_lines.append(renderer.top_border(title=error_type))
        frame_lines.extend(renderer.content_rows(content_lines))
        frame_lines.append(renderer.bottom_border())

        return "\n".join(frame_lines)
