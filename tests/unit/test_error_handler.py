"""
Unit tests for error handler component.

Tests basic error display functionality.
"""

from mudhound.core.exceptions import (
    ConfigError,
    NetworkError,
    RateLimitError,
    ValidationError,
)
from mudhound.ui.components.error import ErrorHandler


def test_error_handler_basic_formatting():
    """Test basic error formatting."""
    error = ConfigError("Invalid configuration file")
    handler = ErrorHandler(verbose=False)

    formatted = handler.format_error(error)

    assert "Configuration Error" in formatted
    assert "Invalid configuration file" in formatted
    assert "✗" in formatted  # Cross glyph


def test_error_handler_with_suggestions():
    """Test that suggestions are included for known error types."""
    error = NetworkError("Connection timeout")
    handler = ErrorHandler(verbose=False)

    formatted = handler.format_error(error)

    assert "Network Error" in formatted
    assert "Connection timeout" in formatted
    assert "Suggestions:" in formatted
    assert "internet connection" in formatted.lower()


def test_error_handler_rate_limit_special_handling():
    """Test special handling for RateLimitError with retry_after."""
    error = RateLimitError("Too many requests", retry_after=60.0)
    handler = ErrorHandler(verbose=False)

    formatted = handler.format_error(error)

    assert "Rate Limit" in formatted
    assert "Too many requests" in formatted
    assert "Retry after" in formatted
    assert "60" in formatted


def test_error_handler_verbose_mode():
    """Test that verbose mode includes stack trace."""
    error = ValidationError("Invalid input")
    handler_verbose = ErrorHandler(verbose=True)
    handler_normal = ErrorHandler(verbose=False)

    formatted_verbose = handler_verbose.format_error(error)
    formatted_normal = handler_normal.format_error(error)

    assert "Stack trace" in formatted_verbose
    assert "Stack trace" not in formatted_normal
    assert len(formatted_verbose) > len(formatted_normal)


def test_error_handler_display_with_frame():
    """Test that display_error creates a framed output."""
    error = ConfigError("Test error")
    handler = ErrorHandler(verbose=False)

    framed = handler.display_error(error, width=60)

    # Should contain frame borders
    assert "┌" in framed or "╔" in framed or "+" in framed
    assert "Configuration Error" in framed
    assert "Test error" in framed


def test_error_classification_inheritance():
    """Test that error classification works with inheritance."""
    # RateLimitError inherits from AdapterError
    error = RateLimitError("Test")
    handler = ErrorHandler()

    # Should classify as RateLimitError, not generic AdapterError
    error_type = handler.classify_error(error)
    assert error_type == "Rate Limit Exceeded"


def test_suggestions_for_all_error_types():
    """Test that all major error types have suggestions."""
    handler = ErrorHandler()

    error_types = [
        ConfigError("test"),
        NetworkError("test"),
        ValidationError("test"),
    ]

    for error in error_types:
        suggestions = handler.get_suggestions(error)
        assert len(suggestions) > 0, f"No suggestions for {type(error).__name__}"
