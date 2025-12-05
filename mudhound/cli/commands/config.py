"""
Config command for MudHound CLI.

Provides functionality to manage application configuration:
- list: Display all configuration keys and values
- get: Retrieve a specific configuration value
- set: Update a configuration value
- reset: Reset configuration to defaults
- edit: Open configuration file in $EDITOR
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from mudhound.core.config import ConfigManager
from mudhound.core.exceptions import ConfigError


app = typer.Typer(help="Manage MudHound configuration")
console = Console()
console_err = Console(stderr=True)


def get_config_manager(ctx: typer.Context) -> ConfigManager:
    """Get or create a ConfigManager instance.
    
    Args:
        ctx: Typer context containing global options
        
    Returns:
        ConfigManager instance
    """
    # Get config path from global options if available
    config_path = None
    if ctx.parent and ctx.parent.obj:
        config_path = ctx.parent.obj.get("config")
    
    return ConfigManager(cli_config_path=config_path)


@app.command()
def list(ctx: typer.Context):
    """
    List all configuration keys and values.
    
    Displays the complete configuration in a formatted table.
    """
    try:
        config_manager = get_config_manager(ctx)
        config_dict = config_manager.list()
        
        # Create a table for display
        table = Table(title="MudHound Configuration", show_header=True, header_style="bold magenta")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        
        # Flatten nested config for display
        def flatten_dict(d, parent_key=""):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key))
                else:
                    items.append((new_key, str(v)))
            return items
        
        flattened = flatten_dict(config_dict)
        for key, value in sorted(flattened):
            table.add_row(key, value)
        
        console.print(table)
        
        # Show config file location
        if config_manager.config_path:
            console.print(f"\n[dim]Configuration loaded from: {config_manager.config_path}[/dim]")
        else:
            console.print("\n[dim]Using default configuration (no config file found)[/dim]")
            
    except ConfigError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def get(
    ctx: typer.Context,
    key: str = typer.Argument(..., help="Configuration key (supports dot notation, e.g., 'general.engine')"),
):
    """
    Get a specific configuration value.
    
    Supports dot notation for nested keys (e.g., 'general.engine').
    """
    # Validate key is not empty
    if not key or len(key.strip()) == 0:
        console_err.print("[red]Error:[/red] Configuration key cannot be empty")
        console_err.print("[yellow]Tip:[/yellow] Use 'mh config list' to see all available keys")
        raise typer.Exit(1)
    
    try:
        config_manager = get_config_manager(ctx)
        value = config_manager.get(key)
        
        if value is None:
            console_err.print(f"[yellow]Warning:[/yellow] Key '{key}' not found in configuration")
            raise typer.Exit(1)
        
        # Format output based on value type
        if isinstance(value, dict):
            console.print(f"[cyan]{key}[/cyan]:")
            for k, v in value.items():
                console.print(f"  {k}: {v}")
        else:
            console.print(f"[cyan]{key}[/cyan]: {value}")
            
    except ConfigError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def set(
    ctx: typer.Context,
    key: str = typer.Argument(..., help="Configuration key (supports dot notation)"),
    value: str = typer.Argument(..., help="Value to set"),
):
    """
    Set a configuration value.
    
    Supports dot notation for nested keys (e.g., 'general.engine').
    Creates intermediate dictionaries as needed.
    The configuration is persisted to disk after setting.
    """
    # Validate key is not empty
    if not key or len(key.strip()) == 0:
        console_err.print("[red]Error:[/red] Configuration key cannot be empty")
        console_err.print("[yellow]Tip:[/yellow] Use 'mh config list' to see all available keys")
        raise typer.Exit(1)
    
    # Validate value is not empty
    if not value or len(value.strip()) == 0:
        console_err.print("[red]Error:[/red] Configuration value cannot be empty")
        raise typer.Exit(1)
    
    try:
        config_manager = get_config_manager(ctx)
        
        # Try to parse value as appropriate type
        parsed_value = _parse_value(value)
        
        # Set the value
        config_manager.set(key, parsed_value)
        
        # Save to disk
        config_manager.save()
        
        console.print(f"[green]✓[/green] Set [cyan]{key}[/cyan] = {parsed_value}")
        
        if config_manager.config_path:
            console.print(f"[dim]Configuration saved to: {config_manager.config_path}[/dim]")
        
    except ConfigError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def reset(
    ctx: typer.Context,
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """
    Reset configuration to defaults.
    
    This will discard all custom settings and restore the default configuration.
    Requires confirmation unless --yes flag is provided.
    """
    try:
        config_manager = get_config_manager(ctx)
        
        # Confirm destructive action
        if not yes:
            confirm = typer.confirm(
                "This will reset all configuration to defaults. Are you sure?",
                default=False
            )
            if not confirm:
                console.print("[yellow]Reset cancelled[/yellow]")
                raise typer.Exit(0)
        
        # Reset to defaults
        config_manager.reset()
        
        # Save the defaults to disk
        config_manager.save()
        
        console.print("[green]✓[/green] Configuration reset to defaults")
        
        if config_manager.config_path:
            console.print(f"[dim]Configuration saved to: {config_manager.config_path}[/dim]")
            
    except ConfigError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def edit(ctx: typer.Context):
    """
    Open configuration file in $EDITOR.
    
    Opens the configuration file in the editor specified by the EDITOR
    environment variable. Falls back to 'nano' on Unix or 'notepad' on Windows
    if EDITOR is not set.
    
    If no configuration file exists, creates one at the default location.
    """
    try:
        config_manager = get_config_manager(ctx)
        
        # Ensure config file exists
        if config_manager.config_path is None:
            # Create default config file
            config_manager.save()
            console.print(f"[green]✓[/green] Created configuration file at: {config_manager.config_path}")
        
        config_path = config_manager.config_path
        
        # Get editor from environment
        editor = os.environ.get("EDITOR")
        
        if not editor:
            # Fall back to platform defaults
            if sys.platform == "win32":
                editor = "notepad"
            else:
                editor = "nano"
        
        console.print(f"[dim]Opening {config_path} in {editor}...[/dim]")
        
        # Open editor
        try:
            subprocess.run([editor, str(config_path)], check=True)
            console.print("[green]✓[/green] Configuration file closed")
        except subprocess.CalledProcessError as e:
            console_err.print(f"[red]Error:[/red] Editor exited with error code {e.returncode}")
            raise typer.Exit(1)
        except FileNotFoundError:
            console_err.print(f"[red]Error:[/red] Editor '{editor}' not found")
            console_err.print("[yellow]Tip:[/yellow] Set the EDITOR environment variable to your preferred editor")
            raise typer.Exit(1)
            
    except ConfigError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


def _parse_value(value: str):
    """Parse a string value to appropriate Python type.
    
    Attempts to parse as:
    - boolean (true/false, yes/no, on/off)
    - integer
    - float
    - string (fallback)
    
    Args:
        value: String value to parse
        
    Returns:
        Parsed value in appropriate type
    """
    # Boolean values
    if value.lower() in ("true", "yes", "on", "1"):
        return True
    if value.lower() in ("false", "no", "off", "0"):
        return False
    
    # Try integer
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    
    # Return as string
    return value


if __name__ == "__main__":
    app()
