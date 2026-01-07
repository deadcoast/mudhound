"""
Entry point for running MudHound as a module: python -m mudhound

This module serves as the main entry point for the MudHound application.
It performs critical initialization tasks:
- Checks terminal size adequacy
- Registers search engine adapters
- Initializes the configuration system
- Sets up the logging system
- Launches the CLI application
"""

import sys
import logging
from pathlib import Path

from mudhound.utils.terminal import is_terminal_size_adequate, get_terminal_size


def check_terminal_size():
    """Check if terminal meets minimum size requirements.

    Displays a warning if the terminal is too small for optimal display.
    Does not block execution to support scripted/piped usage.

    Returns:
        bool: True if terminal size is adequate
    """
    MIN_WIDTH = 60
    MIN_HEIGHT = 10

    if not is_terminal_size_adequate(MIN_WIDTH, MIN_HEIGHT):
        width, height = get_terminal_size()
        sys.stderr.write(
            f"\033[33mWarning:\033[0m Terminal size ({width}x{height}) is below "
            f"recommended minimum ({MIN_WIDTH}x{MIN_HEIGHT}).\n"
            "Some UI elements may not display correctly.\n\n"
        )
        return False
    return True


def initialize_adapters():
    """Initialize and register all search engine adapters.

    This function discovers and registers adapters from:
    - Built-in adapters (DuckDuckGo, etc.)
    - Plugin packages (mudhound_adapter_*)
    - User adapters (~/.mudhound/adapters/)
    """
    from mudhound.adapters.registry import AdapterRegistry

    # Discover and register all adapters
    AdapterRegistry.discover_all()


def initialize_logging(verbose: bool = False, quiet: bool = False, use_color: bool = True):
    """Initialize the logging system.
    
    Args:
        verbose: Enable verbose (DEBUG) logging
        quiet: Suppress most logging output
        use_color: Enable colored log output
    """
    from mudhound.logging import configure_logging
    from mudhound.logging.levels import TRACE
    
    # Determine log level
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    # Get log file path from config or use default
    log_file = Path.home() / '.mudhound' / 'logs' / 'mudhound.log'
    
    # Configure logging
    configure_logging(
        level=level,
        use_color=use_color,
        log_file=log_file if not quiet else None,
        file_level=logging.DEBUG,  # Always log DEBUG to file
    )


def initialize_config(config_path: str = None):
    """Initialize the configuration system.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        ConfigManager instance
    """
    from mudhound.core.config import ConfigManager
    
    # Create config manager with optional CLI override
    config_manager = ConfigManager(cli_config_path=config_path)
    
    return config_manager


def main():
    """Main entry point for the MudHound application.

    This function:
    1. Checks terminal size adequacy
    2. Initializes all system components (adapters, config, logging)
    3. Launches the CLI application
    4. Handles top-level exceptions and signals
    """
    try:
        # Check terminal size (warns but doesn't block)
        check_terminal_size()

        # Initialize adapters first (no dependencies)
        initialize_adapters()

        # Initialize configuration system
        # Note: Actual config values will be loaded by CLI app based on arguments
        config_manager = initialize_config()

        # Initialize logging with defaults
        # Note: CLI app will reconfigure based on command-line arguments
        initialize_logging()

        # Import and run CLI app
        # Import here to avoid circular imports and allow lazy loading
        from mudhound.cli.app import app

        app()
        
    except KeyboardInterrupt:
        # Handle CTRL+C gracefully
        print("\n\nOperation cancelled by user.")
        sys.exit(130)  # Standard exit code for SIGINT
        
    except Exception as e:
        # Handle unexpected errors
        logger = logging.getLogger("mudhound")
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
