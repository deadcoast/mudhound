"""
Data models for search operations.

This module defines the core data structures used throughout MudHound:
- SearchResult: Individual search result
- SearchOptions: Configuration for search operations
- SearchStatus: Enum for search operation states
- SearchQuery: Search request representation
- SearchSession: Complete search session with results and metadata
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class SearchStatus(Enum):
    """Status of a search operation."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class SearchResult:
    """Individual search result from a search engine.
    
    Attributes:
        url: The URL of the search result
        title: The title of the page
        snippet: A text snippet/description from the page
        source: The source/domain of the result
        rank: The position in search results (1-indexed)
        metadata: Additional metadata specific to the search engine
    """

    url: str
    title: str
    snippet: str
    source: str
    rank: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchOptions:
    """Configuration options for search operations.
    
    Attributes:
        max_results: Maximum number of results to retrieve (default: 50)
        region: Region code for search localization (default: "wt-wt" for worldwide)
        safesearch: Safe search level - "off", "moderate", or "strict" (default: "moderate")
        time_limit: Time limit for results - None, "d" (day), "w" (week), "m" (month), "y" (year)
    """

    max_results: int = 50
    region: str = "wt-wt"
    safesearch: str = "moderate"
    time_limit: Optional[str] = None


@dataclass
class SearchQuery:
    """Representation of a search request.
    
    Attributes:
        id: Unique identifier for the query
        query: The search query string
        engine: Name of the search engine adapter to use
        options: Search configuration options
        created_at: Timestamp when the query was created
        status: Current status of the search operation
    """

    id: str
    query: str
    engine: str
    options: SearchOptions
    created_at: datetime
    status: SearchStatus


@dataclass
class SearchSession:
    """Complete search session including query, results, and metadata.
    
    Attributes:
        query: The search query that was executed
        results: List of search results
        started_at: Timestamp when the search started
        completed_at: Timestamp when the search completed (None if still running)
        error: Error message if the search failed (None if successful)
    """

    query: SearchQuery
    results: List[SearchResult]
    started_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    @property
    def duration(self) -> Optional[float]:
        """Calculate the duration of the search session in seconds.
        
        Returns:
            Duration in seconds if completed, None if still running
        """
        if self.completed_at is None:
            return None
        return (self.completed_at - self.started_at).total_seconds()

    @property
    def result_count(self) -> int:
        """Get the number of results in this session.
        
        Returns:
            Number of search results
        """
        return len(self.results)
