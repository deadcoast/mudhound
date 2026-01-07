"""
Interactive mode command for MudHound.

This module provides an interactive TUI mode where users can perform
multiple operations without re-launching the application.
"""

import sys
from typing import Any, Dict, Optional

from mudhound.adapters.registry import AdapterRegistry
from mudhound.core.config import ConfigManager
from mudhound.core.engine import SearchEngine
from mudhound.core.result import SearchOptions
from mudhound.core.store import ResultStore
from mudhound.ui.components.banner import Banner
from mudhound.ui.components.confirm import Confirmation, ConfirmationVariant
from mudhound.ui.components.logo import Logo, LogoPosition
from mudhound.ui.components.menu import Menu
from mudhound.ui.components.prompt import Prompt, PromptType
from mudhound.ui.components.status import StatusComponent


class InteractiveSession:
    """
    Manages state for an interactive session.

    Maintains session state across multiple operations including:
    - Last search query and results
    - Configuration settings
    - User preferences
    - Navigation history

    Attributes:
        config_manager: Configuration manager instance
        result_store: Result store instance
        last_search_query: Last executed search query
        last_search_results: Results from last search
        last_search_session: Complete session from last search
        operation_count: Number of operations performed in this session
        session_data: Additional session data storage
    """

    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        result_store: Optional[ResultStore] = None,
    ):
        """
        Initialize the interactive session.

        Args:
            config_manager: ConfigManager instance (creates new if None)
            result_store: ResultStore instance (creates new if None)
        """
        self.config_manager = config_manager or ConfigManager()
        self.result_store = result_store or ResultStore()

        # Session state
        self.last_search_query: Optional[str] = None
        self.last_search_results: Optional[list] = None
        self.last_search_session: Optional[Any] = None
        self.operation_count: int = 0
        self.session_data: Dict[str, Any] = {}

    def update_search_state(self, query: str, session: Any) -> None:
        """
        Update session state after a search operation.

        Args:
            query: The search query that was executed
            session: The SearchSession object with results
        """
        self.last_search_query = query
        self.last_search_session = session
        self.last_search_results = session.results if session else []
        self.operation_count += 1

    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session state.

        Returns:
            Dictionary with session state information
        """
        return {
            "last_query": self.last_search_query,
            "result_count": len(self.last_search_results) if self.last_search_results else 0,
            "operations": self.operation_count,
            "has_results": self.last_search_results is not None
            and len(self.last_search_results) > 0,
        }

    def clear_search_state(self) -> None:
        """Clear search-related state."""
        self.last_search_query = None
        self.last_search_results = None
        self.last_search_session = None


class InteractiveMode:
    """
    Interactive TUI mode for MudHound.

    Provides a menu-driven interface for performing multiple operations:
    - Search: Execute new searches
    - History: View and replay past searches
    - Export: Export search results
    - Config: View and modify configuration
    - Quit: Exit the application

    Attributes:
        session: InteractiveSession managing state
        config_manager: Configuration manager
        result_store: Result store
        use_color: Whether to use colored output
        use_animation: Whether to use animations
        output: Output stream
    """

    def __init__(
        self,
        session: Optional[InteractiveSession] = None,
        use_color: bool = True,
        use_animation: bool = True,
        output: Optional[Any] = None,
    ):
        """
        Initialize interactive mode.

        Args:
            session: InteractiveSession instance (creates new if None)
            use_color: Whether to use colored output
            use_animation: Whether to use animations
            output: Output stream (defaults to stdout)
        """
        self.session = session or InteractiveSession()
        self.config_manager = self.session.config_manager
        self.result_store = self.session.result_store
        self.use_color = use_color
        self.use_animation = use_animation
        self.output = output or sys.stdout

        # Initialize UI components
        self.status = StatusComponent(
            use_color=use_color, show_timestamp=False)
        self.logo = Logo(
            position=LogoPosition.INLINE, config_manager=self.config_manager, output=self.output
        )

    def _show_banner(self) -> None:
        """Display the application banner."""
        if self.use_animation:
            banner = Banner(
                style="static",  # Use static for interactive mode
                config_manager=self.config_manager,
                output=self.output,
            )
            banner.render()
            self.output.write("\n")
            self.output.flush()

    def _show_goodbye(self) -> None:
        """Display goodbye message when exiting."""
        self.output.write("\n")
        self.logo.render()
        self.output.write(" ")
        self.status.success("Thank you for using MudHound!")
        self.output.flush()

    def _show_main_menu(self) -> Optional[str]:
        """
        Display the main menu and get user selection.

        Returns:
            Selected menu option or None if cancelled
        """
        options = ["Search", "History", "Export", "Config", "Quit"]

        menu = Menu(
            options=options,
            title="MudHound - Main Menu",
            use_color=self.use_color,
            output=self.output,
        )

        try:
            index = menu.show()
            if index is not None:
                return options[index].lower()
            return None
        except KeyboardInterrupt:
            # User pressed CTRL+C
            return "quit"

    def _handle_search(self) -> None:
        """Handle search operation."""
        self.output.write("\n")
        self.status.info("Search")
        self.output.write("\n")

        try:
            # Use Prompt component for validated input
            prompt = Prompt(
                prompt_text="Enter search query (empty to cancel)",
                prompt_type=PromptType.TEXT,
                default="",
                use_color=self.use_color,
                output=self.output,
            )
            query = prompt.prompt()

            if not query:
                self.status.warning("Search cancelled.")
                return

            # Get search options (use defaults for now)
            max_results = self.config_manager.get("search.max_results", 50)
            engine_name = self.config_manager.get(
                "search.default_engine", "duckduckgo")

            # Create search engine
            try:
                adapter_class = AdapterRegistry.get(engine_name)
                adapter = adapter_class()
                engine = SearchEngine(adapter=adapter)
            except Exception as e:
                self.status.error(f"Error initializing search engine: {e}")
                return

            # Execute search
            self.status.info(f"Searching for: {query}")
            self.output.flush()

            try:
                options = SearchOptions(max_results=max_results)
                session = engine.search(query=query, options=options)

                # Update session state
                self.session.update_search_state(query, session)

                # Display results
                self.status.success(f"Found {len(session.results)} results")
                self.output.write("\n")
                for result in session.results[:10]:  # Show first 10
                    self.output.write(f"[{result.rank}] {result.title}\n")
                    self.output.write(f"    {result.url}\n")
                    self.output.write(f"    {result.snippet[:100]}...\n\n")

                if len(session.results) > 10:
                    self.output.write(
                        f"... and {len(session.results) - 10} more results\n")

                # Persist to history
                self.result_store.persist(session)
                self.status.success("Search saved to history.")

            except KeyboardInterrupt:
                self.status.warning("Search cancelled by user.")
            except Exception as e:
                self.status.error(f"Search error: {e}")

        except KeyboardInterrupt:
            self.status.warning("Search cancelled.")

    def _handle_history(self) -> None:
        """Handle history operation."""
        self.output.write("\n")
        self.status.info("History")
        self.output.write("\n")

        try:
            sessions = self.result_store.list(limit=10)

            if not sessions:
                self.status.warning("No search history found.")
                return

            self.output.write(
                f"Recent searches (showing last {len(sessions)}):\n\n")

            for i, session in enumerate(sessions, 1):
                self.output.write(f"{i}. {session['query']}\n")
                self.output.write(f"   Results: {session['result_count']}, ")
                self.output.write(f"Status: {session['status']}\n")
                self.output.write(f"   ID: {session['id'][:8]}...\n\n")

        except Exception as e:
            self.status.error(f"Error loading history: {e}")

    def _handle_export(self) -> None:
        """Handle export operation."""
        self.output.write("\n")
        self.status.info("Export")
        self.output.write("\n")

        # Check if we have results to export
        if not self.session.last_search_results:
            self.status.warning(
                "No search results to export. Please perform a search first.")
            return

        self.output.write(f"Last search: {self.session.last_search_query}\n")
        self.output.write(
            f"Results: {len(self.session.last_search_results)}\n\n")
        self.status.info(
            "Export functionality will be available in the full implementation.")

    def _handle_config(self) -> None:
        """Handle config operation."""
        self.output.write("\n")
        self.status.info("Configuration")
        self.output.write("\n")

        try:
            # Show some key config values
            engine = self.config_manager.get(
                "search.default_engine", "duckduckgo")
            max_results = self.config_manager.get("search.max_results", 50)
            theme = self.config_manager.get("ui.theme", "default")

            self.output.write(f"Default search engine: {engine}\n")
            self.output.write(f"Max results: {max_results}\n")
            self.output.write(f"Theme: {theme}\n\n")
            self.status.info("Use 'mh config' command to modify settings.")

        except Exception as e:
            self.status.error(f"Error loading configuration: {e}")

    def _confirm_quit(self) -> bool:
        """
        Confirm quit intent with user.

        Returns:
            True if user confirms quit, False otherwise
        """
        confirmation = Confirmation(
            message="Are you sure you want to quit?",
            variant=ConfirmationVariant.YESNO,
            use_color=self.use_color,
            output=self.output,
        )

        try:
            return confirmation.confirm()
        except KeyboardInterrupt:
            # CTRL+C during confirmation means yes, quit
            return True

    def run(self) -> None:
        """
        Run the interactive mode main loop.

        Displays the main menu and handles user selections until quit.
        Maintains session state across operations.
        """
        # Show banner
        self._show_banner()

        # Main loop
        running = True

        while running:
            try:
                # Show main menu
                selection = self._show_main_menu()

                if selection is None:
                    # User cancelled menu (ESC)
                    if self._confirm_quit():
                        running = False
                    continue

                # Handle selection
                if selection == "search":
                    self._handle_search()

                elif selection == "history":
                    self._handle_history()

                elif selection == "export":
                    self._handle_export()

                elif selection == "config":
                    self._handle_config()

                elif selection == "quit":
                    if self._confirm_quit():
                        running = False
                    continue

                # Wait for user to press Enter before showing menu again
                if running and selection != "quit":
                    self.output.write("\n")
                    continue_prompt = Prompt(
                        prompt_text="Press Enter to continue",
                        prompt_type=PromptType.TEXT,
                        default="",
                        use_color=self.use_color,
                        output=self.output,
                    )
                    try:
                        continue_prompt.prompt()
                    except KeyboardInterrupt:
                        # CTRL+C here should confirm quit
                        if self._confirm_quit():
                            running = False

            except KeyboardInterrupt:
                # CTRL+C at main menu level
                self.output.write("\n")
                if self._confirm_quit():
                    running = False

            except Exception as e:
                self.status.error(f"Unexpected error: {e}")
                continue_prompt = Prompt(
                    prompt_text="Press Enter to continue",
                    prompt_type=PromptType.TEXT,
                    default="",
                    use_color=self.use_color,
                    output=self.output,
                )
                try:
                    continue_prompt.prompt()
                except KeyboardInterrupt:
                    if self._confirm_quit():
                        running = False

        # Show goodbye message
        self._show_goodbye()


def interactive_command(use_color: bool = True, use_animation: bool = True) -> None:
    """
    Entry point for the interactive command.

    Args:
        use_color: Whether to use colored output
        use_animation: Whether to use animations
    """
    interactive = InteractiveMode(
        use_color=use_color, use_animation=use_animation)
    interactive.run()


__all__ = ["InteractiveMode", "InteractiveSession", "interactive_command"]
