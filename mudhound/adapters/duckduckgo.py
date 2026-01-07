"""
DuckDuckGo search adapter implementation.

This module provides a search adapter for DuckDuckGo using the duckduckgo-search library.
It supports streaming results, rate limit detection, and comprehensive error handling.
"""

from typing import Generator, List

from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import (
    DuckDuckGoSearchException,
    RatelimitException,
    TimeoutException,
)

from mudhound.adapters.base import SearchAdapter
from mudhound.core.exceptions import NetworkError, RateLimitError
from mudhound.core.result import SearchOptions, SearchResult


class DuckDuckGoAdapter(SearchAdapter):
    """Search adapter for DuckDuckGo.

    This adapter uses the duckduckgo-search library to perform searches without
    requiring API keys or authentication. It supports all standard search options
    including region, safesearch, and time limits.

    Features:
        - Streaming results via generator
        - Rate limit detection and handling
        - Network error handling
        - Support for max_results, region, safesearch, time_limit options
    """

    @property
    def name(self) -> str:
        """Internal identifier for the adapter.

        Returns:
            "duckduckgo"
        """
        return "duckduckgo"

    @property
    def display_name(self) -> str:
        """Human-readable name for the adapter.

        Returns:
            "DuckDuckGo"
        """
        return "DuckDuckGo"

    def search(self, query: str, options: SearchOptions) -> Generator[SearchResult, None, None]:
        """Execute a DuckDuckGo search and yield results as a generator.

        This method performs a search using the duckduckgo-search library and
        yields SearchResult objects one at a time. It handles rate limits and
        network errors appropriately.

        Args:
            query: The search query string
            options: Search configuration options

        Yields:
            SearchResult objects as they are retrieved

        Raises:
            NetworkError: If network connectivity issues occur
            RateLimitError: If rate limits are exceeded
        """
        # Validate options first
        errors = self.validate_options(options)
        if errors:
            raise NetworkError(f"Invalid search options: {', '.join(errors)}")

        try:
            # Create DDGS instance
            ddgs = DDGS()

            # Map our safesearch values to DDGS values
            # DDGS expects: -2 (off), -1 (moderate), 1 (strict)
            safesearch_map = {"off": -2, "moderate": -1, "strict": 1}
            safesearch_value = safesearch_map.get(options.safesearch, -1)

            # Map time_limit to DDGS timelimit parameter
            # DDGS expects: None, 'd', 'w', 'm', 'y'
            timelimit = options.time_limit

            # Execute search with text method
            # The text method returns an iterator of results
            results = ddgs.text(
                keywords=query,
                region=options.region,
                safesearch=safesearch_value,
                timelimit=timelimit,
                max_results=options.max_results,
            )

            # Yield results one at a time
            rank = 1
            for result in results:
                # Extract fields from DuckDuckGo result
                # DuckDuckGo returns: title, href, body
                url = result.get("href", "")
                title = result.get("title", "")
                snippet = result.get("body", "")

                # Extract source from URL (domain name)
                source = self._extract_source(url)

                # Create SearchResult and yield it
                search_result = SearchResult(
                    url=url,
                    title=title,
                    snippet=snippet,
                    source=source,
                    rank=rank,
                    metadata=result,  # Store full result as metadata
                )

                yield search_result
                rank += 1

        except RatelimitException:
            # DuckDuckGo rate limit exceeded
            # Suggest waiting 60 seconds by default
            retry_after = self.on_rate_limit(60)
            raise RateLimitError(
                f"DuckDuckGo rate limit exceeded. Please wait {retry_after} seconds.",
                retry_after=retry_after,
            )

        except TimeoutException as e:
            # Network timeout
            raise NetworkError(f"Network timeout while searching DuckDuckGo: {str(e)}")

        except DuckDuckGoSearchException as e:
            # Other DuckDuckGo-specific errors
            raise NetworkError(f"DuckDuckGo search error: {str(e)}")

        except Exception as e:
            # Catch-all for unexpected errors
            raise NetworkError(f"Unexpected error during DuckDuckGo search: {str(e)}")

    def validate_options(self, options: SearchOptions) -> List[str]:
        """Validate search options for DuckDuckGo.

        Checks that all options are valid for DuckDuckGo searches:
        - max_results must be at least 1
        - safesearch must be "off", "moderate", or "strict"
        - time_limit must be None or one of "d", "w", "m", "y"
        - region should be a valid region code (basic validation)

        Args:
            options: Search configuration options to validate

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Validate max_results
        if options.max_results < 1:
            errors.append("max_results must be at least 1")

        # Validate safesearch
        if options.safesearch not in ["off", "moderate", "strict"]:
            errors.append("safesearch must be 'off', 'moderate', or 'strict'")

        # Validate time_limit
        if options.time_limit is not None:
            if options.time_limit not in ["d", "w", "m", "y"]:
                errors.append("time_limit must be None, 'd', 'w', 'm', or 'y'")

        # Validate region (basic check - should be non-empty string)
        if not isinstance(options.region, str) or len(options.region) == 0:
            errors.append("region must be a non-empty string")

        return errors

    def _extract_source(self, url: str) -> str:
        """Extract the source domain from a URL.

        Args:
            url: The full URL

        Returns:
            The domain name (e.g., "example.com")
        """
        try:
            # Simple extraction: remove protocol and path
            if "://" in url:
                url = url.split("://", 1)[1]

            # Remove path
            if "/" in url:
                url = url.split("/", 1)[0]

            # Remove port
            if ":" in url:
                url = url.split(":", 1)[0]

            return url
        except Exception:
            # If extraction fails, return the original URL
            return url
