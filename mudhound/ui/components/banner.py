"""
Banner component for displaying animated ASCII art headers.

This module provides the Banner class which displays the MUDHOUND logo
with support for multiple display styles and color schemes.
"""

import sys
from typing import Optional, TextIO

from mudhound.ui.animation.engine import AnimationRenderer
from mudhound.ui.animation.timing import TimingEngine
from mudhound.ui.animation.schemes import ColorScheme, generate_rainbow_frame
from mudhound.assets.manager import AssetManager
from mudhound.core.config import ConfigManager


class BannerStyle:
    """Banner display style constants."""
    ANIMATED = "animated"
    STATIC = "static"
    MINIMAL = "minimal"
    NONE = "none"


class Banner:
    """
    Animated ASCII art banner component.
    
    Displays the MUDHOUND logo with configurable styles and color schemes.
    Supports animated color cycling, static display, minimal text, or no banner.
    
    Attributes:
        style: Display style (animated, static, minimal, none)
        scheme: Color scheme for animation
        asset_manager: AssetManager for loading banner frames
        animation_renderer: AnimationRenderer for animated display
        config_manager: ConfigManager for loading preferences
        output: Output stream for rendering
    """
    
    def __init__(
        self,
        style: Optional[str] = None,
        scheme: Optional[str] = None,
        config_manager: Optional[ConfigManager] = None,
        asset_manager: Optional[AssetManager] = None,
        animation_renderer: Optional[AnimationRenderer] = None,
        output: Optional[TextIO] = None
    ):
        """
        Initialize the Banner component.
        
        Args:
            style: Display style (animated, static, minimal, none). 
                   If None, loads from config.
            scheme: Color scheme name. If None, loads from config.
            config_manager: ConfigManager instance for loading preferences
            asset_manager: AssetManager instance for loading frames
            animation_renderer: AnimationRenderer instance for animated display
            output: Output stream (defaults to stdout)
        """
        self.config_manager = config_manager or ConfigManager()
        self.asset_manager = asset_manager or AssetManager()
        self.output = output or sys.stdout
        
        # Load style and scheme from config if not provided
        if style is None:
            style = self.config_manager.get("ui.banner_style", BannerStyle.ANIMATED)
        if scheme is None:
            scheme = self.config_manager.get("animation.color_scheme", "rainbow")
        
        self.style = style
        self.scheme = scheme
        
        # Initialize animation renderer if needed
        if animation_renderer is None and style == BannerStyle.ANIMATED:
            timing_engine = TimingEngine(
                fps=self.config_manager.get("animation.fps", 10)
            )
            self.animation_renderer = AnimationRenderer(
                timing_engine=timing_engine,
                asset_manager=self.asset_manager,
                output=self.output
            )
        else:
            self.animation_renderer = animation_renderer
    
    def _get_terminal_width(self) -> int:
        """
        Get the current terminal width.
        
        Returns:
            Terminal width in columns
        """
        try:
            import shutil
            size = shutil.get_terminal_size()
            return size.columns
        except Exception:
            return 80  # Default fallback
    
    def _scale_banner(self, banner_content: str, max_width: int) -> str:
        """
        Scale down banner content to fit within max_width.
        
        For narrow terminals, this truncates lines and adds ellipsis.
        
        Args:
            banner_content: Original banner content
            max_width: Maximum width in columns
            
        Returns:
            Scaled banner content
        """
        lines = banner_content.split('\n')
        scaled_lines = []
        
        for line in lines:
            # Strip ANSI codes to measure actual width
            visible_line = self._strip_ansi(line)
            
            if len(visible_line) <= max_width:
                scaled_lines.append(line)
            else:
                # Truncate and add ellipsis
                # This is a simple truncation; preserving ANSI codes properly
                # would be more complex
                if max_width > 3:
                    scaled_lines.append(visible_line[:max_width - 3] + "...")
                else:
                    scaled_lines.append(visible_line[:max_width])
        
        return '\n'.join(scaled_lines)
    
    def _strip_ansi(self, text: str) -> str:
        """
        Strip ANSI escape codes from text.
        
        Args:
            text: Text with potential ANSI codes
            
        Returns:
            Text with ANSI codes removed
        """
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def _get_banner_width(self, banner_content: str) -> int:
        """
        Get the width of the banner content.
        
        Args:
            banner_content: Banner content
            
        Returns:
            Width in columns (max line width)
        """
        lines = banner_content.split('\n')
        max_width = 0
        
        for line in lines:
            visible_line = self._strip_ansi(line)
            max_width = max(max_width, len(visible_line))
        
        return max_width
    
    def render(self) -> None:
        """
        Render the banner based on the configured style.
        
        Handles animated, static, minimal, and none styles.
        Applies responsive scaling for narrow terminals.
        """
        if self.style == BannerStyle.NONE:
            return
        
        if self.style == BannerStyle.MINIMAL:
            self._render_minimal()
            return
        
        if self.style == BannerStyle.STATIC:
            self._render_static()
            return
        
        if self.style == BannerStyle.ANIMATED:
            self._render_animated()
            return
    
    def _render_minimal(self) -> None:
        """Render minimal banner (just version string)."""
        # Get version from package if available
        try:
            from mudhound import __version__
            version_str = f"MUDHOUND v{__version__}"
        except (ImportError, AttributeError):
            version_str = "MUDHOUND"
        
        self.output.write(version_str + "\n")
        self.output.flush()
    
    def _render_static(self) -> None:
        """Render static banner (no animation)."""
        # Load banner frames (will get static or first frame)
        frames = self.asset_manager.get_banner_frames(self.scheme)
        
        if not frames:
            self._render_minimal()
            return
        
        # Use first frame
        banner_content = frames[0]
        
        # Apply responsive scaling
        terminal_width = self._get_terminal_width()
        banner_width = self._get_banner_width(banner_content)
        
        if banner_width > terminal_width:
            banner_content = self._scale_banner(banner_content, terminal_width)
        
        self.output.write(banner_content + "\n")
        self.output.flush()
    
    def _render_animated(self) -> None:
        """Render animated banner with color cycling."""
        if self.animation_renderer is None:
            # Fall back to static if no animation renderer
            self._render_static()
            return
        
        # Load banner frames
        self.animation_renderer.load_banner_frames(self.scheme)
        
        if not self.animation_renderer.frames:
            self._render_minimal()
            return
        
        # Apply responsive scaling to all frames
        terminal_width = self._get_terminal_width()
        banner_width = self._get_banner_width(self.animation_renderer.frames[0])
        
        if banner_width > terminal_width:
            scaled_frames = [
                self._scale_banner(frame, terminal_width)
                for frame in self.animation_renderer.frames
            ]
            self.animation_renderer.load_frames(scaled_frames)
        
        # Render a single frame (for now, full animation would be in animate())
        self.animation_renderer.render_frame(0)
    
    def animate(self, duration: float = 0.0) -> None:
        """
        Animate the banner for the specified duration.
        
        Args:
            duration: Animation duration in seconds (0 = infinite loop)
        """
        if self.style != BannerStyle.ANIMATED or self.animation_renderer is None:
            self.render()
            return
        
        # Load banner frames
        self.animation_renderer.load_banner_frames(self.scheme)
        
        if not self.animation_renderer.frames:
            self._render_minimal()
            return
        
        # Apply responsive scaling
        terminal_width = self._get_terminal_width()
        banner_width = self._get_banner_width(self.animation_renderer.frames[0])
        
        if banner_width > terminal_width:
            scaled_frames = [
                self._scale_banner(frame, terminal_width)
                for frame in self.animation_renderer.frames
            ]
            self.animation_renderer.load_frames(scaled_frames)
        
        # Run animation
        self.animation_renderer.animate(duration=duration)
    
    def clear(self) -> None:
        """Clear the banner from the terminal."""
        if self.animation_renderer:
            self.animation_renderer.clear()
