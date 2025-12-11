"""
Core UI renderer for terminal output.

This module provides the UIRenderer class which handles all terminal output,
including frame rendering with theme application, ANSI escape sequence handling,
cursor management, and output buffering.
"""

import sys
from io import StringIO
from typing import List, Optional, TextIO

from mudhound.ui.frames import BorderStyle, FrameRenderer
from mudhound.ui.layout import LayoutManager
from mudhound.ui.theme import ThemeEngine, get_theme_engine


class UIRenderer:
    """
    Core renderer for terminal UI output.

    Handles frame rendering with theme application, cursor management,
    ANSI escape sequences, and output buffering for smooth rendering.

    Attributes:
        frame_renderer: FrameRenderer instance for drawing frames
        theme_engine: ThemeEngine instance for color application
        layout_manager: LayoutManager for responsive sizing
        output: Output stream (defaults to stdout)
        buffer: StringIO buffer for batched output
    """

    # ANSI escape sequences for cursor management
    CURSOR_SAVE = "\033[s"
    CURSOR_RESTORE = "\033[u"
    CURSOR_HIDE = "\033[?25l"
    CURSOR_SHOW = "\033[?25h"
    CLEAR_LINE = "\033[2K"
    CLEAR_SCREEN = "\033[2J"
    CURSOR_HOME = "\033[H"

    def __init__(
        self,
        frame_renderer: Optional[FrameRenderer] = None,
        theme_engine: Optional[ThemeEngine] = None,
        layout_manager: Optional[LayoutManager] = None,
        output: Optional[TextIO] = None,
    ):
        """
        Initialize the UI renderer.

        Args:
            frame_renderer: FrameRenderer instance (creates default if None)
            theme_engine: ThemeEngine instance (uses global if None)
            layout_manager: LayoutManager instance (creates default if None)
            output: Output stream (defaults to stdout)
        """
        self.frame_renderer = frame_renderer or FrameRenderer()
        self.theme_engine = theme_engine or get_theme_engine()
        self.layout_manager = layout_manager or LayoutManager()
        self.output = output or sys.stdout
        self.buffer = StringIO()

        # Track cursor state
        self._cursor_visible = True

    def save_cursor(self) -> None:
        """Save the current cursor position."""
        self.buffer.write(self.CURSOR_SAVE)

    def restore_cursor(self) -> None:
        """Restore the cursor to the saved position."""
        self.buffer.write(self.CURSOR_RESTORE)

    def hide_cursor(self) -> None:
        """Hide the terminal cursor."""
        if self._cursor_visible:
            self.buffer.write(self.CURSOR_HIDE)
            self._cursor_visible = False

    def show_cursor(self) -> None:
        """Show the terminal cursor."""
        if not self._cursor_visible:
            self.buffer.write(self.CURSOR_SHOW)
            self._cursor_visible = True

    def move_cursor_up(self, lines: int) -> None:
        """
        Move cursor up by specified number of lines.

        Args:
            lines: Number of lines to move up
        """
        if lines > 0:
            self.buffer.write(f"\033[{lines}A")

    def move_cursor_down(self, lines: int) -> None:
        """
        Move cursor down by specified number of lines.

        Args:
            lines: Number of lines to move down
        """
        if lines > 0:
            self.buffer.write(f"\033[{lines}B")

    def move_cursor_to_column(self, column: int) -> None:
        """
        Move cursor to specified column (1-indexed).

        Args:
            column: Column number (1-indexed)
        """
        self.buffer.write(f"\033[{column}G")

    def clear_line(self) -> None:
        """Clear the current line."""
        self.buffer.write(self.CLEAR_LINE)

    def clear_lines(self, count: int) -> None:
        """
        Clear multiple lines starting from current position.

        Args:
            count: Number of lines to clear
        """
        for _ in range(count):
            self.clear_line()
            if _ < count - 1:
                self.move_cursor_down(1)
                self.move_cursor_to_column(1)

    def clear_screen(self) -> None:
        """Clear the entire screen."""
        self.buffer.write(self.CLEAR_SCREEN)
        self.buffer.write(self.CURSOR_HOME)

    def apply_theme_to_text(self, text: str, semantic_name: str) -> str:
        """
        Apply theme color to text.

        Args:
            text: Text to colorize
            semantic_name: Semantic color name from theme

        Returns:
            Text with ANSI color codes applied
        """
        return self.theme_engine.apply(text, semantic_name)

    def render_frame(
        self,
        content: List[str],
        title: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        pagination: Optional[str] = None,
        style: Optional[BorderStyle] = None,
        apply_theme: bool = True,
    ) -> List[str]:
        """
        Render a complete frame with theme application.

        Args:
            content: List of content lines
            title: Optional title for top border
            status: Optional status for bottom border
            tag: Optional tag for top border
            pagination: Optional pagination info for bottom border
            style: Border style (uses frame_renderer's style if None)
            apply_theme: Whether to apply theme colors

        Returns:
            List of rendered frame lines with theme applied
        """
        # Get current terminal width for responsive rendering
        width = self.layout_manager.get_terminal_size()[0]

        # Update frame renderer width
        if style:
            self.frame_renderer.set_style(style)
        self.frame_renderer.set_width(width)

        # Build frame
        frame_lines = []

        # Top border
        top = self.frame_renderer.top_border(title=title, tag=tag)
        if apply_theme:
            top = self.apply_theme_to_text(top, "frame_border")
        frame_lines.append(top)

        # Content rows
        content_rows = self.frame_renderer.content_rows(content)
        for row in content_rows:
            if apply_theme:
                # Apply theme to border characters, keep content as-is
                # Split into border + content + border
                border_char = self.frame_renderer.chars["vertical"]
                if row.startswith(border_char):
                    # Apply theme to borders only
                    themed_border = self.apply_theme_to_text(
                        border_char, "frame_border")
                    # Replace first and last border characters
                    row = themed_border + row[1:-1] + themed_border
            frame_lines.append(row)

        # Bottom border
        bottom = self.frame_renderer.bottom_border(
            status=status, pagination=pagination)
        if apply_theme:
            bottom = self.apply_theme_to_text(bottom, "frame_border")
        frame_lines.append(bottom)

        return frame_lines

    def render_frame_with_header(
        self,
        header: str,
        content: List[str],
        title: Optional[str] = None,
        style: Optional[BorderStyle] = None,
        apply_theme: bool = True,
    ) -> List[str]:
        """
        Render a frame with a header section.

        Args:
            header: Header text
            content: List of content lines
            title: Optional title for top border
            style: Border style
            apply_theme: Whether to apply theme colors

        Returns:
            List of rendered frame lines with theme applied
        """
        # Get current terminal width
        width = self.layout_manager.get_terminal_size()[0]

        # Update frame renderer
        if style:
            self.frame_renderer.set_style(style)
        self.frame_renderer.set_width(width)

        # Build frame
        frame_lines = []

        # Top border
        top = self.frame_renderer.top_border(title=title)
        if apply_theme:
            top = self.apply_theme_to_text(top, "frame_border")
        frame_lines.append(top)

        # Header row
        header_row = self.frame_renderer.header_row(header, align="center")
        if apply_theme:
            border_char = self.frame_renderer.chars["vertical"]
            themed_border = self.apply_theme_to_text(
                border_char, "frame_border")
            header_row = themed_border + header_row[1:-1] + themed_border
        frame_lines.append(header_row)

        # Divider
        divider = self.frame_renderer.divider()
        if apply_theme:
            divider = self.apply_theme_to_text(divider, "frame_border")
        frame_lines.append(divider)

        # Content rows
        content_rows = self.frame_renderer.content_rows(content)
        for row in content_rows:
            if apply_theme:
                border_char = self.frame_renderer.chars["vertical"]
                themed_border = self.apply_theme_to_text(
                    border_char, "frame_border")
                row = themed_border + row[1:-1] + themed_border
            frame_lines.append(row)

        # Bottom border
        bottom = self.frame_renderer.bottom_border()
        if apply_theme:
            bottom = self.apply_theme_to_text(bottom, "frame_border")
        frame_lines.append(bottom)

        return frame_lines

    def write(self, text: str) -> None:
        """
        Write text to the output buffer.

        Args:
            text: Text to write
        """
        self.buffer.write(text)

    def writeln(self, text: str = "") -> None:
        """
        Write text followed by a newline to the output buffer.

        Args:
            text: Text to write (empty string for blank line)
        """
        self.buffer.write(text)
        self.buffer.write("\n")

    def write_lines(self, lines: List[str]) -> None:
        """
        Write multiple lines to the output buffer.

        Args:
            lines: List of lines to write
        """
        for line in lines:
            self.writeln(line)

    def flush(self) -> None:
        """Flush the buffer to the output stream."""
        content = self.buffer.getvalue()
        if content:
            self.output.write(content)
            self.output.flush()
            # Clear the buffer
            self.buffer = StringIO()

    def render_and_flush(
        self,
        content: List[str],
        title: Optional[str] = None,
        status: Optional[str] = None,
        apply_theme: bool = True,
    ) -> None:
        """
        Render a frame and immediately flush to output.

        Convenience method that combines render_frame, write_lines, and flush.

        Args:
            content: List of content lines
            title: Optional title
            status: Optional status
            apply_theme: Whether to apply theme colors
        """
        frame = self.render_frame(
            content=content, title=title, status=status, apply_theme=apply_theme
        )
        self.write_lines(frame)
        self.flush()

    def clear_and_render(
        self,
        content: List[str],
        previous_line_count: int = 0,
        title: Optional[str] = None,
        status: Optional[str] = None,
        apply_theme: bool = True,
    ) -> int:
        """
        Clear previous output and render new frame.

        Useful for updating animated or dynamic content.

        Args:
            content: List of content lines
            previous_line_count: Number of lines to clear from previous render
            title: Optional title
            status: Optional status
            apply_theme: Whether to apply theme colors

        Returns:
            Number of lines rendered (for next clear operation)
        """
        # Clear previous output if any
        if previous_line_count > 0:
            self.move_cursor_up(previous_line_count)
            self.clear_lines(previous_line_count)
            self.move_cursor_up(previous_line_count)

        # Render new frame
        frame = self.render_frame(
            content=content, title=title, status=status, apply_theme=apply_theme
        )

        self.write_lines(frame)
        self.flush()

        return len(frame)
