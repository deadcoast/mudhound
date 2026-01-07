"""
Result storage and search history management.

This module provides persistent storage for search sessions using SQLite.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mudhound.core.exceptions import MudHoundError
from mudhound.core.result import (
    SearchOptions,
    SearchQuery,
    SearchResult,
    SearchSession,
    SearchStatus,
)


class StoreError(MudHoundError):
    """Errors related to result storage operations."""

    pass


class ResultStore:
    """Persistent storage for search history and results.

    Uses SQLite to store search sessions with full query parameters,
    results, and metadata. Supports listing, retrieving, replaying,
    and deleting search history.

    Attributes:
        db_path: Path to the SQLite database file
    """

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize the result store.

        Args:
            db_path: Path to SQLite database. If None, uses default location
                    (~/.mudhound/history.db)
        """
        if db_path is None:
            db_path = Path.home() / ".mudhound" / "history.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_database()

    def _init_database(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS search_sessions (
                    id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    engine TEXT NOT NULL,
                    options TEXT NOT NULL,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    error TEXT,
                    result_count INTEGER NOT NULL,
                    duration REAL,
                    created_at TEXT NOT NULL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS search_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    snippet TEXT NOT NULL,
                    source TEXT NOT NULL,
                    rank INTEGER NOT NULL,
                    metadata TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES search_sessions(id)
                        ON DELETE CASCADE
                )
            """)

            # Create index for faster lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_created_at
                ON search_sessions(created_at DESC)
            """)

            conn.commit()
        finally:
            conn.close()

    def persist(self, session: SearchSession) -> None:
        """Persist a search session to the database.

        Args:
            session: The search session to store

        Raises:
            StoreError: If the session cannot be persisted
        """
        conn = sqlite3.connect(self.db_path)
        try:
            # Serialize options to JSON
            options_json = json.dumps(
                {
                    "max_results": session.query.options.max_results,
                    "region": session.query.options.region,
                    "safesearch": session.query.options.safesearch,
                    "time_limit": session.query.options.time_limit,
                }
            )

            # Insert session record
            conn.execute(
                """
                INSERT INTO search_sessions (
                    id, query, engine, options, status,
                    started_at, completed_at, error,
                    result_count, duration, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    session.query.id,
                    session.query.query,
                    session.query.engine,
                    options_json,
                    session.query.status.value,
                    session.started_at.isoformat(),
                    session.completed_at.isoformat() if session.completed_at else None,
                    session.error,
                    session.result_count,
                    session.duration,
                    session.query.created_at.isoformat(),
                ),
            )

            # Insert result records
            for result in session.results:
                metadata_json = json.dumps(result.metadata)
                conn.execute(
                    """
                    INSERT INTO search_results (
                        session_id, url, title, snippet,
                        source, rank, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        session.query.id,
                        result.url,
                        result.title,
                        result.snippet,
                        result.source,
                        result.rank,
                        metadata_json,
                    ),
                )

            conn.commit()
        except sqlite3.Error as e:
            raise StoreError(f"Failed to persist session: {e}")
        finally:
            conn.close()

    def list(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List recent search sessions.

        Args:
            limit: Maximum number of sessions to return (default: 20)

        Returns:
            List of session summaries with id, query, result_count,
            status, and timestamp

        Raises:
            StoreError: If sessions cannot be retrieved
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT id, query, engine, status, result_count,
                       started_at, completed_at, duration, error
                FROM search_sessions
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            )

            sessions = []
            for row in cursor:
                sessions.append(
                    {
                        "id": row["id"],
                        "query": row["query"],
                        "engine": row["engine"],
                        "status": row["status"],
                        "result_count": row["result_count"],
                        "started_at": row["started_at"],
                        "completed_at": row["completed_at"],
                        "duration": row["duration"],
                        "error": row["error"],
                    }
                )

            return sessions
        except sqlite3.Error as e:
            raise StoreError(f"Failed to list sessions: {e}")
        finally:
            conn.close()

    def show(self, session_id: str) -> Optional[SearchSession]:
        """Retrieve full results for a specific search session.

        Args:
            session_id: The unique identifier of the session

        Returns:
            The complete SearchSession object, or None if not found

        Raises:
            StoreError: If the session cannot be retrieved
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row

            # Retrieve session record
            cursor = conn.execute(
                """
                SELECT id, query, engine, options, status,
                       started_at, completed_at, error, created_at
                FROM search_sessions
                WHERE id = ?
            """,
                (session_id,),
            )

            row = cursor.fetchone()
            if row is None:
                return None

            # Parse options from JSON
            options_dict = json.loads(row["options"])
            options = SearchOptions(
                max_results=options_dict["max_results"],
                region=options_dict["region"],
                safesearch=options_dict["safesearch"],
                time_limit=options_dict.get("time_limit"),
            )

            # Create SearchQuery
            query = SearchQuery(
                id=row["id"],
                query=row["query"],
                engine=row["engine"],
                options=options,
                created_at=datetime.fromisoformat(row["created_at"]),
                status=SearchStatus(row["status"]),
            )

            # Retrieve results
            results_cursor = conn.execute(
                """
                SELECT url, title, snippet, source, rank, metadata
                FROM search_results
                WHERE session_id = ?
                ORDER BY rank
            """,
                (session_id,),
            )

            results = []
            for result_row in results_cursor:
                metadata = json.loads(result_row["metadata"])
                results.append(
                    SearchResult(
                        url=result_row["url"],
                        title=result_row["title"],
                        snippet=result_row["snippet"],
                        source=result_row["source"],
                        rank=result_row["rank"],
                        metadata=metadata,
                    )
                )

            # Create SearchSession
            session = SearchSession(
                query=query,
                results=results,
                started_at=datetime.fromisoformat(row["started_at"]),
                completed_at=(
                    datetime.fromisoformat(
                        row["completed_at"]) if row["completed_at"] else None
                ),
                error=row["error"],
            )

            return session
        except (sqlite3.Error, json.JSONDecodeError, ValueError) as e:
            raise StoreError(f"Failed to retrieve session: {e}")
        finally:
            conn.close()

    def replay(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve original search parameters for replay.

        Args:
            session_id: The unique identifier of the session

        Returns:
            Dictionary with query, engine, and options, or None if not found

        Raises:
            StoreError: If parameters cannot be retrieved
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT query, engine, options
                FROM search_sessions
                WHERE id = ?
            """,
                (session_id,),
            )

            row = cursor.fetchone()
            if row is None:
                return None

            # Parse options from JSON
            options_dict = json.loads(row["options"])

            return {
                "query": row["query"],
                "engine": row["engine"],
                "options": options_dict,
            }
        except (sqlite3.Error, json.JSONDecodeError) as e:
            raise StoreError(f"Failed to retrieve replay parameters: {e}")
        finally:
            conn.close()

    def delete(self, session_id: str) -> bool:
        """Delete a specific search session.

        Args:
            session_id: The unique identifier of the session

        Returns:
            True if the session was deleted, False if not found

        Raises:
            StoreError: If the session cannot be deleted
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                """
                DELETE FROM search_sessions
                WHERE id = ?
            """,
                (session_id,),
            )
            conn.commit()

            return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise StoreError(f"Failed to delete session: {e}")
        finally:
            conn.close()

    def clear(self) -> int:
        """Delete all search history.

        Returns:
            Number of sessions deleted

        Raises:
            StoreError: If history cannot be cleared
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute("SELECT COUNT(*) FROM search_sessions")
            count = cursor.fetchone()[0]

            conn.execute("DELETE FROM search_sessions")
            conn.execute("DELETE FROM search_results")
            conn.commit()

            return count
        except sqlite3.Error as e:
            raise StoreError(f"Failed to clear history: {e}")
        finally:
            conn.close()
