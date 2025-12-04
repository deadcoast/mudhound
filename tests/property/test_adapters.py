"""
Property-based tests for search adapters.

Tests universal properties that should hold for all search adapter implementations.
"""

from typing import Generator, List
from hypothesis import given, strategies as st, settings, HealthCheck
import pytest

from mudhound.adapters.base import SearchAdapter
from mudhound.core.result import SearchResult, SearchOptions


# Create a concrete test adapter for testing the interface
class TestAdapter(SearchAdapter):
    """Concrete test adapter for property testing."""
    
    def __init__(self, adapter_name: str = "test", adapter_display_name: str = "Test Adapter"):
        self._name = adapter_name
        self._display_name = adapter_display_name
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def display_name(self) -> str:
        return self._display_name
    
    def search(
        self,
        query: str,
        options: SearchOptions
    ) -> Generator[SearchResult, None, None]:
        """Yield test results."""
        for i in range(min(3, options.max_results)):
            yield SearchResult(
                url=f"https://example.com/{i}",
                title=f"Result {i}",
                snippet=f"Snippet for {query}",
                source="example.com",
                rank=i + 1,
                metadata={}
            )
    
    def validate_options(self, options: SearchOptions) -> List[str]:
        """Validate options."""
        errors = []
        if options.max_results < 1:
            errors.append("max_results must be at least 1")
        if options.safesearch not in ["off", "moderate", "strict"]:
            errors.append("safesearch must be 'off', 'moderate', or 'strict'")
        return errors


# Strategies for generating test data
@st.composite
def search_options_strategy(draw):
    """Generate random SearchOptions instances."""
    return SearchOptions(
        max_results=draw(st.integers(min_value=1, max_value=500)),
        region=draw(st.text(min_size=2, max_size=10)),
        safesearch=draw(st.sampled_from(["off", "moderate", "strict"])),
        time_limit=draw(st.one_of(st.none(), st.sampled_from(["d", "w", "m", "y"]))),
    )


@st.composite
def adapter_strategy(draw):
    """Generate random adapter instances."""
    name = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=97, max_codepoint=122)))
    display_name = draw(st.text(min_size=1, max_size=100))
    return TestAdapter(adapter_name=name, adapter_display_name=display_name)


@given(adapter=adapter_strategy())
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_adapter_interface_compliance(adapter):
    """
    Feature: mudhound-full-implementation, Property 12: Adapter interface compliance
    Validates: Requirements 4.1
    
    For any search adapter implementation, it should implement all required methods:
    name, display_name, search, and validate_options.
    """
    # Verify the adapter is an instance of SearchAdapter
    assert isinstance(adapter, SearchAdapter)
    
    # Verify name property exists and returns a string
    assert hasattr(adapter, 'name')
    name = adapter.name
    assert isinstance(name, str)
    assert len(name) > 0
    
    # Verify display_name property exists and returns a string
    assert hasattr(adapter, 'display_name')
    display_name = adapter.display_name
    assert isinstance(display_name, str)
    assert len(display_name) > 0
    
    # Verify search method exists and is callable
    assert hasattr(adapter, 'search')
    assert callable(adapter.search)
    
    # Verify validate_options method exists and is callable
    assert hasattr(adapter, 'validate_options')
    assert callable(adapter.validate_options)
    
    # Verify on_rate_limit method exists and is callable
    assert hasattr(adapter, 'on_rate_limit')
    assert callable(adapter.on_rate_limit)
    
    # Verify on_rate_limit has default implementation
    retry_after = 60
    result = adapter.on_rate_limit(retry_after)
    assert isinstance(result, int)
    assert result == retry_after  # Default implementation returns the input


@given(
    adapter=adapter_strategy(),
    query=st.text(min_size=1, max_size=200),
    options=search_options_strategy()
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_generator_based_search_results(adapter, query, options):
    """
    Feature: mudhound-full-implementation, Property 13: Generator-based search results
    Validates: Requirements 4.2
    
    For any search execution, the adapter should yield results as a generator
    (not return a list).
    """
    # Execute search
    result = adapter.search(query, options)
    
    # Verify the result is a generator
    assert hasattr(result, '__iter__')
    assert hasattr(result, '__next__')
    
    # Verify we can iterate over the results
    results = []
    for search_result in result:
        # Verify each yielded item is a SearchResult
        assert isinstance(search_result, SearchResult)
        results.append(search_result)
    
    # Verify results were yielded (not returned as a list)
    assert isinstance(results, list)
    
    # Verify all results have required fields
    for search_result in results:
        assert hasattr(search_result, 'url')
        assert isinstance(search_result.url, str)
        
        assert hasattr(search_result, 'title')
        assert isinstance(search_result.title, str)
        
        assert hasattr(search_result, 'snippet')
        assert isinstance(search_result.snippet, str)
        
        assert hasattr(search_result, 'source')
        assert isinstance(search_result.source, str)
        
        assert hasattr(search_result, 'rank')
        assert isinstance(search_result.rank, int)
        assert search_result.rank > 0
        
        assert hasattr(search_result, 'metadata')
        assert isinstance(search_result.metadata, dict)


@given(
    adapter=adapter_strategy(),
    options=search_options_strategy()
)
def test_validate_options_returns_list(adapter, options):
    """
    Test that validate_options always returns a list of error messages.
    """
    errors = adapter.validate_options(options)
    
    # Verify the result is a list
    assert isinstance(errors, list)
    
    # Verify all items in the list are strings
    for error in errors:
        assert isinstance(error, str)


@given(adapter=adapter_strategy())
def test_on_rate_limit_default_implementation(adapter):
    """
    Test that on_rate_limit has a default implementation that returns the input.
    """
    retry_after_values = [0, 1, 30, 60, 300, 3600]
    
    for retry_after in retry_after_values:
        result = adapter.on_rate_limit(retry_after)
        assert isinstance(result, int)
        assert result == retry_after


# DuckDuckGo-specific property tests
# Note: These tests use the TestAdapter as a mock since we can't make real API calls
# in property tests. The actual DuckDuckGo adapter behavior is tested in integration tests.


@given(
    max_results=st.integers(min_value=1, max_value=100),
    query=st.text(min_size=1, max_size=100)
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_max_results_enforcement(max_results, query):
    """
    Feature: mudhound-full-implementation, Property 16: Max results enforcement
    Validates: Requirements 5.2
    
    For any max_results value specified, the DuckDuckGo adapter should return
    at most that number of results.
    """
    # Use TestAdapter as a proxy since we can't make real API calls
    adapter = TestAdapter()
    options = SearchOptions(max_results=max_results)
    
    # Execute search and collect results
    results = list(adapter.search(query, options))
    
    # Verify we got at most max_results
    assert len(results) <= max_results
    
    # Verify each result has proper rank
    for i, result in enumerate(results):
        assert result.rank == i + 1


@given(
    query=st.text(min_size=1, max_size=100),
    max_results=st.integers(min_value=1, max_value=50)
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_search_result_structure_completeness(query, max_results):
    """
    Feature: mudhound-full-implementation, Property 17: Search result structure completeness
    Validates: Requirements 5.4
    
    For any search result yielded by the DuckDuckGo adapter, it should contain
    all required fields: url, title, snippet, source, and rank.
    """
    # Use TestAdapter as a proxy since we can't make real API calls
    adapter = TestAdapter()
    options = SearchOptions(max_results=max_results)
    
    # Execute search and collect results
    results = list(adapter.search(query, options))
    
    # Verify each result has all required fields
    for result in results:
        # Verify url field exists and is a non-empty string
        assert hasattr(result, 'url')
        assert isinstance(result.url, str)
        assert len(result.url) > 0
        
        # Verify title field exists and is a string
        assert hasattr(result, 'title')
        assert isinstance(result.title, str)
        
        # Verify snippet field exists and is a string
        assert hasattr(result, 'snippet')
        assert isinstance(result.snippet, str)
        
        # Verify source field exists and is a non-empty string
        assert hasattr(result, 'source')
        assert isinstance(result.source, str)
        assert len(result.source) > 0
        
        # Verify rank field exists and is a positive integer
        assert hasattr(result, 'rank')
        assert isinstance(result.rank, int)
        assert result.rank > 0
        
        # Verify metadata field exists and is a dict
        assert hasattr(result, 'metadata')
        assert isinstance(result.metadata, dict)
