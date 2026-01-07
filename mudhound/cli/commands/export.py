"""
Export command for MudHound CLI.

Provides functionality to export search results in multiple formats:
- JSON: Structured data with all fields
- CSV: Tabular format with headers
- TXT: Human-readable formatted text
- URLs: Simple list of URLs (one per line)
"""

import csv
import json
from pathlib import Path
from typing import List, Optional

import typer

from mudhound.core.exceptions import ExportError
from mudhound.core.result import SearchResult

app = typer.Typer(help="Export search results to various formats")


def export_json(results: List[SearchResult], output_path: Path) -> None:
    """Export results to JSON format.

    Args:
        results: List of search results to export
        output_path: Path to write the JSON file

    Raises:
        ExportError: If file writing fails
    """
    try:
        data = [
            {
                "url": result.url,
                "title": result.title,
                "snippet": result.snippet,
                "source": result.source,
                "rank": result.rank,
                "metadata": result.metadata,
            }
            for result in results
        ]

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    except OSError as e:
        raise ExportError(f"Failed to write JSON file: {e}")


def export_csv(results: List[SearchResult], output_path: Path) -> None:
    """Export results to CSV format.

    Args:
        results: List of search results to export
        output_path: Path to write the CSV file

    Raises:
        ExportError: If file writing fails
    """
    try:
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["rank", "url", "title", "snippet", "source"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for result in results:
                writer.writerow(
                    {
                        "rank": result.rank,
                        "url": result.url,
                        "title": result.title,
                        "snippet": result.snippet,
                        "source": result.source,
                    }
                )

    except OSError as e:
        raise ExportError(f"Failed to write CSV file: {e}")


def export_txt(results: List[SearchResult], output_path: Path) -> None:
    """Export results to formatted text.

    Args:
        results: List of search results to export
        output_path: Path to write the text file

    Raises:
        ExportError: If file writing fails
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for result in results:
                f.write(f"[{result.rank}] {result.title}\n")
                f.write(f"URL: {result.url}\n")
                f.write(f"Source: {result.source}\n")
                f.write(f"Snippet: {result.snippet}\n")
                f.write("\n" + "-" * 80 + "\n\n")

    except OSError as e:
        raise ExportError(f"Failed to write TXT file: {e}")


def export_urls(results: List[SearchResult], output_path: Path) -> None:
    """Export URLs only (one per line).

    Args:
        results: List of search results to export
        output_path: Path to write the URLs file

    Raises:
        ExportError: If file writing fails
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for result in results:
                f.write(f"{result.url}\n")

    except OSError as e:
        raise ExportError(f"Failed to write URLs file: {e}")


@app.command()
def export(
    session_id: Optional[str] = typer.Argument(
        None, help="Session ID to export (uses last session if not provided)"
    ),
    output: str = typer.Option(..., "--output", "-o", help="Output file path"),
    format: str = typer.Option(
        "json", "--format", "-f", help="Export format: json, csv, txt, urls"
    ),
):
    """
    Export search results to a file.

    Supports multiple output formats:
    - json: Structured JSON with all fields
    - csv: Comma-separated values with headers
    - txt: Human-readable formatted text
    - urls: Simple list of URLs (one per line)
    """
    from rich.console import Console

    from mudhound.cli.validation import validate_format, validate_output_path

    console_err = Console(stderr=True)

    # Validate arguments
    errors = []

    # Validate format
    is_valid_format, format_error = validate_format(format)
    if not is_valid_format:
        errors.append(format_error)

    # Validate output path
    is_valid_output, output_error = validate_output_path(output)
    if not is_valid_output:
        errors.append(output_error)

    # If there are validation errors, display them and exit
    if errors:
        console_err.print("[red]Validation Error(s):[/red]")
        for error in errors:
            console_err.print(f"  • {error}")
        console_err.print("\n[yellow]Tip:[/yellow] Use --help to see valid options")
        raise typer.Exit(1)

    # This is a placeholder - actual implementation would retrieve session from store
    # For now, we'll focus on the export functions themselves
    typer.echo(f"Exporting session {session_id or 'latest'} to {output} as {format}")

    typer.echo("Export functionality will be wired up with search engine in task 38")


if __name__ == "__main__":
    app()
