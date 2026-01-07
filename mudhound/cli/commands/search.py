"""
Search command for MudHound CLI.

Provides the primary search functionality via the command line.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from mudhound.adapters.registry import AdapterRegistry
from mudhound.cli.commands.export import (
    export_csv,
    export_json,
    export_txt,
    export_urls,
)
from mudhound.cli.validation import (
    validate_engine,
    validate_format,
    validate_max_results,
    validate_output_path,
)
from mudhound.core.engine import SearchEngine
from mudhound.core.exceptions import MudHoundError
from mudhound.core.result import SearchOptions
from mudhound.core.store import ResultStore
from mudhound.ui.components.error import ErrorHandler
from mudhound.ui.components.progress import Progress, ProgressVariant
from mudhound.ui.components.table import Table
from mudhound.ui.layout import LayoutManager
from mudhound.ui.renderer import UIRenderer

app = typer.Typer(help="Search for URLs using various search engines")

logger = logging.getLogger("mudhound.cli.search")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    max_results: int = typer.Option(
        50, "--max", "-m", help="Maximum number of results"),
    engine: str = typer.Option(
        "duckduckgo", "--engine", "-e", help="Search engine adapter"),
    region: str = typer.Option("wt-wt", "--region", "-r", help="Region code"),
    safesearch: str = typer.Option(
        "moderate", "--safesearch", "-s", help="Safe search level (off|moderate|strict)"
    ),
    time_limit: Optional[str] = typer.Option(
        None, "--time", "-t", help="Time filter (d|w|m|y)"),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file path"),
    format: str = typer.Option(
        "json", "--format", "-f", help="Output format (json|csv|txt|urls)"),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Suppress UI, output only"),
    interactive_results: bool = typer.Option(
        False, "--interactive", "-i", help="Interactive results with navigation"
    ),
):
    """
    Execute a search query and display results.

    Examples:
        mh search "python libraries"
        mh search "machine learning" --max 100 --region us-en
        mh search "cybersecurity" --output results.json --format json
        mh search "python tutorials" --interactive
    """
    console = Console()
    console_err = Console(stderr=True)
    error_handler = ErrorHandler(verbose=False)

    # Validate arguments
    errors = []

    is_valid_max, max_error = validate_max_results(max_results)
    if not is_valid_max:
        errors.append(max_error)

    is_valid_engine, engine_error = validate_engine(engine)
    if not is_valid_engine:
        errors.append(engine_error)

    if output:
        is_valid_format, format_error = validate_format(format)
        if not is_valid_format:
            errors.append(format_error)

        is_valid_output, output_error = validate_output_path(output)
        if not is_valid_output:
            errors.append(output_error)

    # Validate safesearch
    valid_safesearch = ["off", "moderate", "strict"]
    if safesearch.lower() not in valid_safesearch:
        errors.append(
            f"Invalid safesearch value: {safesearch}. Must be one of: {', '.join(valid_safesearch)}"
        )

    # Validate time_limit
    if time_limit:
        valid_time = ["d", "w", "m", "y"]
        if time_limit.lower() not in valid_time:
            errors.append(
                f"Invalid time filter: {time_limit}. Must be one of: {', '.join(valid_time)}"
            )

    if errors:
        console_err.print("[red]Validation Error(s):[/red]")
        for error in errors:
            console_err.print(f"  [red]•[/red] {error}")
        console_err.print(
            "\n[yellow]Tip:[/yellow] Use --help to see valid options")
        raise typer.Exit(1)

    # Initialize search engine
    try:
        adapter_class = AdapterRegistry.get(engine)
        adapter = adapter_class()
        search_engine = SearchEngine(adapter=adapter)
    except MudHoundError as e:
        if not quiet:
            console_err.print(error_handler.format_error(e))
        else:
            console_err.print(f"Error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        console_err.print(f"[red]Error initializing search engine:[/red] {e}")
        raise typer.Exit(1)

    # Create search options
    options = SearchOptions(
        max_results=max_results,
        region=region,
        safesearch=safesearch,
        time_limit=time_limit,
    )

    # Execute search
    if not quiet:
        # Use UIRenderer with LayoutManager for structured display
        layout_manager = LayoutManager()
        ui_renderer = UIRenderer(layout_manager=layout_manager)

        # Render search info in a frame
        search_info = [
            f"Query: {query}",
            f"Engine: {engine} | Max: {max_results} | Region: {region}",
        ]
        ui_renderer.render_and_flush(
            content=search_info, title="Search", apply_theme=True)
        console.print()

    # Initialize progress component
    progress = Progress(
        variant=ProgressVariant.SPINNER,
        total=max_results,
        use_color=True,
        output=sys.stdout,
    )

    try:
        if not quiet:
            progress.start()

        def progress_callback(result):
            if not quiet:
                progress.update()

        session = search_engine.search(
            query=query,
            options=options,
            progress_callback=progress_callback if not quiet else None,
        )

        if not quiet:
            progress.complete("Search complete")
            console.print()

        # Display results based on mode
        if not quiet:
            if interactive_results and session.results:
                # Use custom Table component for interactive navigation
                table = Table(
                    results=session.results,
                    use_color=True,
                    page_size=10,
                )
                console.print(
                    "[dim]Interactive mode: Navigate with j/k, filter with /, select with Enter[/dim]\n"
                )
                selected = table.show_interactive()
                if selected:
                    console.print(f"\n[green]Selected:[/green] {selected.url}")
            else:
                # Standard display
                for result in session.results[:10]:
                    console.print(
                        f"[bold cyan][{result.rank}][/bold cyan] {result.title}")
                    console.print(
                        f"    [link={result.url}]{result.url}[/link]")
                    snippet = (
                        result.snippet[:150] + "..."
                        if len(result.snippet) > 150
                        else result.snippet
                    )
                    console.print(f"    [dim]{snippet}[/dim]\n")

                if len(session.results) > 10:
                    console.print(
                        f"[dim]... and {len(session.results) - 10} more results[/dim]\n")

        # Save to history
        store = ResultStore()
        store.persist(session)

        if not quiet:
            console.print(
                f"[dim]Search saved to history (ID: {session.query.id[:8]}...)[/dim]")

        # Export if output path provided
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            format_lower = format.lower()
            if format_lower == "json":
                export_json(session.results, output_path)
            elif format_lower == "csv":
                export_csv(session.results, output_path)
            elif format_lower == "txt":
                export_txt(session.results, output_path)
            elif format_lower == "urls":
                export_urls(session.results, output_path)

            if not quiet:
                console.print(f"[green]Results exported to:[/green] {output}")

        # In quiet mode, just output the URLs
        if quiet and not output:
            for result in session.results:
                typer.echo(result.url)

    except KeyboardInterrupt:
        if not quiet:
            progress.cancel("Search cancelled by user")
        else:
            console.print("\nCancelled")
        raise typer.Exit(130)
    except MudHoundError as e:
        if not quiet:
            progress.error(str(e))
            console_err.print(error_handler.format_error(e))
        else:
            console_err.print(f"Error: {e}")
        logger.exception("Search failed")
        raise typer.Exit(1)
    except Exception as e:
        if not quiet:
            progress.error(str(e))
        console_err.print(f"[red]Search error:[/red] {e}")
        logger.exception("Search failed")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
