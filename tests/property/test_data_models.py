"""
Property-based tests for data models.

Tests universal properties that should hold for all data model instances.
"""

from datetime import datetime, timedelta

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from mudhound.core.result import (
    SearchOptions,
    SearchQuery,
    SearchResult,
    SearchSession,
    SearchStatus,
)


# Strategies for generating test data
@st.composite
def search_result_strategy(draw):
    """Generate random SearchResult instances."""
    return SearchResult(
        url=draw(st.text(min_size=10, max_size=200)),
        title=draw(st.text(min_size=1, max_size=100)),
        snippet=draw(st.text(min_size=1, max_size=500)),
        source=draw(st.text(min_size=1, max_size=50)),
        rank=draw(st.integers(min_value=1, max_value=1000)),
        metadata=draw(st.dictionaries(
            st.text(min_size=1, max_size=20), st.text(max_size=100))),
    )


@st.composite
def search_options_strategy(draw):
    """Generate random SearchOptions instances."""
    return SearchOptions(
        max_results=draw(st.integers(min_value=1, max_value=500)),
        region=draw(st.text(min_size=2, max_size=10)),
        safesearch=draw(st.sampled_from(["off", "moderate", "strict"])),
        time_limit=draw(
            st.one_of(st.none(), st.sampled_from(["d", "w", "m", "y"]))),
    )


@st.composite
def search_query_strategy(draw):
    """Generate random SearchQuery instances."""
    return SearchQuery(
        id=draw(st.text(min_size=1, max_size=50)),
        query=draw(st.text(min_size=1, max_size=200)),
        engine=draw(st.text(min_size=1, max_size=50)),
        options=draw(search_options_strategy()),
        created_at=draw(
            st.datetimes(min_value=datetime(2020, 1, 1),
                         max_value=datetime(2030, 12, 31))
        ),
        status=draw(st.sampled_from(SearchStatus)),
    )


@st.composite
def search_session_strategy(draw):
    """Generate random SearchSession instances."""
    query = draw(search_query_strategy())
    results = draw(st.lists(search_result_strategy(),
                   min_size=0, max_size=100))
    started_at = draw(
        st.datetimes(min_value=datetime(2020, 1, 1),
                     max_value=datetime(2030, 12, 31))
    )

    # completed_at should be after started_at if present
    has_completed = draw(st.booleans())
    if has_completed:
        # Add a random duration between 0 and 3600 seconds
        duration_seconds = draw(st.floats(min_value=0, max_value=3600))
        completed_at = started_at + timedelta(seconds=duration_seconds)
    else:
        completed_at = None

    error = draw(st.one_of(st.none(), st.text(min_size=1, max_size=200)))

    return SearchSession(
        query=query,
        results=results,
        started_at=started_at,
        completed_at=completed_at,
        error=error,
    )


@given(session=search_session_strategy())
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_session_data_completeness(session):
    """
    Feature: mudhound-full-implementation, Property 26: Session data completeness
    Validates: Requirements 8.2

    For any stored search session, it should contain all required fields:
    query, results, timestamps, status, and error (if applicable).
    """
    # Verify all required fields are present and have valid types
    assert session.query is not None
    assert isinstance(session.query, SearchQuery)

    assert session.results is not None
    assert isinstance(session.results, list)
    assert all(isinstance(r, SearchResult) for r in session.results)

    assert session.started_at is not None
    assert isinstance(session.started_at, datetime)

    # completed_at can be None (for running searches) or a datetime
    assert session.completed_at is None or isinstance(
        session.completed_at, datetime)

    # error can be None (for successful searches) or a string
    assert session.error is None or isinstance(session.error, str)

    # Verify query contains all required fields
    assert session.query.id is not None
    assert isinstance(session.query.id, str)

    assert session.query.query is not None
    assert isinstance(session.query.query, str)

    assert session.query.engine is not None
    assert isinstance(session.query.engine, str)

    assert session.query.options is not None
    assert isinstance(session.query.options, SearchOptions)

    assert session.query.created_at is not None
    assert isinstance(session.query.created_at, datetime)

    assert session.query.status is not None
    assert isinstance(session.query.status, SearchStatus)

    # Verify result_count property works correctly
    assert session.result_count == len(session.results)
    assert isinstance(session.result_count, int)
    assert session.result_count >= 0

    # Verify duration property works correctly
    if session.completed_at is not None:
        assert session.duration is not None
        assert isinstance(session.duration, float)
        assert session.duration >= 0
        # Verify duration calculation is correct
        expected_duration = (session.completed_at -
                             session.started_at).total_seconds()
        assert (
            abs(session.duration - expected_duration) < 0.001
        )  # Allow for floating point precision
    else:
        assert session.duration is None


@given(session=search_session_strategy())
def test_session_result_count_property(session):
    """
    Test that result_count property always matches the length of results list.
    """
    assert session.result_count == len(session.results)


@given(session=search_session_strategy())
def test_session_duration_property(session):
    """
    Test that duration property correctly calculates time difference.
    """
    if session.completed_at is not None:
        # Duration should be non-negative
        assert session.duration >= 0

        # Duration should match manual calculation
        expected = (session.completed_at - session.started_at).total_seconds()
        assert abs(session.duration - expected) < 0.001
    else:
        # Duration should be None for incomplete sessions
        assert session.duration is None
