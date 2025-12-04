"""Search engine adapter layer."""

from mudhound.adapters.base import SearchAdapter
from mudhound.adapters.registry import AdapterRegistry
from mudhound.adapters.duckduckgo import DuckDuckGoAdapter

__all__ = ["SearchAdapter", "AdapterRegistry", "DuckDuckGoAdapter"]
