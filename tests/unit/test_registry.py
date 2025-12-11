"""
Unit tests for the AdapterRegistry.

Tests the basic functionality of adapter registration, retrieval, and discovery.
"""

from typing import Generator, List

import pytest

from mudhound.adapters.base import SearchAdapter
from mudhound.adapters.registry import AdapterRegistry
from mudhound.core.exceptions import AdapterNotFoundError
from mudhound.core.result import SearchOptions, SearchResult


class MockAdapter(SearchAdapter):
    """Mock adapter for testing."""

    @property
    def name(self) -> str:
        return "mock"

    @property
    def display_name(self) -> str:
        return "Mock Adapter"

    def search(self, query: str, options: SearchOptions) -> Generator[SearchResult, None, None]:
        yield SearchResult(
            url="https://example.com",
            title="Test",
            snippet="Test snippet",
            source="example.com",
            rank=1,
            metadata={},
        )

    def validate_options(self, options: SearchOptions) -> List[str]:
        return []


class AnotherMockAdapter(SearchAdapter):
    """Another mock adapter for testing."""

    @property
    def name(self) -> str:
        return "another"

    @property
    def display_name(self) -> str:
        return "Another Mock Adapter"

    def search(self, query: str, options: SearchOptions) -> Generator[SearchResult, None, None]:
        yield SearchResult(
            url="https://example.com",
            title="Test",
            snippet="Test snippet",
            source="example.com",
            rank=1,
            metadata={},
        )

    def validate_options(self, options: SearchOptions) -> List[str]:
        return []


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear the registry before and after each test."""
    AdapterRegistry.clear()
    yield
    AdapterRegistry.clear()


def test_register_adapter():
    """Test registering an adapter."""
    AdapterRegistry.register(MockAdapter)

    # Verify the adapter is registered
    assert "mock" in AdapterRegistry.list_available()


def test_register_multiple_adapters():
    """Test registering multiple adapters."""
    AdapterRegistry.register(MockAdapter)
    AdapterRegistry.register(AnotherMockAdapter)

    # Verify both adapters are registered
    available = AdapterRegistry.list_available()
    assert "mock" in available
    assert "another" in available
    assert len(available) == 2


def test_get_adapter():
    """Test retrieving a registered adapter."""
    AdapterRegistry.register(MockAdapter)

    # Retrieve the adapter
    adapter_class = AdapterRegistry.get("mock")

    # Verify it's the correct class
    assert adapter_class is MockAdapter

    # Verify we can instantiate it
    adapter = adapter_class()
    assert isinstance(adapter, SearchAdapter)
    assert adapter.name == "mock"


def test_get_nonexistent_adapter():
    """Test retrieving a non-existent adapter raises AdapterNotFoundError."""
    with pytest.raises(AdapterNotFoundError) as exc_info:
        AdapterRegistry.get("nonexistent")

    assert "nonexistent" in str(exc_info.value)


def test_list_available_empty():
    """Test listing available adapters when none are registered."""
    available = AdapterRegistry.list_available()
    assert available == []


def test_list_available_with_adapters():
    """Test listing available adapters."""
    AdapterRegistry.register(MockAdapter)
    AdapterRegistry.register(AnotherMockAdapter)

    available = AdapterRegistry.list_available()
    assert len(available) == 2
    assert "mock" in available
    assert "another" in available


def test_register_non_adapter_raises_error():
    """Test that registering a non-SearchAdapter class raises TypeError."""

    class NotAnAdapter:
        pass

    with pytest.raises(TypeError) as exc_info:
        AdapterRegistry.register(NotAnAdapter)

    assert "must be a subclass of SearchAdapter" in str(exc_info.value)


def test_clear_registry():
    """Test clearing the registry."""
    AdapterRegistry.register(MockAdapter)
    AdapterRegistry.register(AnotherMockAdapter)

    # Verify adapters are registered
    assert len(AdapterRegistry.list_available()) == 2

    # Clear the registry
    AdapterRegistry.clear()

    # Verify registry is empty
    assert len(AdapterRegistry.list_available()) == 0


def test_discover_builtin():
    """Test discovering built-in adapters."""
    # This test will discover any actual adapters in the mudhound.adapters package
    AdapterRegistry.discover_builtin()

    # We can't assert specific adapters since they may not exist yet,
    # but we can verify the method runs without error
    available = AdapterRegistry.list_available()
    assert isinstance(available, list)


def test_discover_plugins():
    """Test discovering plugin adapters."""
    # This test verifies the method runs without error
    # In a real environment, it would discover mudhound_adapter_* packages
    AdapterRegistry.discover_plugins()

    available = AdapterRegistry.list_available()
    assert isinstance(available, list)


def test_discover_user_adapters():
    """Test discovering user adapters."""
    # This test verifies the method runs without error
    # In a real environment, it would discover adapters from ~/.mudhound/adapters/
    AdapterRegistry.discover_user_adapters()

    available = AdapterRegistry.list_available()
    assert isinstance(available, list)


def test_discover_all():
    """Test discovering all adapters from all sources."""
    AdapterRegistry.discover_all()

    available = AdapterRegistry.list_available()
    assert isinstance(available, list)
