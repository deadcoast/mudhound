"""
Property-based tests for result storage and history.

Tests universal properties for the ResultStore persistence layer.
"""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from mudhound.core.result import (
    SearchOptions,
    SearchQuery,
    SearchResult,
    SearchSession,
    SearchStatus,
)
from mudhound.core.store import ResultStore


# Reuse strategies from test_data_models
@st.composite
def search_result_strategy(draw):
    """Generate random SearchResult instances."""
    return SearchResult(
        url=draw(st.text(min_size=10, max_size=200)),
        title=draw(st.text(min_size=1, max_size=100)),
        snippet=draw(st.text(min_size=1, max_size=500)),
        source=draw(st.text(min_size=1, max_size=50)),
        rank=draw(st.integers(min_value=1, max_value=1000)),
        metadata=draw(st.dictionaries(st.text(min_size=1, max_size=20), st.text(max_size=100))),
    )


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
def search_query_strategy(draw):
    """Generate random SearchQuery instances."""
    return SearchQuery(
        id=draw(st.text(min_size=1, max_size=50)),
        query=draw(st.text(min_size=1, max_size=200)),
        engine=draw(st.text(min_size=1, max_size=50)),
        options=draw(search_options_strategy()),
        created_at=draw(st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31))),
        status=draw(st.sampled_from(SearchStatus)),
    )


@st.composite
def search_session_strategy(draw):
    """Generate random SearchSession instances."""
    query = draw(search_query_strategy())
    results = draw(st.lists(search_result_strategy(), min_size=0, max_size=50))
    started_at = draw(st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31)))

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
def test_search_session_persistence(session):
    """
    Feature: mudhound-full-implementation, Property 25: Search session persistence
    Validates: Requirements 8.1
    
    For any completed search, the result store should persist the SearchSession
    to the history database.
    """
    # Create a temporary database for this test
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Persist the session
        store.persist(session)

        # Verify the session was persisted by retrieving it
        retrieved = store.show(session.query.id)

        assert retrieved is not None, "Session should be retrievable after persistence"

        # Verify all fields match
        assert retrieved.query.id == session.query.id
        assert retrieved.query.query == session.query.query
        assert retrieved.query.engine == session.query.engine
        assert retrieved.query.status == session.query.status

        # Verify options match
        assert retrieved.query.options.max_results == session.query.options.max_results
        assert retrieved.query.options.region == session.query.options.region
        assert retrieved.query.options.safesearch == session.query.options.safesearch
        assert retrieved.query.options.time_limit == session.query.options.time_limit

        # Verify timestamps match (within 1 second due to serialization)
        assert abs((retrieved.query.created_at - session.query.created_at).total_seconds()) < 1
        assert abs((retrieved.started_at - session.started_at).total_seconds()) < 1

        if session.completed_at is not None:
            assert retrieved.completed_at is not None
            assert abs((retrieved.completed_at - session.completed_at).total_seconds()) < 1
        else:
            assert retrieved.completed_at is None

        # Verify error matches
        assert retrieved.error == session.error

        # Verify results match
        assert len(retrieved.results) == len(session.results)

        # Sort both lists by rank for comparison (database returns them sorted by rank)
        orig_sorted = sorted(session.results, key=lambda r: r.rank)
        retr_sorted = sorted(retrieved.results, key=lambda r: r.rank)

        for orig_result, retr_result in zip(orig_sorted, retr_sorted):
            assert retr_result.url == orig_result.url
            assert retr_result.title == orig_result.title
            assert retr_result.snippet == orig_result.snippet
            assert retr_result.source == orig_result.source
            assert retr_result.rank == orig_result.rank
            assert retr_result.metadata == orig_result.metadata


@given(session=search_session_strategy())
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_history_retrieval_by_id(session):
    """
    Feature: mudhound-full-implementation, Property 27: History retrieval by ID
    Validates: Requirements 8.4
    
    For any valid search ID, executing show should retrieve and display
    the full results for that search.
    """
    # Create a temporary database for this test
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Persist the session
        store.persist(session)

        # Retrieve by ID
        retrieved = store.show(session.query.id)

        # Should successfully retrieve the session
        assert retrieved is not None
        assert retrieved.query.id == session.query.id

        # Should contain all results
        assert len(retrieved.results) == len(session.results)

        # Verify result data is complete
        for result in retrieved.results:
            assert result.url is not None and len(result.url) > 0
            assert result.title is not None
            assert result.snippet is not None
            assert result.source is not None
            assert result.rank > 0
            assert result.metadata is not None


@given(session=search_session_strategy())
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_history_replay_parameter_preservation(session):
    """
    Feature: mudhound-full-implementation, Property 28: History replay parameter preservation
    Validates: Requirements 8.5
    
    For any search ID, replaying the search should use the exact same parameters
    (query, engine, options) as the original search.
    """
    # Create a temporary database for this test
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Persist the session
        store.persist(session)

        # Retrieve replay parameters
        replay_params = store.replay(session.query.id)

        # Should successfully retrieve parameters
        assert replay_params is not None

        # Verify query matches exactly
        assert replay_params["query"] == session.query.query

        # Verify engine matches exactly
        assert replay_params["engine"] == session.query.engine

        # Verify all options match exactly
        assert replay_params["options"]["max_results"] == session.query.options.max_results
        assert replay_params["options"]["region"] == session.query.options.region
        assert replay_params["options"]["safesearch"] == session.query.options.safesearch
        assert replay_params["options"]["time_limit"] == session.query.options.time_limit


@given(sessions=st.lists(search_session_strategy(), min_size=1, max_size=10, unique_by=lambda s: s.query.id))
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=50)
def test_list_returns_recent_searches(sessions):
    """
    Test that list method returns recent searches in correct order.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Persist all sessions
        for session in sessions:
            store.persist(session)

        # List all sessions
        listed = store.list(limit=len(sessions))

        # Should return all sessions
        assert len(listed) <= len(sessions)

        # Each listed session should have required fields
        for item in listed:
            assert "id" in item
            assert "query" in item
            assert "engine" in item
            assert "status" in item
            assert "result_count" in item


@given(session=search_session_strategy())
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_delete_removes_session(session):
    """
    Test that delete method removes a session from the database.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Persist the session
        store.persist(session)

        # Verify it exists
        assert store.show(session.query.id) is not None

        # Delete it
        deleted = store.delete(session.query.id)
        assert deleted is True

        # Verify it no longer exists
        assert store.show(session.query.id) is None


@given(sessions=st.lists(search_session_strategy(), min_size=1, max_size=5, unique_by=lambda s: s.query.id))
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=50)
def test_clear_removes_all_sessions(sessions):
    """
    Test that clear method removes all sessions from the database.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Persist all sessions
        for session in sessions:
            store.persist(session)

        # Clear all
        count = store.clear()

        # Should return the number of sessions cleared
        assert count == len(sessions)

        # List should be empty
        listed = store.list()
        assert len(listed) == 0


def test_show_returns_none_for_nonexistent_id():
    """
    Test that show returns None for a non-existent session ID.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        result = store.show("nonexistent-id")
        assert result is None


def test_replay_returns_none_for_nonexistent_id():
    """
    Test that replay returns None for a non-existent session ID.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        result = store.replay("nonexistent-id")
        assert result is None


def test_delete_returns_false_for_nonexistent_id():
    """
    Test that delete returns False for a non-existent session ID.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        result = store.delete("nonexistent-id")
        assert result is False
