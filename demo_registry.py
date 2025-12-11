"""
Demo script showing the AdapterRegistry functionality.
"""

from typing import Generator, List

from mudhound.adapters.base import SearchAdapter
from mudhound.adapters.registry import AdapterRegistry
from mudhound.core.result import SearchOptions, SearchResult


# Create a demo adapter
class DemoAdapter(SearchAdapter):
    """Demo adapter for testing."""

    @property
    def name(self) -> str:
        return "demo"

    @property
    def display_name(self) -> str:
        return "Demo Search Engine"

    def search(self, query: str, options: SearchOptions) -> Generator[SearchResult, None, None]:
        """Yield demo results."""
        for i in range(3):
            yield SearchResult(
                url=f"https://demo.com/result{i}",
                title=f"Demo Result {i}",
                snippet=f"This is a demo result for: {query}",
                source="demo.com",
                rank=i + 1,
                metadata={"demo": True},
            )

    def validate_options(self, options: SearchOptions) -> List[str]:
        """Validate options."""
        errors = []
        if options.max_results < 1:
            errors.append("max_results must be at least 1")
        return errors


def main():
    print("=== AdapterRegistry Demo ===\n")

    # 1. Register an adapter manually
    print("1. Registering DemoAdapter...")
    AdapterRegistry.register(DemoAdapter)
    print(f"   Registered: {AdapterRegistry.list_available()}\n")

    # 2. Retrieve the adapter
    print("2. Retrieving DemoAdapter...")
    adapter_class = AdapterRegistry.get("demo")
    print(f"   Retrieved: {adapter_class}\n")

    # 3. Use the adapter
    print("3. Using the adapter to search...")
    adapter = adapter_class()
    options = SearchOptions(max_results=3)
    results = list(adapter.search("test query", options))
    print(f"   Found {len(results)} results:")
    for result in results:
        print(f"   - {result.title}: {result.url}")
    print()

    # 4. Discover built-in adapters
    print("4. Discovering built-in adapters...")
    AdapterRegistry.discover_builtin()
    print(f"   Available adapters: {AdapterRegistry.list_available()}\n")

    # 5. Try to get a non-existent adapter
    print("5. Trying to get non-existent adapter...")
    try:
        AdapterRegistry.get("nonexistent")
    except Exception as e:
        print(f"   Error (expected): {e}\n")

    # 6. List all available adapters
    print("6. Final list of available adapters:")
    for adapter_name in AdapterRegistry.list_available():
        adapter_class = AdapterRegistry.get(adapter_name)
        instance = adapter_class()
        print(f"   - {adapter_name}: {instance.display_name}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
