"""
Demo script for the error handler component.

Shows various error types and formatting options.
"""

from mudhound.core.exceptions import (
    AnimationError,
    ConfigError,
    ExportError,
    NetworkError,
    RateLimitError,
    ValidationError,
)
from mudhound.ui.components.error import ErrorHandler


def demo_basic_errors():
    """Demonstrate basic error formatting."""
    print("=" * 80)
    print("BASIC ERROR FORMATTING")
    print("=" * 80)
    print()

    handler = ErrorHandler(verbose=False)

    # Config error
    config_err = ConfigError("Invalid TOML syntax in configuration file")
    print(handler.display_error(config_err, width=70))
    print()

    # Network error
    network_err = NetworkError("Connection timeout after 30 seconds")
    print(handler.display_error(network_err, width=70))
    print()

    # Validation error
    validation_err = ValidationError("Input must be between 1 and 100", field="max_results")
    print(handler.display_error(validation_err, width=70))
    print()


def demo_rate_limit_error():
    """Demonstrate RateLimitError with retry_after."""
    print("=" * 80)
    print("RATE LIMIT ERROR WITH RETRY_AFTER")
    print("=" * 80)
    print()

    handler = ErrorHandler(verbose=False)
    error = RateLimitError("Too many requests to search API", retry_after=120.0)
    print(handler.display_error(error, width=70))
    print()


def demo_verbose_mode():
    """Demonstrate verbose mode with stack trace."""
    print("=" * 80)
    print("VERBOSE MODE WITH STACK TRACE")
    print("=" * 80)
    print()

    handler = ErrorHandler(verbose=True)

    try:
        # Create a real exception with stack trace
        raise ExportError("Failed to write to /protected/file.json: Permission denied")
    except ExportError as e:
        print(handler.display_error(e, width=80))
    print()


def demo_all_error_types():
    """Show classification of all error types."""
    print("=" * 80)
    print("ERROR TYPE CLASSIFICATION")
    print("=" * 80)
    print()

    handler = ErrorHandler(verbose=False)

    errors = [
        ConfigError("Config error example"),
        NetworkError("Network error example"),
        RateLimitError("Rate limit error example"),
        ValidationError("Validation error example"),
        ExportError("Export error example"),
        AnimationError("Animation error example"),
    ]

    for error in errors:
        error_type = handler.classify_error(error)
        print(f"{type(error).__name__:25} -> {error_type}")
    print()


if __name__ == "__main__":
    demo_basic_errors()
    demo_rate_limit_error()
    demo_all_error_types()
    demo_verbose_mode()
