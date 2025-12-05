"""
Integration tests for MudHound application wiring.

Tests that all components are properly initialized and connected:
- Adapter registry
- Configuration system
- Logging system
- CLI application
"""

import pytest
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

from mudhound.adapters.registry import AdapterRegistry
from mudhound.adapters.duckduckgo import DuckDuckGoAdapter
from mudhound.core.config import ConfigManager
from mudhound.logging import configure_logging


class TestAdapterIntegration:
    """Test adapter registry integration."""
    
    def test_duckduckgo_adapter_registered(self):
        """Test that DuckDuckGo adapter is registered on startup."""
        # Clear registry first
        AdapterRegistry.clear()
        
        # Discover adapters
        AdapterRegistry.discover_builtin()
        
        # Verify DuckDuckGo is registered
        available = AdapterRegistry.list_available()
        assert "duckduckgo" in available
        
        # Verify we can retrieve it
        adapter_class = AdapterRegistry.get("duckduckgo")
        assert adapter_class == DuckDuckGoAdapter
    
    def test_adapter_discovery_all(self):
        """Test that discover_all finds built-in adapters."""
        # Clear registry first
        AdapterRegistry.clear()
        
        # Discover all adapters
        AdapterRegistry.discover_all()
        
        # Should have at least DuckDuckGo
        available = AdapterRegistry.list_available()
        assert len(available) >= 1
        assert "duckduckgo" in available


class TestConfigurationIntegration:
    """Test configuration system integration."""
    
    def test_config_manager_initialization(self):
        """Test that ConfigManager initializes with defaults."""
        config_manager = ConfigManager()
        
        # Verify default values are loaded
        assert config_manager.get("general.engine") == "duckduckgo"
        assert config_manager.get("general.max_results") == 50
        assert config_manager.get("ui.theme") == "default"
        assert config_manager.get("animation.enabled") is True
    
    def test_config_manager_with_cli_override(self, tmp_path):
        """Test that ConfigManager respects CLI config path."""
        # Create a temporary config file
        config_file = tmp_path / "test_config.toml"
        config_file.write_text("""
[general]
engine = "test_engine"
max_results = 100

[ui]
theme = "custom"
""")
        
        # Initialize with CLI override
        config_manager = ConfigManager(cli_config_path=str(config_file))
        
        # Verify overridden values
        assert config_manager.get("general.engine") == "test_engine"
        assert config_manager.get("general.max_results") == 100
        assert config_manager.get("ui.theme") == "custom"


class TestLoggingIntegration:
    """Test logging system integration."""
    
    def test_logging_configuration(self):
        """Test that logging can be configured."""
        # Configure logging
        logger = configure_logging(
            level=logging.INFO,
            use_color=False,
            log_file=None,
        )
        
        # Verify logger is configured
        assert logger.name == "mudhound"
        assert len(logger.handlers) > 0
        
        # Verify we can log messages
        logger.info("Test message")
        logger.debug("Debug message")
    
    def test_logging_with_file(self, tmp_path):
        """Test that file logging can be configured."""
        log_file = tmp_path / "test.log"
        
        # Configure with file logging
        logger = configure_logging(
            level=logging.INFO,
            use_color=False,
            log_file=log_file,
            file_level=logging.DEBUG,
        )
        
        # Log a message
        logger.info("Test file logging")
        
        # Verify log file was created
        assert log_file.exists()
        
        # Verify content
        content = log_file.read_text()
        assert "Test file logging" in content
    
    def test_logging_levels(self):
        """Test that custom log levels work."""
        from mudhound.logging.levels import TRACE, SUCCESS
        
        logger = configure_logging(level=TRACE, use_color=False)
        
        # Test custom levels
        logger.trace("Trace message")
        logger.success("Success message")


class TestCLIIntegration:
    """Test CLI application integration."""
    
    def test_cli_app_imports(self):
        """Test that CLI app can be imported."""
        from mudhound.cli.app import app
        
        assert app is not None
        assert app.info.name == "mudhound"
    
    def test_cli_commands_registered(self):
        """Test that CLI commands are registered."""
        from mudhound.cli.app import app
        
        # Verify app has registered groups (subcommands)
        group_names = [group.name for group in app.registered_groups]
        assert "config" in group_names
        assert "history" in group_names
        
        # Verify app has some registered commands
        # Note: Typer registers commands dynamically, so we just verify the structure exists
        assert hasattr(app, 'registered_commands')
        assert hasattr(app, 'registered_groups')


class TestMainEntryPoint:
    """Test main entry point integration."""
    
    def test_main_imports(self):
        """Test that main entry point can be imported."""
        from mudhound.__main__ import main, initialize_adapters, initialize_config, initialize_logging
        
        assert callable(main)
        assert callable(initialize_adapters)
        assert callable(initialize_config)
        assert callable(initialize_logging)
    
    def test_initialize_adapters(self):
        """Test adapter initialization function."""
        from mudhound.__main__ import initialize_adapters
        
        # Clear registry
        AdapterRegistry.clear()
        
        # Initialize
        initialize_adapters()
        
        # Verify adapters are registered
        available = AdapterRegistry.list_available()
        assert len(available) >= 1
        assert "duckduckgo" in available
    
    def test_initialize_config(self):
        """Test config initialization function."""
        from mudhound.__main__ import initialize_config
        
        # Initialize
        config_manager = initialize_config()
        
        # Verify config is loaded
        assert config_manager is not None
        assert config_manager.get("general.engine") is not None
    
    def test_initialize_logging(self):
        """Test logging initialization function."""
        from mudhound.__main__ import initialize_logging
        
        # Initialize
        initialize_logging(verbose=False, quiet=False, use_color=False)
        
        # Verify logger exists
        logger = logging.getLogger("mudhound")
        assert logger is not None
        assert len(logger.handlers) > 0


class TestEndToEndIntegration:
    """Test end-to-end integration scenarios."""
    
    def test_full_initialization_sequence(self):
        """Test the complete initialization sequence."""
        from mudhound.__main__ import initialize_adapters, initialize_config, initialize_logging
        
        # Clear state
        AdapterRegistry.clear()
        
        # Run initialization sequence
        initialize_adapters()
        config_manager = initialize_config()
        initialize_logging()
        
        # Verify all systems are operational
        
        # 1. Adapters
        available_adapters = AdapterRegistry.list_available()
        assert "duckduckgo" in available_adapters
        
        # 2. Configuration
        assert config_manager.get("general.engine") == "duckduckgo"
        
        # 3. Logging
        logger = logging.getLogger("mudhound")
        assert logger is not None
        logger.info("Integration test complete")
    
    @patch('mudhound.cli.app.app')
    def test_main_entry_point_flow(self, mock_app):
        """Test that main entry point calls app correctly."""
        from mudhound.__main__ import main
        
        # Clear state
        AdapterRegistry.clear()
        
        # Run main (will call mocked app)
        try:
            main()
        except SystemExit:
            pass  # Expected if app exits
        
        # Verify app was called
        mock_app.assert_called_once()
        
        # Verify adapters were initialized
        available = AdapterRegistry.list_available()
        assert "duckduckgo" in available


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
