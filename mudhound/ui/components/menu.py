"""
Menu component for interactive navigation.

This module provides the Menu class for displaying numbered options
with keyboard navigation support.
"""

import sys
from typing import List, Optional, TextIO

from mudhound.ui.glyphs import get_glyph
from mudhound.ui.theme import get_theme_engine


class Menu:
    """
    Interactive menu component with keyboard navigation.

    Displays numbered options with a cursor indicator and supports:
    - Arrow key navigation (up/down)
    - Number key direct selection
    - Enter to confirm selection
    - ESC to cancel

    Attributes:
        options: List of menu option strings
        title: Optional menu title
        selected_index: Currently selected option index
        use_color: Whether to apply color codes
        output: Output stream for rendering
        input_stream: Input stream for reading user input
    """

    def __init__(
        self,
        options: List[str],
        title: Optional[str] = None,
        selected_index: int = 0,
        use_color: bool = True,
        output: Optional[TextIO] = None,
        input_stream: Optional[TextIO] = None,
    ):
        """
        Initialize the Menu component.

        Args:
            options: List of menu option strings
            title: Optional menu title
            selected_index: Initial selected option index (default 0)
            use_color: Whether to apply ANSI color codes
            output: Output stream (defaults to stdout)
            input_stream: Input stream (defaults to stdin)
        """
        if not options:
            raise ValueError("Menu must have at least one option")

        self.options = options
        self.title = title
        self.selected_index = max(0, min(selected_index, len(options) - 1))
        self.use_color = use_color
        self.output = output or sys.stdout
        self.input_stream = input_stream or sys.stdin

    def _format_option(self, index: int, option: str, is_selected: bool) -> str:
        """
        Format a menu option with number and cursor indicator.

        Args:
            index: Option index (0-based)
            option: Option text
            is_selected: Whether this option is currently selected

        Returns:
            Formatted option string
        """
        # Number the option (1-based for display)
        number = index + 1

        # Add cursor indicator for selected option
        if is_selected:
            cursor = get_glyph("selection", "cursor")
            if self.use_color:
                theme_engine = get_theme_engine()
                cursor = theme_engine.apply(cursor, "accent")
                option_text = theme_engine.apply(option, "accent")
            else:
                option_text = option
            return f"{cursor} {number}. {option_text}"
        else:
            return f"  {number}. {option}"

    def _render_menu(self) -> str:
        """
        Render the complete menu.

        Returns:
            Formatted menu string
        """
        lines = []

        # Add title if present
        if self.title:
            if self.use_color:
                theme_engine = get_theme_engine()
                title_text = theme_engine.apply(self.title, "primary")
            else:
                title_text = self.title
            lines.append(title_text)
            lines.append("")  # Blank line after title

        # Add all options
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_index
            formatted_option = self._format_option(i, option, is_selected)
            lines.append(formatted_option)

        return "\n".join(lines)

    def _read_key(self) -> str:
        """
        Read a single key press from input.

        This is a simplified implementation that reads a line.
        For full arrow key support, platform-specific terminal handling
        would be needed (e.g., using termios on Unix, msvcrt on Windows).

        Returns:
            Key string
        """
        # Read a line of input
        line = self.input_stream.readline()

        if not line:
            return ""

        # Strip whitespace
        key = line.strip()

        return key

    def _handle_number_selection(self, key: str) -> Optional[int]:
        """
        Handle direct number selection.

        Args:
            key: Input key string

        Returns:
            Selected index if valid number, None otherwise
        """
        try:
            number = int(key)
            # Convert from 1-based to 0-based index
            index = number - 1

            # Validate index is in range
            if 0 <= index < len(self.options):
                return index
        except ValueError:
            pass

        return None

    def show(self) -> Optional[int]:
        """
        Display the menu and get user selection.

        Supports:
        - Arrow keys: 'up'/'u' to move up, 'down'/'d' to move down
        - Number keys: Direct selection (1-based)
        - Enter: Confirm selection (empty input)
        - ESC: Cancel and return None

        Returns:
            Selected option index (0-based) or None if cancelled

        Raises:
            KeyboardInterrupt: If user presses CTRL+C
        """
        try:
            while True:
                # Render and display menu
                menu_text = self._render_menu()
                self.output.write(menu_text + "\n")
                self.output.write("\nSelect option (number/up/down/enter/esc): ")
                self.output.flush()

                # Read input
                key = self._read_key()

                # Handle empty input (Enter to confirm)
                if not key:
                    return self.selected_index

                # Handle ESC to cancel
                if key.lower() in ("esc", "escape", "q", "quit"):
                    return None

                # Handle arrow key navigation
                if key.lower() in ("up", "u"):
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    # Clear previous menu display
                    self._clear_menu()
                    continue

                if key.lower() in ("down", "d"):
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    # Clear previous menu display
                    self._clear_menu()
                    continue

                # Handle direct number selection
                selected_index = self._handle_number_selection(key)
                if selected_index is not None:
                    return selected_index

                # Invalid input - show error and redisplay
                error_msg = "Invalid input. Use number, up/down, enter, or esc."
                if self.use_color:
                    theme_engine = get_theme_engine()
                    error_msg = theme_engine.apply(error_msg, "error")
                self.output.write(error_msg + "\n")
                self.output.flush()

                # Clear previous menu display
                self._clear_menu()

        except KeyboardInterrupt:
            # User pressed CTRL+C
            self.output.write("\n")
            self.output.flush()
            raise

    def _clear_menu(self):
        """Clear the previous menu display."""
        # Calculate number of lines to clear
        lines_to_clear = len(self.options)
        if self.title:
            lines_to_clear += 2  # Title + blank line
        lines_to_clear += 2  # Prompt line + error/input line

        # Move cursor up and clear lines
        for _ in range(lines_to_clear):
            self.output.write("\033[F\033[K")  # Move up and clear line
        self.output.flush()

    def get_selected_option(self) -> Optional[str]:
        """
        Show menu and return the selected option text.

        Returns:
            Selected option text or None if cancelled
        """
        index = self.show()
        if index is not None:
            return self.options[index]
        return None


__all__ = ["Menu"]
