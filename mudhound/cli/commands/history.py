"""
History command for MudHound CLI.

Provides functionality to manage search history:
- list: Display recent search sessions
- show: Display full results for a specific session
- replay: Re-execute a search with original parameters
- delete: Delete a specific search session
- clear: Delete all search history
"""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from mudhound.core.store import ResultStore, StoreError
from mudhound.core.engine import SearchEngine
from mudhound.core.result import SearchOptions
from mudhound.adapters.registry import AdapterRegistry
from mudhound.core.exceptions import MudHoundError


app = typer.Typer(help="Manage search history")
console = Console()
console_err = Console(stderr=True)


def get_result_store(ctx: typer.Context) -> ResultStore:
    """Get or create a ResultStore instance.
    
    Args:
        ctx: Typer context containing global options
        
    Returns:
        ResultStore instance
    """
    # For now, use default location
    # Could be extended to support custom db path from config
    return ResultStore()


@app.command()
def list(
    ctx: typer.Context,
    limit: int = typer.Option(20, "--limit", "-n", help="Maximum number of sessions to display"),
):
    """
    List recent search sessions.
    
    Displays a table of recent searches with ID, query, result count,
    status, and timestamp.
    """
    from mudhound.cli.validation import validate_limit
    
    # Validate limit
    is_valid, error = validate_limit(limit)
    if not is_valid:
        console_err.print(f"[red]Validation Error:[/red] {error}")
        console_err.print("[yellow]Tip:[/yellow] Limit must be between 1 and 10000")
        raise typer.Exit(1)
    
    try:
        store = get_result_store(ctx)
        sessions = store.list(limit=limit)
        
        if not sessions:
            console.print("[yellow]No search history found[/yellow]")
            return
        
        # Create a table for display
        table = Table(title="Search History", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Query", style="green")
        table.add_column("Engine", style="blue")
        table.add_column("Results", justify="right", style="yellow")
        table.add_column("Status", style="white")
        table.add_column("Duration", justify="right", style="dim")
        table.add_column("Timestamp", style="dim")
        
        for session in sessions:
            # Format duration
            duration_str = ""
            if session["duration"] is not None:
                duration_str = f"{session['duration']:.2f}s"
            
            # Format timestamp (just the date and time, not microseconds)
            timestamp = session["started_at"]
            if "T" in timestamp:
                timestamp = timestamp.split("T")[0] + " " + timestamp.split("T")[1].split(".")[0]
            
            # Truncate query if too long
            query = session["query"]
            if len(query) > 40:
                query = query[:37] + "..."
            
            # Color code status
            status = session["status"]
            if status == "COMPLETE":
                status_display = f"[green]{status}[/green]"
            elif status == "FAILED":
                status_display = f"[red]{status}[/red]"
            elif status == "CANCELLED":
                status_display = f"[yellow]{status}[/yellow]"
            else:
                status_display = status
            
            # Truncate ID for display
            id_display = session["id"][:8]
            
            table.add_row(
                id_display,
                query,
                session["engine"],
                str(session["result_count"]),
                status_display,
                duration_str,
                timestamp,
            )
        
        console.print(table)
        console.print(f"\n[dim]Showing {len(sessions)} of {len(sessions)} sessions[/dim]")
        console.print(f"[dim]Use 'mh history show <id>' to view full results[/dim]")
        
    except StoreError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def show(
    ctx: typer.Context,
    session_id: str = typer.Argument(..., help="Session ID to display (can use short ID)"),
):
    """
    Display full results for a specific search session.
    
    Shows all details including query parameters, results, and metadata.
    """
    # Validate session_id is not empty
    if not session_id or len(session_id.strip()) == 0:
        console_err.print("[red]Error:[/red] Session ID cannot be empty")
        console_err.print("[yellow]Tip:[/yellow] Use 'mh history list' to see available sessions")
        raise typer.Exit(1)
    
    try:
        store = get_result_store(ctx)
        
        # Try to find session by full or partial ID
        session = None
        if len(session_id) < 36:  # Short ID provided
            # List all sessions and find matching one
            all_sessions = store.list(limit=1000)
            matching = [s for s in all_sessions if s["id"].startswith(session_id)]
            
            if not matching:
                console_err.print(f"[red]Error:[/red] No session found with ID starting with '{session_id}'")
                raise typer.Exit(1)
            elif len(matching) > 1:
                console_err.print(f"[red]Error:[/red] Ambiguous ID '{session_id}' matches multiple sessions:")
                for s in matching:
                    console_err.print(f"  - {s['id'][:8]}: {s['query']}")
                raise typer.Exit(1)
            
            session_id = matching[0]["id"]
        
        session = store.show(session_id)
        
        if session is None:
            console_err.print(f"[red]Error:[/red] Session not found: {session_id}")
            raise typer.Exit(1)
        
        # Display session header
        console.print(f"\n[bold cyan]Search Session:[/bold cyan] {session.query.id[:8]}")
        console.print(f"[bold]Query:[/bold] {session.query.query}")
        console.print(f"[bold]Engine:[/bold] {session.query.engine}")
        console.print(f"[bold]Status:[/bold] {session.query.status.value}")
        console.print(f"[bold]Started:[/bold] {session.started_at}")
        if session.completed_at:
            console.print(f"[bold]Completed:[/bold] {session.completed_at}")
        if session.duration:
            console.print(f"[bold]Duration:[/bold] {session.duration:.2f}s")
        console.print(f"[bold]Results:[/bold] {session.result_count}")
        
        # Display options
        console.print(f"\n[bold]Search Options:[/bold]")
        console.print(f"  Max Results: {session.query.options.max_results}")
        console.print(f"  Region: {session.query.options.region}")
        console.print(f"  Safe Search: {session.query.options.safesearch}")
        if session.query.options.time_limit:
            console.print(f"  Time Limit: {session.query.options.time_limit}")
        
        # Display error if present
        if session.error:
            console.print(f"\n[bold red]Error:[/bold red] {session.error}")
        
        # Display results
        if session.results:
            console.print(f"\n[bold]Results:[/bold]")
            
            # Create results table
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Rank", justify="right", style="cyan", width=4)
            table.add_column("Title", style="green")
            table.add_column("URL", style="blue")
            table.add_column("Source", style="yellow", width=15)
            
            for result in session.results:
                # Truncate title and URL for display
                title = result.title
                if len(title) > 50:
                    title = title[:47] + "..."
                
                url = result.url
                if len(url) > 60:
                    url = url[:57] + "..."
                
                table.add_row(
                    str(result.rank),
                    title,
                    url,
                    result.source,
                )
            
            console.print(table)
        
    except StoreError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def replay(
    ctx: typer.Context,
    session_id: str = typer.Argument(..., help="Session ID to replay (can use short ID)"),
):
    """
    Re-execute a search with original parameters.
    
    Retrieves the original query and options from history and executes
    a new search with the same parameters.
    """
    # Validate session_id is not empty
    if not session_id or len(session_id.strip()) == 0:
        console_err.print("[red]Error:[/red] Session ID cannot be empty")
        console_err.print("[yellow]Tip:[/yellow] Use 'mh history list' to see available sessions")
        raise typer.Exit(1)
    
    try:
        store = get_result_store(ctx)
        
        # Try to find session by full or partial ID
        if len(session_id) < 36:  # Short ID provided
            # List all sessions and find matching one
            all_sessions = store.list(limit=1000)
            matching = [s for s in all_sessions if s["id"].startswith(session_id)]
            
            if not matching:
                console_err.print(f"[red]Error:[/red] No session found with ID starting with '{session_id}'")
                raise typer.Exit(1)
            elif len(matching) > 1:
                console_err.print(f"[red]Error:[/red] Ambiguous ID '{session_id}' matches multiple sessions:")
                for s in matching:
                    console_err.print(f"  - {s['id'][:8]}: {s['query']}")
                raise typer.Exit(1)
            
            session_id = matching[0]["id"]
        
        # Get replay parameters
        params = store.replay(session_id)
        
        if params is None:
            console_err.print(f"[red]Error:[/red] Session not found: {session_id}")
            raise typer.Exit(1)
        
        console.print(f"[cyan]Replaying search:[/cyan] {params['query']}")
        console.print(f"[dim]Engine: {params['engine']}[/dim]")
        console.print(f"[dim]Options: {params['options']}[/dim]")
        console.print()
        
        # Create search options
        options_dict = params["options"]
        options = SearchOptions(
            max_results=options_dict["max_results"],
            region=options_dict["region"],
            safesearch=options_dict["safesearch"],
            time_limit=options_dict.get("time_limit"),
        )
        
        # Create search engine with the specified adapter
        try:
            engine = SearchEngine(adapter_name=params["engine"])
        except Exception as e:
            console_err.print(f"[red]Error:[/red] Failed to initialize search engine: {e}")
            raise typer.Exit(1)
        
        # Execute search
        console.print("[yellow]Executing search...[/yellow]")
        
        try:
            session = engine.search(
                query=params["query"],
                options=options,
                progress_callback=lambda result: console.print(f"  [{result.rank}] {result.title}"),
            )
            
            # Persist the new session
            store.persist(session)
            
            console.print(f"\n[green]✓[/green] Search completed: {session.result_count} results in {session.duration:.2f}s")
            console.print(f"[dim]New session ID: {session.query.id[:8]}[/dim]")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Search cancelled by user[/yellow]")
            raise typer.Exit(130)
        except MudHoundError as e:
            console_err.print(f"\n[red]Error:[/red] {e}")
            raise typer.Exit(1)
        
    except StoreError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def delete(
    ctx: typer.Context,
    session_id: str = typer.Argument(..., help="Session ID to delete (can use short ID)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """
    Delete a specific search session.
    
    Removes the session and all associated results from history.
    Requires confirmation unless --yes flag is provided.
    """
    # Validate session_id is not empty
    if not session_id or len(session_id.strip()) == 0:
        console_err.print("[red]Error:[/red] Session ID cannot be empty")
        console_err.print("[yellow]Tip:[/yellow] Use 'mh history list' to see available sessions")
        raise typer.Exit(1)
    
    try:
        store = get_result_store(ctx)
        
        # Try to find session by full or partial ID
        full_session_id = session_id
        if len(session_id) < 36:  # Short ID provided
            # List all sessions and find matching one
            all_sessions = store.list(limit=1000)
            matching = [s for s in all_sessions if s["id"].startswith(session_id)]
            
            if not matching:
                console_err.print(f"[red]Error:[/red] No session found with ID starting with '{session_id}'")
                raise typer.Exit(1)
            elif len(matching) > 1:
                console_err.print(f"[red]Error:[/red] Ambiguous ID '{session_id}' matches multiple sessions:")
                for s in matching:
                    console_err.print(f"  - {s['id'][:8]}: {s['query']}")
                raise typer.Exit(1)
            
            full_session_id = matching[0]["id"]
            
            # Show what we're about to delete
            console.print(f"[yellow]Session:[/yellow] {matching[0]['query']}")
        
        # Confirm destructive action
        if not yes:
            confirm = typer.confirm(
                f"Delete session {session_id}?",
                default=False
            )
            if not confirm:
                console.print("[yellow]Delete cancelled[/yellow]")
                raise typer.Exit(0)
        
        # Delete the session
        deleted = store.delete(full_session_id)
        
        if deleted:
            console.print(f"[green]✓[/green] Session deleted: {session_id}")
        else:
            console_err.print(f"[red]Error:[/red] Session not found: {session_id}")
            raise typer.Exit(1)
        
    except StoreError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def clear(
    ctx: typer.Context,
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """
    Delete all search history.
    
    Removes all sessions and results from the history database.
    This action cannot be undone. Requires confirmation unless --yes flag is provided.
    """
    try:
        store = get_result_store(ctx)
        
        # Confirm destructive action
        if not yes:
            confirm = typer.confirm(
                "This will delete ALL search history. Are you sure?",
                default=False
            )
            if not confirm:
                console.print("[yellow]Clear cancelled[/yellow]")
                raise typer.Exit(0)
        
        # Clear all history
        count = store.clear()
        
        console.print(f"[green]✓[/green] Cleared {count} session(s) from history")
        
    except StoreError as e:
        console_err.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
