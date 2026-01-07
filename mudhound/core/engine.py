"""
Search engine orchestration.

This module provides the SearchEngine class which coordinates search operations,
manages sessions, handles errors, and integrates with the result store.
"""

import time
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Callable, List, Optional

if TYPE_CHECKING:
    from mudhound.adapters.base import SearchAdapter

from mudhound.core.exceptions import (
    AdapterError,
    NetworkError,
    RateLimitError,
    ValidationError,
)
from mudhound.core.result import (
    SearchOptions,
    SearchQuery,
    SearchResult,
    SearchSession,
    SearchStatus,
)


class SearchEngine:
    """Orchestrates search operations across different adapters.

    The SearchEngine coordinates all aspects of a search operation:
    - Adapter selection and validation
    - Progress tracking and callbacks
    - Result collection
    - Session management
    - Error handling and retry logic
    - Cancellation support

    Attributes:
        adapter: The search adapter to use for searches
        max_retries: Maximum number of retry attempts for failed searches
        retry_delay: Base delay in seconds between retries (uses exponential backoff)
    """

    def __init__(
        self,
        adapter: Optional["SearchAdapter"] = None,
        adapter_name: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize the SearchEngine.

        Args:
            adapter: A SearchAdapter instance to use (takes precedence over adapter_name)
            adapter_name: Name of adapter to load from registry (used if adapter is None)
            max_retries: Maximum number of retry attempts for failed searches
            retry_delay: Base delay in seconds between retries

        Raises:
            ValueError: If neither adapter nor adapter_name is provided
            AdapterNotFoundError: If adapter_name is not found in registry
        """
        if adapter is not None:
            self.adapter = adapter
        elif adapter_name is not None:
            # Import here to avoid circular import
            from mudhound.adapters.registry import AdapterRegistry

            adapter_class = AdapterRegistry.get(adapter_name)
            self.adapter = adapter_class()
        else:
            raise ValueError("Either adapter or adapter_name must be provided")

        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def search(
        self,
        query: str,
        options: Optional[SearchOptions] = None,
        progress_callback: Optional[Callable[[SearchResult], None]] = None,
        on_complete: Optional[Callable[[SearchSession], None]] = None,
    ) -> SearchSession:
        """Execute a search operation.

        This method coordinates the entire search process:
        1. Validates search options
        2. Creates a SearchQuery and SearchSession
        3. Executes the search with the adapter
        4. Collects results with progress callbacks
        5. Handles errors with retry logic
        6. Returns the completed session

        Args:
            query: The search query string
            options: Search configuration options (uses defaults if None)
            progress_callback: Optional callback invoked for each result
            on_complete: Optional callback invoked when search completes

        Returns:
            SearchSession containing query, results, and metadata

        Raises:
            ValidationError: If search options are invalid
            NetworkError: If network errors occur after all retries
            RateLimitError: If rate limits are exceeded
            AdapterError: For other adapter-specific errors
            KeyboardInterrupt: If user cancels with CTRL+C
        """
        # Use default options if none provided
        if options is None:
            options = SearchOptions()

        # Validate options
        validation_errors = self.adapter.validate_options(options)
        if validation_errors:
            raise ValidationError(f"Invalid search options: {', '.join(validation_errors)}")

        # Create search query
        query_id = str(uuid.uuid4())
        search_query = SearchQuery(
            id=query_id,
            query=query,
            engine=self.adapter.name,
            options=options,
            created_at=datetime.now(),
            status=SearchStatus.PENDING,
        )

        # Create search session
        session = SearchSession(
            query=search_query,
            results=[],
            started_at=datetime.now(),
        )

        # Update status to running
        search_query.status = SearchStatus.RUNNING

        # Execute search with retry logic
        retry_count = 0
        last_error = None

        while retry_count <= self.max_retries:
            try:
                # Execute the search
                results = self._execute_search(
                    query=query,
                    options=options,
                    progress_callback=progress_callback,
                )

                # Update session with results
                session.results = results
                session.completed_at = datetime.now()
                search_query.status = SearchStatus.COMPLETE

                # Call completion callback if provided
                if on_complete:
                    on_complete(session)

                return session

            except KeyboardInterrupt:
                # User cancelled - update status and re-raise
                search_query.status = SearchStatus.CANCELLED
                session.completed_at = datetime.now()
                session.error = "Cancelled by user"
                raise

            except RateLimitError as e:
                # Rate limit - don't retry, just raise
                search_query.status = SearchStatus.FAILED
                session.completed_at = datetime.now()
                session.error = str(e)
                raise

            except NetworkError as e:
                # Network error - retry with exponential backoff
                last_error = e
                retry_count += 1

                if retry_count <= self.max_retries:
                    # Calculate backoff delay
                    delay = self.retry_delay * (2 ** (retry_count - 1))
                    time.sleep(delay)
                else:
                    # Max retries exceeded
                    search_query.status = SearchStatus.FAILED
                    session.completed_at = datetime.now()
                    session.error = f"Network error after {self.max_retries} retries: {str(e)}"
                    raise

            except AdapterError as e:
                # Other adapter error - don't retry
                search_query.status = SearchStatus.FAILED
                session.completed_at = datetime.now()
                session.error = str(e)
                raise

            except Exception as e:
                # Unexpected error - don't retry
                search_query.status = SearchStatus.FAILED
                session.completed_at = datetime.now()
                session.error = f"Unexpected error: {str(e)}"
                raise AdapterError(f"Unexpected error during search: {str(e)}")

        # Should never reach here, but just in case
        search_query.status = SearchStatus.FAILED
        session.completed_at = datetime.now()
        session.error = f"Search failed after {self.max_retries} retries"
        if last_error:
            raise last_error
        raise AdapterError("Search failed")

    def _execute_search(
        self,
        query: str,
        options: SearchOptions,
        progress_callback: Optional[Callable[[SearchResult], None]] = None,
    ) -> List[SearchResult]:
        """Execute the actual search and collect results.

        This is an internal method that handles the low-level search execution.

        Args:
            query: The search query string
            options: Search configuration options
            progress_callback: Optional callback invoked for each result

        Returns:
            List of SearchResult objects

        Raises:
            NetworkError: If network errors occur
            RateLimitError: If rate limits are exceeded
            AdapterError: For other adapter-specific errors
            KeyboardInterrupt: If user cancels with CTRL+C
        """
        results = []

        try:
            # Execute search as generator
            for result in self.adapter.search(query, options):
                # Add result to collection
                results.append(result)

                # Call progress callback if provided
                if progress_callback:
                    progress_callback(result)

        except KeyboardInterrupt:
            # User cancelled - re-raise to be handled by caller
            raise

        except (NetworkError, RateLimitError, AdapterError):
            # Known adapter errors - re-raise to be handled by caller
            raise

        except Exception as e:
            # Wrap unexpected errors in AdapterError
            raise AdapterError(f"Unexpected error during search: {str(e)}")

        return results
