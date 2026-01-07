"""
Adapter registry for managing search engine adapters.

This module provides the AdapterRegistry class which manages registration,
discovery, and retrieval of search engine adapters. It supports:
- Manual registration of adapters
- Discovery from built-in modules
- Plugin discovery (mudhound_adapter_* packages)
- User adapter discovery (~/.mudhound/adapters/)
"""

import importlib
import importlib.util
import pkgutil
import sys
from pathlib import Path
from typing import Dict, List, Type

from mudhound.adapters.base import SearchAdapter
from mudhound.core.exceptions import AdapterNotFoundError


class AdapterRegistry:
    """Registry for managing search engine adapters.

    The AdapterRegistry provides a centralized system for registering and
    retrieving search engine adapters. It supports multiple discovery mechanisms:

    1. Manual registration via the register() class method
    2. Built-in adapter discovery from mudhound.adapters package
    3. Plugin discovery from mudhound_adapter_* packages
    4. User adapter discovery from ~/.mudhound/adapters/

    Attributes:
        _adapters: Dictionary mapping adapter names to adapter classes
    """

    _adapters: Dict[str, Type[SearchAdapter]] = {}

    @classmethod
    def register(cls, adapter_class: Type[SearchAdapter]) -> None:
        """Register a search adapter.

        Registers an adapter class with the registry. The adapter's name
        property is used as the registration key.

        Args:
            adapter_class: The SearchAdapter subclass to register

        Raises:
            TypeError: If adapter_class is not a SearchAdapter subclass
        """
        if not issubclass(adapter_class, SearchAdapter):
            raise TypeError(f"{adapter_class.__name__} must be a subclass of SearchAdapter")

        # Instantiate to get the name property
        instance = adapter_class()
        adapter_name = instance.name

        cls._adapters[adapter_name] = adapter_class

    @classmethod
    def get(cls, adapter_name: str) -> Type[SearchAdapter]:
        """Retrieve an adapter by name.

        Args:
            adapter_name: The name of the adapter to retrieve

        Returns:
            The adapter class

        Raises:
            AdapterNotFoundError: If the adapter is not registered
        """
        if adapter_name not in cls._adapters:
            raise AdapterNotFoundError(adapter_name)

        return cls._adapters[adapter_name]

    @classmethod
    def list_available(cls) -> List[str]:
        """List all available adapter names.

        Returns:
            List of registered adapter names
        """
        return list(cls._adapters.keys())

    @classmethod
    def discover_builtin(cls) -> None:
        """Discover and register built-in adapters.

        Searches the mudhound.adapters package for adapter modules and
        automatically registers any SearchAdapter subclasses found.
        """
        import mudhound.adapters

        # Get the adapters package path
        adapters_path = Path(mudhound.adapters.__file__).parent

        # Iterate through all Python files in the adapters directory
        for module_info in pkgutil.iter_modules([str(adapters_path)]):
            module_name = module_info.name

            # Skip base, registry, and __init__ modules
            if module_name in ("base", "registry", "__init__"):
                continue

            try:
                # Import the module
                full_module_name = f"mudhound.adapters.{module_name}"
                module = importlib.import_module(full_module_name)

                # Look for SearchAdapter subclasses in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    # Check if it's a class, a SearchAdapter subclass, and not the base class
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, SearchAdapter)
                        and attr is not SearchAdapter
                    ):
                        cls.register(attr)

            except Exception:
                # Silently skip modules that fail to import
                # This allows the system to continue even if some adapters are broken
                pass

    @classmethod
    def discover_plugins(cls) -> None:
        """Discover and register plugin adapters.

        Searches for installed packages matching the pattern mudhound_adapter_*
        and attempts to register adapters from them. This enables third-party
        adapter plugins.

        Plugin packages should expose their adapter class in the package's
        __init__.py or in a module named 'adapter'.
        """
        # Iterate through all installed packages
        for _finder, name, _ispkg in pkgutil.iter_modules():
            # Check if package name matches the plugin pattern
            if name.startswith("mudhound_adapter_"):
                try:
                    # Import the plugin package
                    plugin_module = importlib.import_module(name)

                    # Look for SearchAdapter subclasses
                    for attr_name in dir(plugin_module):
                        attr = getattr(plugin_module, attr_name)

                        if (
                            isinstance(attr, type)
                            and issubclass(attr, SearchAdapter)
                            and attr is not SearchAdapter
                        ):
                            cls.register(attr)

                except Exception:
                    # Silently skip plugins that fail to load
                    pass

    @classmethod
    def discover_user_adapters(cls) -> None:
        """Discover and register user-defined adapters.

        Searches the ~/.mudhound/adapters/ directory for Python files
        containing adapter implementations. This allows users to create
        custom adapters without packaging them as plugins.

        Each Python file in the directory is imported and searched for
        SearchAdapter subclasses.
        """
        # Get the user adapters directory
        user_adapters_dir = Path.home() / ".mudhound" / "adapters"

        # Check if the directory exists
        if not user_adapters_dir.exists() or not user_adapters_dir.is_dir():
            return

        # Add the directory to sys.path temporarily
        user_adapters_str = str(user_adapters_dir)
        if user_adapters_str not in sys.path:
            sys.path.insert(0, user_adapters_str)

        try:
            # Iterate through Python files in the directory
            for py_file in user_adapters_dir.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue

                try:
                    # Load the module from file
                    module_name = py_file.stem
                    spec = importlib.util.spec_from_file_location(module_name, py_file)

                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # Look for SearchAdapter subclasses
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)

                            if (
                                isinstance(attr, type)
                                and issubclass(attr, SearchAdapter)
                                and attr is not SearchAdapter
                            ):
                                cls.register(attr)

                except Exception:
                    # Silently skip files that fail to load
                    pass

        finally:
            # Remove the directory from sys.path
            if user_adapters_str in sys.path:
                sys.path.remove(user_adapters_str)

    @classmethod
    def discover_all(cls) -> None:
        """Discover and register all adapters from all sources.

        This is a convenience method that calls all discovery methods:
        - discover_builtin()
        - discover_plugins()
        - discover_user_adapters()
        """
        cls.discover_builtin()
        cls.discover_plugins()
        cls.discover_user_adapters()

    @classmethod
    def clear(cls) -> None:
        """Clear all registered adapters.

        This method is primarily useful for testing purposes.
        """
        cls._adapters.clear()
