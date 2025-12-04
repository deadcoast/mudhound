"""Layout management for responsive terminal UI."""

from typing import Tuple, Optional, Callable, List
from mudhound.utils.terminal import get_terminal_size


class LayoutManager:
    """
    Manages terminal layout dimensions and resize handling.
    
    Provides content width calculations, minimum dimension enforcement,
    and resize detection with callback support.
    """
    
    MIN_WIDTH = 60
    MIN_HEIGHT = 10
    BORDER_WIDTH = 4  # Double border (2 chars each side)
    
    def __init__(self):
        """Initialize the layout manager."""
        self._cached_size: Optional[Tuple[int, int]] = None
        self._resize_callbacks: List[Callable[[], None]] = []
        self._animation_pause_callback: Optional[Callable[[], None]] = None
        self._animation_resume_callback: Optional[Callable[[], None]] = None
    
    def get_terminal_size(self) -> Tuple[int, int]:
        """
        Get current terminal size.
        
        Returns cached size if available (for testing), otherwise queries actual terminal.
        
        Returns:
            Tuple[int, int]: (width, height) in columns and rows
        """
        if self._cached_size is not None:
            return self._cached_size
        return get_terminal_size()
    
    def get_content_width(self) -> int:
        """
        Calculate available content width accounting for borders and padding.
        
        Returns:
            int: Content width in columns
        """
        width, _ = self.get_terminal_size()
        return width - self.BORDER_WIDTH
    
    def get_content_height(self) -> int:
        """
        Calculate available content height accounting for borders.
        
        Returns:
            int: Content height in rows
        """
        _, height = self.get_terminal_size()
        # Account for top and bottom borders
        return height - 2
    
    def check_minimum_dimensions(self) -> bool:
        """
        Check if terminal meets minimum dimension requirements.
        
        Returns:
            bool: True if terminal is large enough
        """
        width, height = self.get_terminal_size()
        return width >= self.MIN_WIDTH and height >= self.MIN_HEIGHT
    
    def detect_resize(self) -> bool:
        """
        Detect if terminal has been resized since last check.
        
        Returns:
            bool: True if terminal size has changed
        """
        current_size = self.get_terminal_size()
        
        if self._cached_size is None:
            self._cached_size = current_size
            return False
        
        if current_size != self._cached_size:
            self._cached_size = current_size
            return True
        
        return False
    
    def register_resize_callback(self, callback: Callable[[], None]) -> None:
        """
        Register a callback to be invoked on terminal resize.
        
        Args:
            callback: Function to call when resize is detected
        """
        if callback not in self._resize_callbacks:
            self._resize_callbacks.append(callback)
    
    def unregister_resize_callback(self, callback: Callable[[], None]) -> None:
        """
        Unregister a resize callback.
        
        Args:
            callback: Function to remove from callbacks
        """
        if callback in self._resize_callbacks:
            self._resize_callbacks.remove(callback)
    
    def set_animation_callbacks(
        self,
        pause_callback: Optional[Callable[[], None]] = None,
        resume_callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Set callbacks for pausing/resuming animation on resize.
        
        Args:
            pause_callback: Function to pause animation
            resume_callback: Function to resume animation
        """
        self._animation_pause_callback = pause_callback
        self._animation_resume_callback = resume_callback
    
    def handle_resize(self) -> None:
        """
        Handle terminal resize event.
        
        Pauses animation, triggers callbacks, and resumes animation.
        """
        # Pause animation if callback is set
        if self._animation_pause_callback:
            self._animation_pause_callback()
        
        # Trigger all registered resize callbacks
        for callback in self._resize_callbacks:
            callback()
        
        # Resume animation if callback is set
        if self._animation_resume_callback:
            self._animation_resume_callback()
    
    def check_and_handle_resize(self) -> bool:
        """
        Check for resize and handle it if detected.
        
        Returns:
            bool: True if resize was detected and handled
        """
        if self.detect_resize():
            self.handle_resize()
            return True
        return False
