"""
Configuration management system for MudHound.

This module provides the ConfigManager class which handles loading, saving,
and accessing configuration from multiple sources with a priority chain:
CLI override → environment variable → current directory → XDG standard → legacy → defaults
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Handle Python 3.11+ where tomllib is built-in
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w

from mudhound.core.exceptions import ConfigError

# Default configuration schema
DEFAULT_CONFIG = {
    "general": {
        "engine": "duckduckgo",
        "max_results": 50,
        "region": "wt-wt",
        "safesearch": "moderate",
    },
    "ui": {
        "theme": "default",
        "color": True,
        "animation": True,
        "banner_style": "animated",
        "logo_position": "header",
    },
    "animation": {
        "enabled": True,
        "fps": 10,
        "color_scheme": "rainbow",
        "easing": "linear",
    },
    "search": {
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "stream_results": True,
    },
    "export": {
        "default_format": "json",
        "default_directory": "~/.mudhound/exports",
        "include_metadata": True,
    },
    "logging": {
        "level": "INFO",
        "file_logging": False,
        "log_file": "~/.mudhound/logs/mudhound.log",
        "max_size": 10485760,  # 10MB
        "backup_count": 5,
    },
    "adapters": {
        "duckduckgo": {
            "enabled": True,
        },
    },
}


class ConfigManager:
    """Manages application configuration with priority chain loading.
    
    Configuration is loaded from the first found source in this order:
    1. CLI override (passed to constructor)
    2. Environment variable (MUDHOUND_CONFIG)
    3. Current directory (./mudhound.toml or ./.mudhound/config.toml)
    4. XDG standard (~/.config/mudhound/config.toml)
    5. Legacy location (~/.mudhound/config.toml)
    6. Internal defaults
    
    Attributes:
        config: The loaded configuration dictionary
        config_path: Path to the configuration file that was loaded (None for defaults)
    """

    def __init__(self, cli_config_path: Optional[str] = None):
        """Initialize the ConfigManager.
        
        Args:
            cli_config_path: Optional path to config file from CLI argument
        """
        self.config: Dict[str, Any] = {}
        self.config_path: Optional[Path] = None
        self._load_config(cli_config_path)

    def _get_config_search_paths(self, cli_path: Optional[str] = None) -> List[Path]:
        """Get the list of paths to search for configuration files in priority order.
        
        Args:
            cli_path: Optional CLI-provided config path
            
        Returns:
            List of Path objects to search in priority order
        """
        paths = []

        # 1. CLI override
        if cli_path:
            paths.append(Path(cli_path).expanduser().resolve())

        # 2. Environment variable
        env_path = os.environ.get("MUDHOUND_CONFIG")
        if env_path:
            paths.append(Path(env_path).expanduser().resolve())

        # 3. Current directory
        paths.append(Path.cwd() / "mudhound.toml")
        paths.append(Path.cwd() / ".mudhound" / "config.toml")

        # 4. XDG standard
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            paths.append(Path(xdg_config_home) / "mudhound" / "config.toml")
        else:
            paths.append(Path.home() / ".config" / "mudhound" / "config.toml")

        # 5. Legacy location
        paths.append(Path.home() / ".mudhound" / "config.toml")

        return paths

    def _load_config(self, cli_path: Optional[str] = None) -> None:
        """Load configuration from the first available source.
        
        Args:
            cli_path: Optional CLI-provided config path
            
        Raises:
            ConfigError: If a config file is found but cannot be parsed
        """
        # Start with defaults
        self.config = self._deep_copy_dict(DEFAULT_CONFIG)
        self.config_path = None

        # Search for config files
        search_paths = self._get_config_search_paths(cli_path)

        for path in search_paths:
            if path.exists() and path.is_file():
                try:
                    with open(path, "rb") as f:
                        user_config = tomllib.load(f)

                    # Merge user config with defaults
                    self._merge_config(self.config, user_config)
                    self.config_path = path
                    return

                except Exception as e:
                    raise ConfigError(f"Failed to parse config file '{path}': {e}")

        # No config file found, using defaults

    def _deep_copy_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deep copy of a dictionary.
        
        Args:
            d: Dictionary to copy
            
        Returns:
            Deep copy of the dictionary
        """
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = self._deep_copy_dict(value)
            elif isinstance(value, list):
                result[key] = value.copy()
            else:
                result[key] = value
        return result

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Merge override config into base config (modifies base in place).
        
        Args:
            base: Base configuration dictionary (modified in place)
            override: Override configuration dictionary
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.
        
        Supports dot notation for nested keys (e.g., "general.engine").
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value by key.
        
        Supports dot notation for nested keys (e.g., "general.engine").
        Creates intermediate dictionaries as needed.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split(".")
        config = self.config

        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            elif not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value

    def list(self) -> Dict[str, Any]:
        """Get all configuration keys and values.
        
        Returns:
            Complete configuration dictionary
        """
        return self._deep_copy_dict(self.config)

    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to a TOML file.
        
        Args:
            path: Path to save to (defaults to current config_path or XDG location)
            
        Raises:
            ConfigError: If save fails
        """
        if path is None:
            if self.config_path is not None:
                path = self.config_path
            else:
                # Default to XDG location
                xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
                if xdg_config_home:
                    path = Path(xdg_config_home) / "mudhound" / "config.toml"
                else:
                    path = Path.home() / ".config" / "mudhound" / "config.toml"

        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write config
            with open(path, "wb") as f:
                tomli_w.dump(self.config, f)

            self.config_path = path

        except Exception as e:
            raise ConfigError(f"Failed to save config to '{path}': {e}")

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self._deep_copy_dict(DEFAULT_CONFIG)

