"""
Progress component for displaying operation progress in the terminal.

This module provides the Progress class which displays progress indicators
with support for multiple variants including bars, spinners, counters, and
rainbow animations.
"""

import sys
from datetime import datetime, timedelta
from typing import Optional, TextIO

from mudhound.ui.glyphs import get_glyph, get_spinner_frame
from mudhound.ui.theme import get_theme_engine


class ProgressVariant:
    """Progress display variant constants."""
    BAR = "bar"
    SPINNER = "spinner"
    COUNTER = "counter"
    TRANSFER = "transfer"
    RAINBOW = "rainbow"


class Progress:
    """
    Progress indicator component.
    
    Displays operation progress with configurable variants:
    - bar: Traditional progress bar with percentage
    - spinner: Animated spinner with counter
    - counter: Simple result counter
    - transfer: Transfer-style progress with rate
    - rainbow: Rainbow-colored progress bar
    
    Attributes:
        variant: Display variant (bar, spinner, counter, transfer, rainbow)
        total: Total number of items (None for indeterminate)
        current: Current progress count
        use_color: Whether to apply color codes
        output: Output stream for rendering
        start_time: Time when progress started
        last_render_time: Time of last render (for rate limiting)
        spinner_frame: Current spinner animation frame
        cancelled: Whether operation was cancelled
    """

    def __init__(
        self,
        variant: str = ProgressVariant.BAR,
        total: Optional[int] = None,
        use_color: bool = True,
        output: Optional[TextIO] = None
    ):
        """
        Initialize the Progress component.
        
        Args:
            variant: Display variant (bar, spinner, counter, transfer, rainbow)
            total: Total number of items (None for indeterminate progress)
            use_color: Whether to apply ANSI color codes
            output: Output stream (defaults to stdout)
        """
        self.variant = variant
        self.total = total
        self.current = 0
        self.use_color = use_color
        self.output = output or sys.stdout

        self.start_time: Optional[datetime] = None
        self.last_render_time: Optional[datetime] = None
        self.spinner_frame = 0
        self.cancelled = False

        # Minimum time between renders (to avoid flickering)
        self.min_render_interval = 0.1  # 100ms

    def start(self) -> None:
        """Start the progress tracking."""
        self.start_time = datetime.now()
        self.current = 0
        self.cancelled = False
        self.render()

    def update(self, count: int = 1) -> None:
        """
        Update the progress by incrementing the counter.
        
        Args:
            count: Number to increment by (default 1)
        """
        self.current += count

        # Rate limit rendering
        now = datetime.now()
        if self.last_render_time is None or \
           (now - self.last_render_time).total_seconds() >= self.min_render_interval:
            self.render()
            self.last_render_time = now

    def set_current(self, value: int) -> None:
        """
        Set the current progress value directly.
        
        Args:
            value: Current progress value
        """
        self.current = value
        self.render()

    def get_percentage(self) -> float:
        """
        Calculate the current progress percentage.
        
        Returns:
            Progress percentage (0-100), or 0 if total is None
        """
        if self.total is None or self.total == 0:
            return 0.0
        return min(100.0, (self.current / self.total) * 100.0)

    def get_elapsed_time(self) -> timedelta:
        """
        Get the elapsed time since progress started.
        
        Returns:
            Elapsed time as timedelta
        """
        if self.start_time is None:
            return timedelta(0)
        return datetime.now() - self.start_time

    def format_elapsed_time(self) -> str:
        """
        Format the elapsed time as a human-readable string.
        
        Returns:
            Formatted elapsed time (e.g., "1m 23s")
        """
        elapsed = self.get_elapsed_time()
        total_seconds = int(elapsed.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def _clear_line(self) -> None:
        """Clear the current line in the terminal."""
        self.output.write("\r\033[K")
        self.output.flush()

    def _render_bar(self) -> str:
        """
        Render a traditional progress bar.
        
        Returns:
            Formatted progress bar string
        """
        percentage = self.get_percentage()
        bar_width = 40
        filled = int((percentage / 100.0) * bar_width)
        empty = bar_width - filled

        bar = "█" * filled + "░" * empty

        if self.use_color:
            theme_engine = get_theme_engine()
            bar = theme_engine.apply(bar, "primary")

        return f"[{bar}] {percentage:.1f}% ({self.current}/{self.total or '?'})"

    def _render_spinner(self) -> str:
        """
        Render an animated spinner with counter.
        
        Returns:
            Formatted spinner string
        """
        spinner_char = get_spinner_frame(self.spinner_frame)
        self.spinner_frame = (self.spinner_frame + 1) % 10

        if self.use_color:
            theme_engine = get_theme_engine()
            spinner_char = theme_engine.apply(spinner_char, "accent")

        return f"{spinner_char} Processing... ({self.current} results)"

    def _render_counter(self) -> str:
        """
        Render a simple counter.
        
        Returns:
            Formatted counter string
        """
        bullet = get_glyph("progress", "bullet")

        if self.use_color:
            theme_engine = get_theme_engine()
            bullet = theme_engine.apply(bullet, "success")

        return f"{bullet} Results: {self.current}"

    def _render_transfer(self) -> str:
        """
        Render transfer-style progress with rate.
        
        Returns:
            Formatted transfer progress string
        """
        elapsed = self.get_elapsed_time()
        elapsed_seconds = elapsed.total_seconds()

        if elapsed_seconds > 0:
            rate = self.current / elapsed_seconds
            rate_str = f"{rate:.1f}/s"
        else:
            rate_str = "0.0/s"

        arrow = get_glyph("dataflow", "output")

        if self.use_color:
            theme_engine = get_theme_engine()
            arrow = theme_engine.apply(arrow, "info")

        return f"{arrow} {self.current} results @ {rate_str}"

    def _render_rainbow(self) -> str:
        """
        Render a rainbow-colored progress bar.
        
        Returns:
            Formatted rainbow progress bar string
        """
        percentage = self.get_percentage()
        bar_width = 40
        filled = int((percentage / 100.0) * bar_width)
        empty = bar_width - filled

        # Create bar with rainbow colors
        bar_chars = "█" * filled + "░" * empty

        if self.use_color:
            # Apply rainbow colors to filled portion
            from mudhound.ui.animation.schemes import RAINBOW_COLORS_256
            colored_bar = ""
            for i, char in enumerate(bar_chars):
                if i < filled:
                    color_idx = i % len(RAINBOW_COLORS_256)
                    color = RAINBOW_COLORS_256[color_idx]
                    colored_bar += f"\033[38;5;{color}m{char}\033[0m"
                else:
                    colored_bar += char
            bar_chars = colored_bar

        return f"[{bar_chars}] {percentage:.1f}% ({self.current}/{self.total or '?'})"

    def render(self) -> None:
        """
        Render the progress indicator based on the variant.
        
        Clears the current line and renders the appropriate progress display.
        """
        if self.cancelled:
            return

        # Clear current line
        self._clear_line()

        # Render based on variant
        if self.variant == ProgressVariant.BAR:
            progress_str = self._render_bar()
        elif self.variant == ProgressVariant.SPINNER:
            progress_str = self._render_spinner()
        elif self.variant == ProgressVariant.COUNTER:
            progress_str = self._render_counter()
        elif self.variant == ProgressVariant.TRANSFER:
            progress_str = self._render_transfer()
        elif self.variant == ProgressVariant.RAINBOW:
            progress_str = self._render_rainbow()
        else:
            progress_str = f"Progress: {self.current}"

        # Add elapsed time footer
        elapsed_str = self.format_elapsed_time()
        full_str = f"{progress_str} | {elapsed_str}"

        # Write to output
        self.output.write(full_str)
        self.output.flush()

    def complete(self, message: Optional[str] = None) -> None:
        """
        Mark the progress as complete and display final message.
        
        Args:
            message: Optional completion message
        """
        self._clear_line()

        if message:
            check = get_glyph("decorative", "check")
            if self.use_color:
                theme_engine = get_theme_engine()
                check = theme_engine.apply(check, "success")

            elapsed_str = self.format_elapsed_time()
            self.output.write(f"{check} {message} ({self.current} results in {elapsed_str})\n")
        else:
            self.output.write(f"Complete: {self.current} results\n")

        self.output.flush()

    def cancel(self, message: Optional[str] = None) -> None:
        """
        Cancel the progress and display cancellation message.
        
        Args:
            message: Optional cancellation message
        """
        self.cancelled = True
        self._clear_line()

        cross = get_glyph("decorative", "cross")
        if self.use_color:
            theme_engine = get_theme_engine()
            cross = theme_engine.apply(cross, "error")

        if message:
            self.output.write(f"{cross} {message}\n")
        else:
            self.output.write(f"{cross} Cancelled ({self.current} results)\n")

        self.output.flush()

    def error(self, message: str) -> None:
        """
        Display an error message and stop progress.
        
        Args:
            message: Error message to display
        """
        self.cancelled = True
        self._clear_line()

        error_glyph = get_glyph("status", "error")
        if self.use_color:
            theme_engine = get_theme_engine()
            error_glyph = theme_engine.apply(error_glyph, "error")

        self.output.write(f"{error_glyph} {message}\n")
        self.output.flush()


__all__ = ["Progress", "ProgressVariant"]
