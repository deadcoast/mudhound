"""
Animation rendering engine for terminal graphics.

This module provides the AnimationRenderer class which coordinates frame loading,
timing, and terminal rendering for animated ASCII art and UI elements.
"""

import sys
from typing import Callable, List, Optional, TextIO

from mudhound.assets.manager import AssetManager
from mudhound.ui.animation.timing import TimingEngine


class AnimationRenderer:
    """
    Coordinates animation rendering with cursor management and frame tracking.
    
    Integrates with TimingEngine for frame index calculation, AssetManager for
    frame loading, and handles terminal-specific rendering with cursor management.
    
    Attributes:
        timing_engine: TimingEngine instance for frame timing
        asset_manager: AssetManager instance for loading frames
        output: Output stream (defaults to stdout)
        frames: List of frame contents to animate
        previous_frame_height: Height of previously rendered frame for clearing
    """

    def __init__(
        self,
        timing_engine: Optional[TimingEngine] = None,
        asset_manager: Optional[AssetManager] = None,
        output: Optional[TextIO] = None
    ):
        """
        Initialize the animation renderer.
        
        Args:
            timing_engine: TimingEngine instance (creates default if None)
            asset_manager: AssetManager instance (creates default if None)
            output: Output stream (defaults to stdout)
        """
        self.timing_engine = timing_engine or TimingEngine()
        self.asset_manager = asset_manager or AssetManager()
        self.output = output or sys.stdout

        self.frames: List[str] = []
        self.previous_frame_height: int = 0
        self._is_paused = False

    @property
    def is_paused(self) -> bool:
        """Whether the animation is currently paused."""
        return self._is_paused

    def load_frames(self, frames: List[str]) -> None:
        """
        Load frames for animation.
        
        Args:
            frames: List of frame contents (strings)
        """
        self.frames = frames

        # Update timing engine with frame count
        if self.frames:
            self.timing_engine.total_frames = len(self.frames)

    def load_banner_frames(self, scheme: str = "rainbow") -> None:
        """
        Load banner frames from asset manager.
        
        Args:
            scheme: Color scheme name
        """
        frames = self.asset_manager.get_banner_frames(scheme)
        self.load_frames(frames)

    def load_logo_frames(self, scheme: str = "rainbow") -> None:
        """
        Load logo frames from asset manager.
        
        Args:
            scheme: Color scheme name
        """
        frames = self.asset_manager.get_logo_frames(scheme)
        self.load_frames(frames)

    def _count_lines(self, text: str) -> int:
        """
        Count the number of lines in a text string.
        
        Args:
            text: Text to count lines in
            
        Returns:
            Number of lines
        """
        if not text:
            return 0
        return text.count('\n') + 1

    def _clear_previous_frame(self) -> None:
        """Clear the previously rendered frame from the terminal."""
        if self.previous_frame_height > 0:
            # Move cursor up to the start of the previous frame
            self.output.write(f"\033[{self.previous_frame_height}A")

            # Clear each line
            for _ in range(self.previous_frame_height):
                self.output.write("\033[2K")  # Clear line
                if _ < self.previous_frame_height - 1:
                    self.output.write("\033[1B")  # Move down one line

            # Move cursor back to the start position
            self.output.write(f"\033[{self.previous_frame_height}A")

            self.output.flush()

    def render_frame(self, frame_index: Optional[int] = None) -> None:
        """
        Render a single frame with cursor management.
        
        Clears the previous frame by moving cursor up and clearing lines,
        then renders the new frame.
        
        Args:
            frame_index: Index of frame to render (uses timing engine if None)
        """
        if not self.frames:
            return

        # Get frame index from timing engine if not specified
        if frame_index is None:
            if self.timing_engine.is_running:
                frame_index = self.timing_engine.get_current_frame()
            else:
                frame_index = 0

        # Ensure frame index is valid
        frame_index = frame_index % len(self.frames)

        # Get the frame content
        frame_content = self.frames[frame_index]

        # Clear previous frame if any
        self._clear_previous_frame()

        # Render new frame
        self.output.write(frame_content)
        self.output.write("\n")
        self.output.flush()

        # Track frame height for next clear operation
        self.previous_frame_height = self._count_lines(frame_content)

    def pause(self) -> None:
        """
        Pause the animation.
        
        Pauses the timing engine and sets the paused flag.
        Used during terminal resize events.
        """
        if self.timing_engine.is_running and not self._is_paused:
            self.timing_engine.pause()
            self._is_paused = True

    def resume(self) -> None:
        """
        Resume the animation after pause.
        
        Resumes the timing engine and clears the paused flag.
        Used after terminal resize events are handled.
        """
        if self.timing_engine.is_running and self._is_paused:
            self.timing_engine.resume()
            self._is_paused = False

    def animate(
        self,
        duration: float = 0.0,
        on_complete: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Run the animation for the specified duration.
        
        Integrates with TimingEngine for frame index calculation and handles
        the animation loop with proper timing.
        
        Args:
            duration: Animation duration in seconds (0 = infinite loop)
            on_complete: Optional callback to invoke when animation completes
        """
        if not self.frames:
            return

        # Update timing engine duration
        self.timing_engine.duration = duration

        # Start the timing engine
        self.timing_engine.start()

        try:
            # Animation loop
            while self.timing_engine.is_running:
                # Check if animation is complete (for non-looping animations)
                if self.timing_engine.is_complete():
                    break

                # Skip rendering if paused
                if not self._is_paused:
                    # Render current frame
                    self.render_frame()

                # Sleep for frame duration to maintain frame rate
                import time
                time.sleep(self.timing_engine.frame_duration)

        finally:
            # Stop the timing engine
            self.timing_engine.stop()

            # Invoke completion callback if provided
            if on_complete:
                on_complete()

    def stop(self) -> None:
        """Stop the animation and clean up."""
        self.timing_engine.stop()
        self._is_paused = False

    def clear(self) -> None:
        """Clear the current frame from the terminal."""
        self._clear_previous_frame()
        self.previous_frame_height = 0
