"""
Main CLI application using Typer.
"""

import typer
from typing import Optional

from mudhound.cli.commands import config as config_cmd
from mudhound.cli.commands import history as history_cmd
from mudhound.cli.commands import interactive as interactive_cmd

app = typer.Typer(
    name="mudhound",
    help="Terminal-based batch URL extraction tool",
    add_completion=False,
)

# Register subcommands
app.add_typer(config_cmd.app, name="config")
app.add_typer(history_cmd.app, name="history")


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
    interactive_cmd.interactive_command(
        use_color=not no_color,
        use_animation=not no_animation
    )


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
    # Store global options in context for use by commands
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["no_color"] = no_color
    ctx.obj["no_animation"] = no_animation
    ctx.obj["theme"] = theme
    ctx.obj["config"] = config


@app.command()
def version():
    """Display version information."""
    from mudhound import __version__
    typer.echo(f"MudHound version {__version__}")


if __name__ == "__main__":
    app()
