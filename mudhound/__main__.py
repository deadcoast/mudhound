"""
Entry point for running MudHound as a module: python -m mudhound
"""

import sys


def main():
    """Main entry point for the MudHound application."""
    # Import here to avoid circular imports and allow lazy loading
    from mudhound.cli.app import app
    
    try:
        app()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
