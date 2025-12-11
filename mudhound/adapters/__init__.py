"""Search engine adapter layer."""

from mudhound.adapters.base import SearchAdapter
from mudhound.adapters.duckduckgo import DuckDuckGoAdapter
from mudhound.adapters.registry import AdapterRegistry

__all__ = ["SearchAdapter", "AdapterRegistry", "DuckDuckGoAdapter"]
