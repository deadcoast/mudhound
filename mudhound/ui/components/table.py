"""
Table component for displaying search results.

This module provides the Table class for rendering search results in a
tabular format with columns for rank, URL, and source. Supports auto-sizing,
URL truncation, keyboard navigation, and inline filtering.
"""

import sys
from dataclasses import dataclass
from typing import List, Optional, TextIO

from mudhound.core.result import SearchResult
from mudhound.ui.glyphs import GLYPHS
from mudhound.ui.layout import LayoutManager
from mudhound.ui.theme import get_theme_engine


@dataclass
class ColumnConfig:
    """Configuration for a table column.

    Attributes:
        name: Column name/header
        width: Column width in characters (None for auto-size)
        min_width: Minimum column width
        max_width: Maximum column width (None for unlimited)
        align: Text alignment ("left", "center", "right")
    """

    name: str
    width: Optional[int] = None
    min_width: int = 5
    max_width: Optional[int] = None
    align: str = "left"


class Table:
    """
    Table component for displaying search results.

    Renders search results in a tabular format with columns for rank, URL,
    and source. Supports auto-sizing based on terminal width, URL truncation
    with ellipsis, keyboard navigation (j/k, PgUp/PgDn), and inline filtering.

    Attributes:
        results: List of search results to display
        layout_manager: LayoutManager for terminal dimensions
        use_color: Whether to apply color codes
        output: Output stream for rendering
        input_stream: Input stream for reading user input
        current_row: Currently selected row index
        filter_text: Current filter text
        page_size: Number of rows per page
    """

    # Default column configurations
    DEFAULT_COLUMNS = [
        ColumnConfig(name="Rank", width=6, min_width=6,
                     max_width=6, align="right"),
        ColumnConfig(name="URL", min_width=20, align="left"),
        ColumnConfig(name="Source", width=20, min_width=10,
                     max_width=30, align="left"),
    ]

    def __init__(
        self,
        results: List[SearchResult],
        layout_manager: Optional[LayoutManager] = None,
        use_color: bool = True,
        output: Optional[TextIO] = None,
        input_stream: Optional[TextIO] = None,
        page_size: int = 10,
    ):
        """
        Initialize the Table component.

        Args:
            results: List of search results to display
            layout_manager: LayoutManager instance (creates default if None)
            use_color: Whether to apply ANSI color codes
            output: Output stream (defaults to stdout)
            input_stream: Input stream (defaults to stdin)
            page_size: Number of rows per page for pagination
        """
        self.results = results
        self.layout_manager = layout_manager or LayoutManager()
        self.use_color = use_color
        self.output = output or sys.stdout
        self.input_stream = input_stream or sys.stdin
        self.page_size = page_size

        # Navigation state
        self.current_row = 0
        self.current_page = 0
        self.filter_text = ""

        # Column configurations
        self.columns = self.DEFAULT_COLUMNS.copy()

    def _calculate_column_widths(self) -> List[int]:
        """
        Calculate column widths based on terminal width and content.

        Auto-sizes columns to fit within terminal width while respecting
        min/max constraints.

        Returns:
            List of column widths
        """
        # Get available width (accounting for borders and padding)
        terminal_width = self.layout_manager.get_terminal_size()[0]
        available_width = terminal_width - 4  # Subtract frame borders

        # Account for column separators (spaces between columns)
        separator_width = len(self.columns) - 1
        available_width -= separator_width

        # Ensure we have minimum available width
        if available_width < 20:
            available_width = 20

        # Calculate widths
        widths = []
        remaining_width = available_width
        flexible_columns = []

        # First pass: assign fixed and min widths
        for i, col in enumerate(self.columns):
            if col.width is not None:
                # Fixed width column
                widths.append(col.width)
                remaining_width -= col.width
            else:
                # Flexible column - start with min width
                widths.append(col.min_width)
                remaining_width -= col.min_width
                flexible_columns.append(i)

        # If we've exceeded available width, we need to shrink flexible columns
        if remaining_width < 0 and flexible_columns:
            # Reduce flexible columns proportionally
            deficit = -remaining_width

            for i in flexible_columns:
                # Calculate how much we can reduce this column
                col = self.columns[i]
                # We can reduce down to a minimum of 5 characters
                absolute_min = 5
                max_reduction = widths[i] - absolute_min

                if max_reduction > 0:
                    # Reduce this column
                    reduction = min(deficit, max_reduction)
                    widths[i] -= reduction
                    deficit -= reduction
                    remaining_width += reduction

                    if deficit <= 0:
                        break

        # Second pass: distribute remaining width to flexible columns
        if remaining_width > 0 and flexible_columns:
            # Distribute evenly among flexible columns
            extra_per_column = remaining_width // len(flexible_columns)
            remainder = remaining_width % len(flexible_columns)

            for i in flexible_columns:
                extra = extra_per_column
                if remainder > 0:
                    extra += 1
                    remainder -= 1

                # Apply max width constraint if present
                col = self.columns[i]
                if col.max_width is not None:
                    max_extra = col.max_width - widths[i]
                    extra = min(extra, max_extra)

                widths[i] += extra

        return widths

    def _truncate_text(self, text: str, width: int) -> str:
        """
        Truncate text to fit within width, adding ellipsis if needed.

        Args:
            text: Text to truncate
            width: Maximum width

        Returns:
            Truncated text with ellipsis if needed
        """
        if len(text) <= width:
            return text

        if width <= 3:
            return "..."[:width]

        return text[: width - 3] + "..."

    def _format_cell(self, text: str, width: int, align: str = "left") -> str:
        """
        Format a cell with alignment and padding.

        Args:
            text: Cell text
            width: Cell width
            align: Alignment ("left", "center", "right")

        Returns:
            Formatted cell text
        """
        # Truncate if needed
        text = self._truncate_text(text, width)

        # Apply alignment
        if align == "center":
            return text.center(width)
        elif align == "right":
            return text.rjust(width)
        else:  # left
            return text.ljust(width)

    def _render_header(self, widths: List[int]) -> str:
        """
        Render the table header row.

        Args:
            widths: List of column widths

        Returns:
            Formatted header row
        """
        cells = []
        for col, width in zip(self.columns, widths):
            cell = self._format_cell(col.name, width, col.align)
            if self.use_color:
                theme_engine = get_theme_engine()
                cell = theme_engine.apply(cell, "primary")
            cells.append(cell)

        return " ".join(cells)

    def _render_separator(self, widths: List[int]) -> str:
        """
        Render a separator line between header and content.

        Args:
            widths: List of column widths

        Returns:
            Formatted separator line
        """
        separators = []
        for width in widths:
            separators.append("─" * width)

        line = " ".join(separators)

        if self.use_color:
            theme_engine = get_theme_engine()
            line = theme_engine.apply(line, "frame_border")

        return line

    def _render_row(
        self, result: SearchResult, widths: List[int], is_selected: bool = False
    ) -> str:
        """
        Render a single data row.

        Args:
            result: Search result to render
            widths: List of column widths
            is_selected: Whether this row is currently selected

        Returns:
            Formatted row
        """
        # Extract data for each column
        rank_text = str(result.rank)
        url_text = result.url
        source_text = result.source

        # Format cells
        cells = [
            self._format_cell(rank_text, widths[0], self.columns[0].align),
            self._format_cell(url_text, widths[1], self.columns[1].align),
            self._format_cell(source_text, widths[2], self.columns[2].align),
        ]

        row = " ".join(cells)

        # Apply selection highlighting
        if is_selected:
            cursor = GLYPHS["selection"]["cursor"]
            if self.use_color:
                theme_engine = get_theme_engine()
                row = theme_engine.apply(row, "accent")
                cursor = theme_engine.apply(cursor, "accent")
            row = f"{cursor} {row}"
        else:
            row = f"  {row}"

        return row

    def _filter_results(self) -> List[SearchResult]:
        """
        Filter results based on current filter text.

        Returns:
            Filtered list of results
        """
        if not self.filter_text:
            return self.results

        filter_lower = self.filter_text.lower()
        filtered = []

        for result in self.results:
            # Search in URL, title, snippet, and source
            if (
                filter_lower in result.url.lower()
                or filter_lower in result.title.lower()
                or filter_lower in result.snippet.lower()
                or filter_lower in result.source.lower()
            ):
                filtered.append(result)

        return filtered

    def _get_page_results(self, filtered_results: List[SearchResult]) -> List[SearchResult]:
        """
        Get results for the current page.

        Args:
            filtered_results: Filtered results list

        Returns:
            Results for current page
        """
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        return filtered_results[start_idx:end_idx]

    def render(self) -> List[str]:
        """
        Render the complete table.

        Returns:
            List of rendered table lines
        """
        lines = []

        # Calculate column widths
        widths = self._calculate_column_widths()

        # Render header
        lines.append(self._render_header(widths))
        lines.append(self._render_separator(widths))

        # Filter results
        filtered_results = self._filter_results()

        # Get page results
        page_results = self._get_page_results(filtered_results)

        # Render rows
        if not page_results:
            no_results = "No results found"
            if self.use_color:
                theme_engine = get_theme_engine()
                no_results = theme_engine.apply(no_results, "warning")
            lines.append(no_results)
        else:
            for i, result in enumerate(page_results):
                is_selected = i == self.current_row
                lines.append(self._render_row(result, widths, is_selected))

        # Add filter indicator if active
        if self.filter_text:
            filter_line = f"Filter: {self.filter_text}"
            if self.use_color:
                theme_engine = get_theme_engine()
                filter_line = theme_engine.apply(filter_line, "info")
            lines.append("")
            lines.append(filter_line)

        # Add pagination info
        total_pages = (len(filtered_results) +
                       self.page_size - 1) // self.page_size
        if total_pages > 1:
            page_info = f"Page {self.current_page + 1}/{total_pages}"
            if self.use_color:
                theme_engine = get_theme_engine()
                page_info = theme_engine.apply(page_info, "secondary")
            lines.append(page_info)

        return lines

    def navigate_up(self) -> None:
        """Move selection up one row."""
        if self.current_row > 0:
            self.current_row -= 1
        elif self.current_page > 0:
            # Move to previous page
            self.current_page -= 1
            self.current_row = self.page_size - 1

    def navigate_down(self) -> None:
        """Move selection down one row."""
        filtered_results = self._filter_results()
        page_results = self._get_page_results(filtered_results)

        if self.current_row < len(page_results) - 1:
            self.current_row += 1
        else:
            # Check if there's a next page
            total_pages = (len(filtered_results) +
                           self.page_size - 1) // self.page_size
            if self.current_page < total_pages - 1:
                self.current_page += 1
                self.current_row = 0

    def page_up(self) -> None:
        """Move up one page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.current_row = 0

    def page_down(self) -> None:
        """Move down one page."""
        filtered_results = self._filter_results()
        total_pages = (len(filtered_results) +
                       self.page_size - 1) // self.page_size

        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.current_row = 0

    def set_filter(self, filter_text: str) -> None:
        """
        Set the filter text and reset navigation.

        Args:
            filter_text: Filter text to apply
        """
        self.filter_text = filter_text
        self.current_row = 0
        self.current_page = 0

    def clear_filter(self) -> None:
        """Clear the current filter."""
        self.filter_text = ""
        self.current_row = 0
        self.current_page = 0

    def get_selected_result(self) -> Optional[SearchResult]:
        """
        Get the currently selected search result.

        Returns:
            Selected SearchResult or None if no selection
        """
        filtered_results = self._filter_results()
        page_results = self._get_page_results(filtered_results)

        if 0 <= self.current_row < len(page_results):
            return page_results[self.current_row]

        return None

    def show_interactive(self) -> Optional[SearchResult]:
        """
        Display the table with interactive navigation.

        Supports:
        - j/k: Move down/up
        - PgUp/PgDn: Page up/down
        - /: Activate inline filtering
        - Enter: Select current result
        - ESC/q: Exit without selection

        Returns:
            Selected SearchResult or None if cancelled

        Raises:
            KeyboardInterrupt: If user presses CTRL+C
        """
        try:
            while True:
                # Render and display table
                table_lines = self.render()
                for line in table_lines:
                    self.output.write(line + "\n")

                self.output.write(
                    "\nNavigate: j/k, PgUp/PgDn | Filter: / | Select: Enter | Quit: q\n"
                )
                self.output.write("> ")
                self.output.flush()

                # Read input
                key = self.input_stream.readline().strip()

                # Handle commands
                if not key or key.lower() == "enter":
                    return self.get_selected_result()

                if key.lower() in ("q", "quit", "esc", "escape"):
                    return None

                if key.lower() in ("j", "down"):
                    self.navigate_down()
                elif key.lower() in ("k", "up"):
                    self.navigate_up()
                elif key.lower() in ("pgdn", "pagedown"):
                    self.page_down()
                elif key.lower() in ("pgup", "pageup"):
                    self.page_up()
                elif key == "/":
                    # Activate filtering
                    self.output.write("Filter: ")
                    self.output.flush()
                    filter_text = self.input_stream.readline().strip()
                    self.set_filter(filter_text)
                elif key.lower() == "clear":
                    self.clear_filter()

                # Clear previous display
                self._clear_display(len(table_lines) + 2)

        except KeyboardInterrupt:
            self.output.write("\n")
            self.output.flush()
            raise

    def _clear_display(self, line_count: int) -> None:
        """
        Clear the previous table display.

        Args:
            line_count: Number of lines to clear
        """
        for _ in range(line_count):
            self.output.write("\033[F\033[K")  # Move up and clear line
        self.output.flush()


__all__ = ["Table", "ColumnConfig"]
