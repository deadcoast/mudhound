"""
Unit tests for history CLI commands.

Tests the history command subcommands: list, show, replay, delete, clear.
"""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from mudhound.cli.app import app
from mudhound.core.result import (
    SearchOptions,
    SearchQuery,
    SearchResult,
    SearchSession,
    SearchStatus,
)
from mudhound.core.store import ResultStore

runner = CliRunner()


def create_test_session(session_id="test-session-123"):
    """Create a test search session for testing."""
    options = SearchOptions(
        max_results=10,
        region="wt-wt",
        safesearch="moderate",
    )

    query = SearchQuery(
        id=session_id,
        query="test query",
        engine="duckduckgo",
        options=options,
        created_at=datetime.now(),
        status=SearchStatus.COMPLETE,
    )

    results = [
        SearchResult(
            url=f"https://example.com/{i}",
            title=f"Test Result {i}",
            snippet=f"This is test result {i}",
            source="example.com",
            rank=i,
            metadata={},
        )
        for i in range(1, 6)
    ]

    session = SearchSession(
        query=query,
        results=results,
        started_at=datetime.now(),
        completed_at=datetime.now(),
    )

    return session


def test_history_list_empty():
    """Test that history list handles empty history."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store = ResultStore(db_path=db_path)
            mock_store_class.return_value = mock_store

            result = runner.invoke(app, ["history", "list"])

            assert result.exit_code == 0
            assert "No search history found" in result.stdout


def test_history_list_with_sessions():
    """Test that history list displays sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session()
        store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(app, ["history", "list"])

            assert result.exit_code == 0
            assert "Search History" in result.stdout
            # Query may be split across lines in table, check for "test" and "query"
            assert "test" in result.stdout.lower()
            assert "query" in result.stdout.lower()
            assert "duckduc" in result.stdout  # May be truncated
            assert "5" in result.stdout  # result count


def test_history_list_with_limit():
    """Test that history list respects limit option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist multiple test sessions
        for i in range(5):
            session = create_test_session(session_id=f"test-session-{i}")
            store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(app, ["history", "list", "--limit", "3"])

            assert result.exit_code == 0
            assert "Search History" in result.stdout


def test_history_show_full_id():
    """Test that history show displays full session details."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session(session_id="test-session-123")
        store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(
                app, ["history", "show", "test-session-123"])

            assert result.exit_code == 0
            assert "Search Session:" in result.stdout
            assert "test query" in result.stdout
            assert "duckduckgo" in result.stdout
            assert "complete" in result.stdout.lower()  # Status may be lowercase
            assert "Test Result 1" in result.stdout


def test_history_show_short_id():
    """Test that history show works with short IDs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session(session_id="test-session-123")
        store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(app, ["history", "show", "test-ses"])

            assert result.exit_code == 0
            assert "Search Session:" in result.stdout
            assert "test query" in result.stdout


def test_history_show_not_found():
    """Test that history show handles nonexistent sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(app, ["history", "show", "nonexistent"])

            assert result.exit_code == 1
            assert "no session found" in result.output.lower()


def test_history_show_ambiguous_id():
    """Test that history show handles ambiguous short IDs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist multiple sessions with similar IDs
        session1 = create_test_session(session_id="test-session-123")
        session2 = create_test_session(session_id="test-session-456")
        store.persist(session1)
        store.persist(session2)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(app, ["history", "show", "test"])

            assert result.exit_code == 1
            assert "Ambiguous" in result.output


def test_history_delete_with_yes():
    """Test that history delete removes a session."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session(session_id="test-session-123")
        store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(
                app, ["history", "delete", "test-session-123", "--yes"])

            assert result.exit_code == 0
            assert "Session deleted" in result.stdout

            # Verify session was deleted
            assert store.show("test-session-123") is None


def test_history_delete_without_yes():
    """Test that history delete prompts for confirmation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session(session_id="test-session-123")
        store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            # Answer 'n' to confirmation
            result = runner.invoke(
                app, ["history", "delete", "test-session-123"], input="n\n")

            assert result.exit_code == 0
            assert "Delete cancelled" in result.stdout

            # Verify session was not deleted
            assert store.show("test-session-123") is not None


def test_history_delete_short_id():
    """Test that history delete works with short IDs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session(session_id="test-session-123")
        store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(
                app, ["history", "delete", "test-ses", "--yes"])

            assert result.exit_code == 0
            assert "Session deleted" in result.stdout


def test_history_clear_with_yes():
    """Test that history clear removes all sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist multiple test sessions
        for i in range(3):
            session = create_test_session(session_id=f"test-session-{i}")
            store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(app, ["history", "clear", "--yes"])

            assert result.exit_code == 0
            assert "Cleared 3 session(s)" in result.stdout

            # Verify all sessions were deleted
            assert len(store.list()) == 0


def test_history_clear_without_yes():
    """Test that history clear prompts for confirmation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session()
        store.persist(session)

        # Mock ResultStore to use test database
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            # Answer 'n' to confirmation
            result = runner.invoke(app, ["history", "clear"], input="n\n")

            assert result.exit_code == 0
            assert "Clear cancelled" in result.stdout

            # Verify sessions were not deleted
            assert len(store.list()) == 1


def test_history_replay():
    """Test that history replay re-executes a search."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session(session_id="test-session-123")
        store.persist(session)

        # Mock ResultStore and SearchEngine
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            with patch("mudhound.cli.commands.history.SearchEngine") as mock_engine_class:
                # Create a mock search engine that returns a new session
                mock_engine = MagicMock()
                new_session = create_test_session(session_id="new-session-456")
                mock_engine.search.return_value = new_session
                mock_engine_class.return_value = mock_engine

                result = runner.invoke(
                    app, ["history", "replay", "test-session-123"])

                assert result.exit_code == 0
                assert "Replaying search:" in result.stdout
                assert "test query" in result.stdout
                assert "Search completed" in result.stdout

                # Verify search was called with correct parameters
                mock_engine.search.assert_called_once()
                call_kwargs = mock_engine.search.call_args[1]
                assert call_kwargs["query"] == "test query"
                assert call_kwargs["options"].max_results == 10


def test_history_replay_short_id():
    """Test that history replay works with short IDs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Create and persist a test session
        session = create_test_session(session_id="test-session-123")
        store.persist(session)

        # Mock ResultStore and SearchEngine
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            with patch("mudhound.cli.commands.history.SearchEngine") as mock_engine_class:
                mock_engine = MagicMock()
                new_session = create_test_session(session_id="new-session-456")
                mock_engine.search.return_value = new_session
                mock_engine_class.return_value = mock_engine

                result = runner.invoke(app, ["history", "replay", "test-ses"])

                assert result.exit_code == 0
                assert "Replaying search:" in result.stdout


def test_history_replay_not_found():
    """Test that history replay handles nonexistent sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_history.db"
        store = ResultStore(db_path=db_path)

        # Mock ResultStore
        with patch("mudhound.cli.commands.history.ResultStore") as mock_store_class:
            mock_store_class.return_value = store

            result = runner.invoke(app, ["history", "replay", "nonexistent"])

            assert result.exit_code == 1
            assert "no session found" in result.output.lower()
