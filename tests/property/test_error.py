"""
Property-based tests for error handling.

Tests error message formatting and classification.
"""

import pytest
from hypothesis import given
from hypothesis import strategies as st

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
from mudhound.ui.components.error import ErrorHandler
from mudhound.ui.glyphs import GLYPHS

# Strategy for generating error messages
error_messages = st.text(min_size=1, max_size=200)

# Strategy for generating retry_after values
retry_after_values = st.floats(min_value=0.1, max_value=3600.0)


@given(message=error_messages)
def test_property_57_error_message_formatting(message):
    """
    Feature: mudhound-full-implementation, Property 57: Error message formatting

    For any error that occurs, the error handler should display a formatted
    message with error type and description.

    Validates: Requirements 18.1
    """
    # Create an error
    error = MudHoundError(message)

    # Create error handler
    handler = ErrorHandler(verbose=False)

    # Format the error
    formatted = handler.format_error(error)

    # Verify formatted message contains error type
    error_type = handler.classify_error(error)
    assert error_type in formatted, f"Error type '{error_type}' not found in formatted message"

    # Verify formatted message contains the error message
    assert message in formatted, f"Error message '{message}' not found in formatted output"

    # Verify formatted message contains error glyph
    error_glyph = GLYPHS["decorative"]["cross"]
    assert error_glyph in formatted, f"Error glyph '{error_glyph}' not found in formatted message"


@given(message=error_messages)
def test_property_57_config_error_formatting(message):
    """
    Feature: mudhound-full-implementation, Property 57: Error message formatting

    Test formatting for ConfigError specifically.

    Validates: Requirements 18.1
    """
    error = ConfigError(message)
    handler = ErrorHandler(verbose=False)
    formatted = handler.format_error(error)

    # Should contain error type
    assert "Configuration Error" in formatted
    # Should contain message
    assert message in formatted
    # Should contain glyph
    assert GLYPHS["decorative"]["cross"] in formatted


@given(message=error_messages)
def test_property_57_network_error_formatting(message):
    """
    Feature: mudhound-full-implementation, Property 57: Error message formatting

    Test formatting for NetworkError specifically.

    Validates: Requirements 18.1
    """
    error = NetworkError(message)
    handler = ErrorHandler(verbose=False)
    formatted = handler.format_error(error)

    # Should contain error type
    assert "Network Error" in formatted
    # Should contain message
    assert message in formatted


@given(message=error_messages, retry_after=retry_after_values)
def test_property_57_rate_limit_error_formatting(message, retry_after):
    """
    Feature: mudhound-full-implementation, Property 57: Error message formatting

    Test formatting for RateLimitError with retry_after display.

    Validates: Requirements 18.1, 18.5
    """
    error = RateLimitError(message, retry_after=retry_after)
    handler = ErrorHandler(verbose=False)
    formatted = handler.format_error(error)

    # Should contain error type
    assert "Rate Limit" in formatted
    # Should contain message
    assert message in formatted
    # Should contain retry_after information
    assert "Retry after" in formatted
    assert str(retry_after) in formatted or f"{retry_after:.1f}" in formatted


@given(message=error_messages)
def test_property_60_error_type_classification_config(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    For any error, the error handler should correctly classify it as the
    appropriate error type.

    Validates: Requirements 18.4
    """
    error = ConfigError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Configuration Error"


@given(message=error_messages)
def test_property_60_error_type_classification_adapter_not_found(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for AdapterNotFoundError.

    Validates: Requirements 18.4
    """
    # AdapterNotFoundError has specific constructor
    error = AdapterNotFoundError("test_adapter")
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Adapter Not Found"


@given(message=error_messages)
def test_property_60_error_type_classification_rate_limit(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for RateLimitError.

    Validates: Requirements 18.4
    """
    error = RateLimitError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Rate Limit Exceeded"


@given(message=error_messages)
def test_property_60_error_type_classification_network(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for NetworkError.

    Validates: Requirements 18.4
    """
    error = NetworkError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Network Error"


@given(message=error_messages)
def test_property_60_error_type_classification_validation(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for ValidationError.

    Validates: Requirements 18.4
    """
    error = ValidationError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Validation Error"


@given(message=error_messages)
def test_property_60_error_type_classification_export(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for ExportError.

    Validates: Requirements 18.4
    """
    error = ExportError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Export Error"


@given(message=error_messages)
def test_property_60_error_type_classification_animation(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for AnimationError.

    Validates: Requirements 18.4
    """
    error = AnimationError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Animation Error"


@given(message=error_messages)
def test_property_60_error_type_classification_adapter(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for generic AdapterError.

    Validates: Requirements 18.4
    """
    error = AdapterError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "Adapter Error"


@given(message=error_messages)
def test_property_60_error_type_classification_mudhound(message):
    """
    Feature: mudhound-full-implementation, Property 60: Error type classification

    Test classification for generic MudHoundError.

    Validates: Requirements 18.4
    """
    error = MudHoundError(message)
    handler = ErrorHandler()

    error_type = handler.classify_error(error)

    assert error_type == "MudHound Error"


# Additional tests for suggestions and verbose mode


@given(message=error_messages)
def test_error_suggestions_provided(message):
    """
    Test that suggestions are provided for common error types.

    Validates: Requirements 18.2
    """
    error = NetworkError(message)
    handler = ErrorHandler()

    suggestions = handler.get_suggestions(error)

    # NetworkError should have suggestions
    assert len(suggestions) > 0
    assert any("internet connection" in s.lower() for s in suggestions)


@given(message=error_messages)
def test_verbose_mode_includes_stack_trace(message):
    """
    Test that verbose mode includes stack trace information.

    Validates: Requirements 18.3
    """
    error = ConfigError(message)
    handler_verbose = ErrorHandler(verbose=True)
    handler_normal = ErrorHandler(verbose=False)

    formatted_verbose = handler_verbose.format_error(error)
    formatted_normal = handler_normal.format_error(error)

    # Verbose should include stack trace
    assert "Stack trace" in formatted_verbose
    # Normal should not
    assert "Stack trace" not in formatted_normal
    # Verbose should be longer
    assert len(formatted_verbose) > len(formatted_normal)
