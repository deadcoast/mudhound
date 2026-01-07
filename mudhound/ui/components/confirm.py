"""
Confirmation component for destructive actions.

This module provides the Confirmation class for prompting users to confirm
actions, with special handling for destructive operations.
"""

import sys
import threading
import time
from enum import Enum
from typing import Optional, TextIO

from mudhound.ui.glyphs import GLYPHS
from mudhound.ui.theme import get_theme_engine


class ConfirmationVariant(Enum):
    """Confirmation variant types."""
    YESNO = "yesno"  # Standard yes/no, default NO
    YESNO_YES = "yesno_yes"  # Standard yes/no, default YES
    DESTRUCTIVE = "destructive"  # Requires typing confirmation word
    TIMED = "timed"  # Auto-cancels after timeout


class Confirmation:
    """
    Confirmation prompt component for destructive actions.
    
    Provides multiple confirmation variants with safety features:
    - yesno: Standard yes/no prompt, defaults to NO
    - yesno_yes: Standard yes/no prompt, defaults to YES
    - destructive: Requires typing a confirmation word
    - timed: Auto-cancels after timeout
    
    Attributes:
        message: Confirmation message to display
        variant: Type of confirmation (yesno, yesno_yes, destructive, timed)
        confirmation_word: Word to type for destructive variant
        timeout: Timeout in seconds for timed variant
        use_color: Whether to apply color codes
        output: Output stream for rendering
        input_stream: Input stream for reading user input
    """

    def __init__(
        self,
        message: str,
        variant: ConfirmationVariant = ConfirmationVariant.YESNO,
        confirmation_word: str = "DELETE",
        timeout: Optional[float] = None,
        use_color: bool = True,
        output: Optional[TextIO] = None,
        input_stream: Optional[TextIO] = None,
    ):
        """
        Initialize the Confirmation component.
        
        Args:
            message: Confirmation message to display
            variant: Type of confirmation
            confirmation_word: Word to type for destructive variant
            timeout: Timeout in seconds for timed variant
            use_color: Whether to apply ANSI color codes
            output: Output stream (defaults to stdout)
            input_stream: Input stream (defaults to stdin)
        """
        self.message = message
        self.variant = variant
        self.confirmation_word = confirmation_word
        self.timeout = timeout
        self.use_color = use_color
        self.output = output or sys.stdout
        self.input_stream = input_stream or sys.stdin
        self._timed_out = False

    def _format_message(self) -> str:
        """
        Format the confirmation message with appropriate styling.
        
        Returns:
            Formatted message string
        """
        # Add warning glyph for destructive actions
        if self.variant == ConfirmationVariant.DESTRUCTIVE:
            warning_glyph = GLYPHS["status"]["warning"]
            if self.use_color:
                theme_engine = get_theme_engine()
                warning_glyph = theme_engine.apply(warning_glyph, "warning")
                message = theme_engine.apply(self.message, "warning")
            else:
                message = self.message
            return f"{warning_glyph} {message}"
        else:
            if self.use_color:
                theme_engine = get_theme_engine()
                return theme_engine.apply(self.message, "info")
            return self.message

    def _format_prompt(self) -> str:
        """
        Format the prompt text based on variant.
        
        Returns:
            Formatted prompt string
        """
        if self.variant == ConfirmationVariant.DESTRUCTIVE:
            prompt = f"Type '{self.confirmation_word}' to confirm: "
        elif self.variant == ConfirmationVariant.YESNO_YES:
            prompt = "Continue? [Y/n]: "
        else:  # YESNO or TIMED
            prompt = "Continue? [y/N]: "

        if self.use_color:
            theme_engine = get_theme_engine()
            prompt = theme_engine.apply(prompt, "info")

        return prompt

    def _get_default_value(self) -> bool:
        """
        Get the default value based on variant.
        
        For destructive actions, default is NO.
        For yesno_yes, default is YES.
        For standard yesno and timed, default is NO.
        
        Returns:
            Default boolean value
        """
        if self.variant == ConfirmationVariant.YESNO_YES:
            return True
        else:
            # YESNO, DESTRUCTIVE, and TIMED all default to NO
            return False

    def _timeout_handler(self):
        """Handle timeout for timed variant."""
        if self.timeout:
            time.sleep(self.timeout)
            self._timed_out = True

    def _parse_yesno_input(self, raw_input: str) -> Optional[bool]:
        """
        Parse yes/no input.
        
        Args:
            raw_input: Raw input string
            
        Returns:
            Boolean value or None if invalid
        """
        lower_input = raw_input.lower().strip()

        if lower_input in ("y", "yes"):
            return True
        elif lower_input in ("n", "no"):
            return False
        else:
            return None

    def confirm(self) -> bool:
        """
        Display confirmation prompt and get user response.
        
        Handles different variants:
        - yesno: Standard yes/no with default NO
        - yesno_yes: Standard yes/no with default YES
        - destructive: Requires typing confirmation word
        - timed: Auto-cancels after timeout
        
        Returns:
            True if confirmed, False if cancelled
            
        Raises:
            KeyboardInterrupt: If user presses CTRL+C
        """
        # Display message
        self.output.write(self._format_message() + "\n")
        self.output.flush()

        # Start timeout thread for timed variant
        timeout_thread = None
        if self.variant == ConfirmationVariant.TIMED and self.timeout:
            self._timed_out = False
            timeout_thread = threading.Thread(target=self._timeout_handler, daemon=True)
            timeout_thread.start()

        try:
            while True:
                # Check if timed out
                if self._timed_out:
                    self.output.write("\nConfirmation timed out. Cancelled.\n")
                    self.output.flush()
                    return False

                # Display prompt
                self.output.write(self._format_prompt())
                self.output.flush()

                # Read input
                raw_input = self.input_stream.readline().strip()

                # Handle empty input with default
                if not raw_input:
                    return self._get_default_value()

                # Handle destructive variant
                if self.variant == ConfirmationVariant.DESTRUCTIVE:
                    if raw_input == self.confirmation_word:
                        return True
                    else:
                        error_msg = f"Confirmation word does not match. Expected '{self.confirmation_word}'."
                        if self.use_color:
                            theme_engine = get_theme_engine()
                            error_msg = theme_engine.apply(error_msg, "error")
                        self.output.write(error_msg + "\n")
                        self.output.flush()
                        continue

                # Handle yes/no variants
                else:
                    result = self._parse_yesno_input(raw_input)
                    if result is not None:
                        return result
                    else:
                        error_msg = "Invalid input. Please enter 'y' or 'n'."
                        if self.use_color:
                            theme_engine = get_theme_engine()
                            error_msg = theme_engine.apply(error_msg, "error")
                        self.output.write(error_msg + "\n")
                        self.output.flush()
                        continue

        except KeyboardInterrupt:
            # User pressed CTRL+C
            self.output.write("\n")
            self.output.flush()
            raise


__all__ = ["Confirmation", "ConfirmationVariant"]
