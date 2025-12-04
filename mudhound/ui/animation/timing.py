"""Animation timing engine with easing functions and frame rate control."""

import time
from enum import Enum
from typing import Callable, Optional


class EasingFunction(Enum):
    """Available easing functions for animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"


class TimingEngine:
    """
    Controls animation timing with configurable FPS and easing functions.
    
    Manages frame rate control, start/stop/pause/resume operations, and
    calculates current frame index based on elapsed time.
    """
    
    def __init__(
        self,
        fps: int = 10,
        total_frames: int = 1,
        duration: float = 0.0,
        easing: EasingFunction = EasingFunction.LINEAR,
        loop: bool = True
    ):
        """
        Initialize the timing engine.
        
        Args:
            fps: Frames per second (default 10)
            total_frames: Total number of frames in the animation
            duration: Animation duration in seconds (0 = infinite loop)
            easing: Easing function to apply
            loop: Whether to loop continuously (True) or single-pass (False)
        """
        self.fps = fps
        self.total_frames = total_frames
        self.duration = duration
        self.easing = easing
        self.loop = loop
        
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._paused_duration: float = 0.0
        self._is_running = False
        self._is_paused = False
    
    @property
    def frame_duration(self) -> float:
        """Duration of a single frame in seconds."""
        return 1.0 / self.fps if self.fps > 0 else 0.0
    
    @property
    def is_running(self) -> bool:
        """Whether the animation is currently running."""
        return self._is_running
    
    @property
    def is_paused(self) -> bool:
        """Whether the animation is currently paused."""
        return self._is_paused
    
    def start(self) -> None:
        """Start the animation timer."""
        if not self._is_running:
            self._start_time = time.time()
            self._paused_duration = 0.0
            self._is_running = True
            self._is_paused = False
    
    def stop(self) -> None:
        """Stop the animation timer and reset state."""
        self._start_time = None
        self._pause_time = None
        self._paused_duration = 0.0
        self._is_running = False
        self._is_paused = False
    
    def pause(self) -> None:
        """Pause the animation timer."""
        if self._is_running and not self._is_paused:
            self._pause_time = time.time()
            self._is_paused = True
    
    def resume(self) -> None:
        """Resume the animation timer after pause."""
        if self._is_running and self._is_paused and self._pause_time is not None:
            self._paused_duration += time.time() - self._pause_time
            self._pause_time = None
            self._is_paused = False
    
    def get_elapsed_time(self) -> float:
        """
        Get the elapsed time since animation start, excluding paused time.
        
        Returns:
            Elapsed time in seconds, or 0.0 if not running
        """
        if not self._is_running or self._start_time is None:
            return 0.0
        
        current_time = time.time()
        
        if self._is_paused and self._pause_time is not None:
            # If paused, use pause time as current time
            elapsed = self._pause_time - self._start_time - self._paused_duration
        else:
            # If running, use actual current time
            elapsed = current_time - self._start_time - self._paused_duration
        
        return max(0.0, elapsed)
    
    def get_current_frame(self) -> int:
        """
        Calculate the current frame index based on elapsed time.
        
        Returns:
            Current frame index (0-based)
        """
        if not self._is_running:
            return 0
        
        elapsed = self.get_elapsed_time()
        
        # Handle infinite loop (duration = 0)
        if self.duration == 0.0:
            # Continuous loop based on frame rate
            frame_index = int(elapsed / self.frame_duration) % self.total_frames
            return frame_index
        
        # Handle finite duration
        if elapsed >= self.duration:
            if self.loop:
                # Loop back to beginning
                elapsed = elapsed % self.duration
            else:
                # Single-pass: stay at last frame
                return self.total_frames - 1
        
        # Calculate progress (0.0 to 1.0)
        progress = elapsed / self.duration if self.duration > 0 else 0.0
        progress = min(1.0, max(0.0, progress))
        
        # Apply easing function
        eased_progress = self._apply_easing(progress)
        
        # Calculate frame index
        frame_index = int(eased_progress * (self.total_frames - 1))
        return min(frame_index, self.total_frames - 1)
    
    def is_complete(self) -> bool:
        """
        Check if the animation has completed.
        
        Returns:
            True if animation is complete (only for non-looping animations)
        """
        if not self._is_running or self.loop or self.duration == 0.0:
            return False
        
        elapsed = self.get_elapsed_time()
        return elapsed >= self.duration
    
    def _apply_easing(self, t: float) -> float:
        """
        Apply the configured easing function to a progress value.
        
        Args:
            t: Progress value from 0.0 to 1.0
            
        Returns:
            Eased progress value from 0.0 to 1.0
        """
        if self.easing == EasingFunction.LINEAR:
            return self._ease_linear(t)
        elif self.easing == EasingFunction.EASE_IN:
            return self._ease_in(t)
        elif self.easing == EasingFunction.EASE_OUT:
            return self._ease_out(t)
        elif self.easing == EasingFunction.EASE_IN_OUT:
            return self._ease_in_out(t)
        elif self.easing == EasingFunction.BOUNCE:
            return self._ease_bounce(t)
        else:
            return t
    
    @staticmethod
    def _ease_linear(t: float) -> float:
        """Linear easing (no easing)."""
        return t
    
    @staticmethod
    def _ease_in(t: float) -> float:
        """Ease in (quadratic)."""
        return t * t
    
    @staticmethod
    def _ease_out(t: float) -> float:
        """Ease out (quadratic)."""
        return t * (2 - t)
    
    @staticmethod
    def _ease_in_out(t: float) -> float:
        """Ease in-out (quadratic)."""
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t
    
    @staticmethod
    def _ease_bounce(t: float) -> float:
        """Bounce easing."""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375
