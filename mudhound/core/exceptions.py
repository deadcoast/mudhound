"""
MudHound exception hierarchy.

All custom exceptions inherit from MudHoundError base class.
"""

from typing import Optional


class MudHoundError(Exception):
    """Base exception for all MudHound errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ConfigError(MudHoundError):
    """Configuration file parsing, validation, or access errors."""
    pass


class AdapterError(MudHoundError):
    """Base exception for search adapter errors."""
    pass


class AdapterNotFoundError(AdapterError):
    """Raised when a requested adapter is not registered."""

    def __init__(self, adapter_name: str):
        self.adapter_name = adapter_name
        message = f"Adapter '{adapter_name}' not found in registry"
        super().__init__(message)


class RateLimitError(AdapterError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: Optional[float] = None):
        self.retry_after = retry_after
        super().__init__(message)


class NetworkError(AdapterError):
    """Network connectivity or timeout issues."""
    pass


class ValidationError(MudHoundError):
    """Input validation failures."""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        self.message = message
        super().__init__(message)


class ExportError(MudHoundError):
    """Export operation failures (file I/O, format errors)."""
    pass


class AnimationError(MudHoundError):
    """Animation system errors (asset loading, rendering)."""
    pass
