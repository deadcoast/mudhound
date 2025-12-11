"""
Logo component for displaying compact animated ASCII art.

This module provides the Logo class which displays a compact MUDHOUND logo
with support for multiple positions and color schemes.
"""

import sys
from typing import Optional, TextIO

from mudhound.assets.manager import AssetManager
from mudhound.core.config import ConfigManager
from mudhound.ui.animation.engine import AnimationRenderer
from mudhound.ui.animation.schemes import ColorScheme
from mudhound.ui.animation.timing import TimingEngine


class LogoPosition:
    """Logo position constants."""

    INLINE = "inline"
    HEADER = "header"
    FOOTER = "footer"
    FLOATING = "floating"


class Logo:
    """
    Compact animated logo component.

    Displays a compact MUDHOUND logo with configurable positions and color schemes.
    Supports animated color cycling and multiple display positions.

    Attributes:
        position: Display position (inline, header, footer, floating)
        scheme: Color scheme for animation
        asset_manager: AssetManager for loading logo frames
        animation_renderer: AnimationRenderer for animated display
        config_manager: ConfigManager for loading preferences
        output: Output stream for rendering
    """

    def __init__(
        self,
        position: Optional[str] = None,
        scheme: Optional[str] = None,
        config_manager: Optional[ConfigManager] = None,
        asset_manager: Optional[AssetManager] = None,
        animation_renderer: Optional[AnimationRenderer] = None,
        output: Optional[TextIO] = None,
    ):
        """
        Initialize the Logo component.

        Args:
            position: Display position (inline, header, footer, floating).
                     If None, defaults to inline.
            scheme: Color scheme name. If None, loads from config.
            config_manager: ConfigManager instance for loading preferences
            asset_manager: AssetManager instance for loading frames
            animation_renderer: AnimationRenderer instance for animated display
            output: Output stream (defaults to stdout)
        """
        self.config_manager = config_manager or ConfigManager()
        self.asset_manager = asset_manager or AssetManager()
        self.output = output or sys.stdout

        # Load position and scheme from config if not provided
        if position is None:
            position = self.config_manager.get(
                "ui.logo_position", LogoPosition.INLINE)
        if scheme is None:
            scheme = self.config_manager.get(
                "animation.color_scheme", "rainbow")

        self.position = position
        self.scheme = scheme

        # Initialize animation renderer if needed
        if animation_renderer is None:
            timing_engine = TimingEngine(
                fps=self.config_manager.get("animation.fps", 10))
            self.animation_renderer = AnimationRenderer(
                timing_engine=timing_engine, asset_manager=self.asset_manager, output=self.output
            )
        else:
            self.animation_renderer = animation_renderer

    def _strip_ansi(self, text: str) -> str:
        """
        Strip ANSI escape codes from text.

        Args:
            text: Text with potential ANSI codes

        Returns:
            Text with ANSI codes removed
        """
        import re

        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", text)

    def _format_for_position(self, logo_content: str) -> str:
        """
        Format logo content based on the configured position.

        Args:
            logo_content: Raw logo content

        Returns:
            Formatted logo content for the specified position
        """
        if self.position == LogoPosition.INLINE:
            # For inline, keep logo on same line (strip newlines)
            lines = logo_content.strip().split("\n")
            # Join lines with spaces for inline display
            return " ".join(line.strip() for line in lines if line.strip())

        elif self.position == LogoPosition.HEADER:
            # For header, add spacing below
            return logo_content.strip() + "\n\n"

        elif self.position == LogoPosition.FOOTER:
            # For footer, add spacing above
            return "\n\n" + logo_content.strip()

        elif self.position == LogoPosition.FLOATING:
            # For floating, center the logo
            return self._center_logo(logo_content)

        else:
            # Default to inline
            return logo_content.strip()

    def _center_logo(self, logo_content: str) -> str:
        """
        Center the logo horizontally in the terminal.

        Args:
            logo_content: Logo content to center

        Returns:
            Centered logo content
        """
        try:
            import shutil

            terminal_width = shutil.get_terminal_size().columns
        except Exception:
            terminal_width = 80

        lines = logo_content.strip().split("\n")
        centered_lines = []

        for line in lines:
            visible_line = self._strip_ansi(line)
            line_width = len(visible_line)

            if line_width < terminal_width:
                padding = (terminal_width - line_width) // 2
                centered_lines.append(" " * padding + line)
            else:
                centered_lines.append(line)

        return "\n".join(centered_lines)

    def render(self, animated: bool = False) -> None:
        """
        Render the logo based on the configured position.

        Args:
            animated: Whether to render with animation (single frame if False)
        """
        # Load logo frames
        frames = self.asset_manager.get_logo_frames(self.scheme)

        if not frames:
            # Fallback to minimal logo
            self.output.write("[MH]")
            self.output.flush()
            return

        # Use first frame for static rendering
        logo_content = frames[0]

        # Format for position
        formatted_logo = self._format_for_position(logo_content)

        # Render
        self.output.write(formatted_logo)
        if self.position != LogoPosition.INLINE:
            self.output.write("\n")
        self.output.flush()

    def render_animated_frame(self, frame_index: int = 0) -> None:
        """
        Render a specific animated frame of the logo.

        Args:
            frame_index: Index of the frame to render
        """
        # Load logo frames
        self.animation_renderer.load_logo_frames(self.scheme)

        if not self.animation_renderer.frames:
            self.render(animated=False)
            return

        # Get the frame
        frame_index = frame_index % len(self.animation_renderer.frames)
        logo_content = self.animation_renderer.frames[frame_index]

        # Format for position
        formatted_logo = self._format_for_position(logo_content)

        # For animation, we need to handle clearing differently based on position
        if self.position == LogoPosition.INLINE:
            # For inline, just write the content
            self.output.write(formatted_logo)
        else:
            # For other positions, use the animation renderer's clearing
            self.animation_renderer.frames = [formatted_logo]
            self.animation_renderer.render_frame(0)

    def animate(self, duration: float = 0.0) -> None:
        """
        Animate the logo for the specified duration.

        Args:
            duration: Animation duration in seconds (0 = infinite loop)
        """
        # Load logo frames
        self.animation_renderer.load_logo_frames(self.scheme)

        if not self.animation_renderer.frames:
            self.render(animated=False)
            return

        # Format all frames for position
        formatted_frames = [
            self._format_for_position(frame) for frame in self.animation_renderer.frames
        ]

        # Load formatted frames
        self.animation_renderer.load_frames(formatted_frames)

        # Run animation
        self.animation_renderer.animate(duration=duration)

    def clear(self) -> None:
        """Clear the logo from the terminal."""
        if self.animation_renderer:
            self.animation_renderer.clear()
