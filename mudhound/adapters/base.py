"""
Base abstract class for search engine adapters.

This module defines the SearchAdapter abstract base class that all search engine
adapters must implement. It provides a standardized interface for search operations,
validation, and rate limit handling.
"""

from abc import ABC, abstractmethod
from typing import Generator, List

from mudhound.core.result import SearchResult, SearchOptions


class SearchAdapter(ABC):
    """Abstract base class for search engine adapters.
    
    All search engine adapters must inherit from this class and implement
    the required abstract properties and methods. This ensures a consistent
    interface across all search engines.
    
    Properties:
        name: Internal identifier for the adapter (e.g., "duckduckgo")
        display_name: Human-readable name for the adapter (e.g., "DuckDuckGo")
    
    Methods:
        search: Execute a search and yield results as a generator
        validate_options: Validate search options and return error messages
        on_rate_limit: Handle rate limit events (optional override)
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Internal identifier for the adapter.
        
        This should be a lowercase, hyphenated string suitable for use
        in configuration files and command-line arguments.
        
        Returns:
            The adapter's internal name (e.g., "duckduckgo")
        """
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name for the adapter.
        
        This is used in user-facing messages and UI components.
        
        Returns:
            The adapter's display name (e.g., "DuckDuckGo")
        """
        pass
    
    @abstractmethod
    def search(
        self,
        query: str,
        options: SearchOptions
    ) -> Generator[SearchResult, None, None]:
        """Execute a search and yield results as a generator.
        
        This method must be implemented as a generator that yields SearchResult
        objects one at a time. This allows for streaming results and progress
        updates during long-running searches.
        
        Args:
            query: The search query string
            options: Search configuration options
            
        Yields:
            SearchResult objects as they are retrieved
            
        Raises:
            NetworkError: If network connectivity issues occur
            RateLimitError: If rate limits are exceeded
            AdapterError: For other adapter-specific errors
        """
        pass
    
    @abstractmethod
    def validate_options(self, options: SearchOptions) -> List[str]:
        """Validate search options and return error messages.
        
        This method checks if the provided search options are valid for this
        adapter. It should return an empty list if all options are valid, or
        a list of error messages describing any validation failures.
        
        Args:
            options: Search configuration options to validate
            
        Returns:
            List of error messages (empty if valid)
        """
        pass
    
    def on_rate_limit(self, retry_after: int) -> int:
        """Handle rate limit events.
        
        This method is called when a rate limit is detected. The default
        implementation simply returns the retry_after duration, but adapters
        can override this to implement custom rate limit handling logic.
        
        Args:
            retry_after: Suggested wait duration in seconds
            
        Returns:
            Actual wait duration in seconds to use
        """
        return retry_after
