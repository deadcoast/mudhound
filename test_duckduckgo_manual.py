"""
Manual test for DuckDuckGo adapter.

This script performs a real search using the DuckDuckGo adapter.
Run this manually to verify the adapter works with the actual API.

Usage:
    python test_duckduckgo_manual.py
"""

from mudhound.adapters import DuckDuckGoAdapter
from mudhound.core.result import SearchOptions
from mudhound.core.exceptions import NetworkError, RateLimitError


def test_duckduckgo_search():
    """Test a real DuckDuckGo search."""
    print("Testing DuckDuckGo adapter...")
    print("-" * 60)
    
    # Create adapter
    adapter = DuckDuckGoAdapter()
    print(f"Adapter: {adapter.display_name} ({adapter.name})")
    
    # Create search options
    options = SearchOptions(
        max_results=5,
        region="wt-wt",
        safesearch="moderate",
        time_limit=None
    )
    
    # Validate options
    errors = adapter.validate_options(options)
    if errors:
        print(f"Validation errors: {errors}")
        return
    
    print(f"Options: max_results={options.max_results}, region={options.region}")
    print()
    
    # Perform search
    query = "python programming"
    print(f"Searching for: '{query}'")
    print("-" * 60)
    
    try:
        results = []
        for result in adapter.search(query, options):
            results.append(result)
            print(f"\n[{result.rank}] {result.title}")
            print(f"    URL: {result.url}")
            print(f"    Source: {result.source}")
            print(f"    Snippet: {result.snippet[:100]}...")
        
        print()
        print("-" * 60)
        print(f"Total results: {len(results)}")
        print(f"Max results requested: {options.max_results}")
        print(f"Results within limit: {len(results) <= options.max_results}")
        
        # Verify all results have required fields
        all_valid = True
        for result in results:
            if not all([result.url, result.title, result.source, result.rank > 0]):
                all_valid = False
                print(f"Invalid result: {result}")
        
        print(f"All results valid: {all_valid}")
        
    except RateLimitError as e:
        print(f"Rate limit error: {e.message}")
        print(f"Retry after: {e.retry_after} seconds")
        
    except NetworkError as e:
        print(f"Network error: {e.message}")
        
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {str(e)}")


if __name__ == "__main__":
    test_duckduckgo_search()
