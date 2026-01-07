"""
Main CLI application using Typer.

This module defines the main CLI application structure and global options.
It integrates with the configuration and logging systems initialized in __main__.py.
"""

import logging
from pathlib import Path
from typing import Optional

import typer

from mudhound.cli.commands import config as config_cmd
from mudhound.cli.commands import export as export_cmd
from mudhound.cli.commands import history as history_cmd
from mudhound.cli.commands import interactive as interactive_cmd
from mudhound.cli.commands import search as search_cmd
from mudhound.core.config import ConfigManager

app = typer.Typer(
    name="mudhound",
    help="Terminal-based batch URL extraction tool",
    add_completion=False,
)

# Register subcommands
app.add_typer(config_cmd.app, name="config")
app.add_typer(history_cmd.app, name="history")
app.add_typer(export_cmd.app, name="export")

# Register search command (primary command)
app.command()(search_cmd.search)


@app.command()
def interactive(
    ctx: typer.Context,
):
    """
    Launch interactive mode with menu-driven interface.

    Interactive mode allows you to perform multiple operations
    (search, history, export, config) without re-launching the application.
    """
    # Get global options from context
    no_color = ctx.obj.get("no_color", False) if ctx.obj else False
    no_animation = ctx.obj.get("no_animation", False) if ctx.obj else False

    # Run interactive mode
    interactive_cmd.interactive_command(use_color=not no_color, use_animation=not no_animation)


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress non-essential output"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output"),
    no_animation: bool = typer.Option(False, "--no-animation", help="Disable animations"),
    theme: Optional[str] = typer.Option(None, "--theme", help="Theme to use"),
    config: Optional[str] = typer.Option(None, "--config", help="Path to config file"),
):
    """
    MudHound - Terminal-based batch URL extraction tool.

    A modular search tool with animated UI and multiple search engine support.
    """
    # Validate conflicting options
    if verbose and quiet:
        typer.echo("Error: Cannot use both --verbose and --quiet options", err=True)
        raise typer.Exit(1)

    # Validate config path if provided
    if config:
        config_path = Path(config)
        # Check if path exists
        if config_path.exists():
            # If it exists, it must be a file
            if not config_path.is_file():
                typer.echo(f"Error: Config path is not a file: {config}", err=True)
                raise typer.Exit(1)
        else:
            # If it doesn't exist, check if parent directory exists
            # This allows creating new config files but catches typos in paths
            if not config_path.parent.exists():
                typer.echo(f"Error: Config file not found: {config}", err=True)
                typer.echo("Tip: Check the file path and try again", err=True)
                raise typer.Exit(1)

    # Reconfigure logging based on CLI arguments
    from mudhound.logging import configure_logging

    # Determine log level
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    # Reconfigure logging with CLI options
    log_file = Path.home() / ".mudhound" / "logs" / "mudhound.log"
    configure_logging(
        level=level,
        use_color=not no_color,
        log_file=log_file if not quiet else None,
        file_level=logging.DEBUG,
    )

    # Load or reload configuration with CLI override
    config_manager = ConfigManager(cli_config_path=config)

    # Store global options in context for use by commands
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["no_color"] = no_color
    ctx.obj["no_animation"] = no_animation
    ctx.obj["theme"] = theme
    ctx.obj["config"] = config
    ctx.obj["config_manager"] = config_manager

    # Get logger
    logger = logging.getLogger("mudhound")
    logger.debug(
        f"MudHound starting with options: verbose={verbose}, quiet={quiet}, no_color={no_color}, no_animation={no_animation}"
    )

    if config:
        logger.debug(f"Using config file: {config}")

    # Log available adapters
    from mudhound.adapters.registry import AdapterRegistry

    available_adapters = AdapterRegistry.list_available()
    logger.debug(f"Available search adapters: {', '.join(available_adapters)}")


@app.command()
def version():
    """Display version information."""
    from mudhound import __version__

    typer.echo(f"MudHound version {__version__}")


if __name__ == "__main__":
    app()
