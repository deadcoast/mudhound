"""
Prompt component for user input with validation.

This module provides the Prompt class for collecting user input with
support for different input types and validation rules.
"""

import sys
from pathlib import Path
from typing import Any, List, Optional, TextIO

from mudhound.ui.glyphs import GLYPHS
from mudhound.ui.theme import get_theme_engine
from mudhound.utils.validators import (
    EnumValidator,
    PathValidator,
    RangeValidator,
    Validator,
)


class PromptType:
    """Prompt type constants."""

    TEXT = "text"
    NUMBER = "number"
    CHOICE = "choice"
    PATH = "path"
    CONFIRM = "confirm"


class Prompt:
    """
    Input prompt component with validation support.

    Supports multiple prompt types (text, number, choice, path, confirm)
    with configurable validation rules. Displays error messages and
    allows re-entry on validation failure.

    Attributes:
        prompt_text: Text to display as the prompt
        prompt_type: Type of prompt (text, number, choice, path, confirm)
        validators: List of validators to apply
        default: Default value if user provides no input
        use_color: Whether to apply color codes
        output: Output stream for rendering
        input_stream: Input stream for reading user input
    """

    def __init__(
        self,
        prompt_text: str,
        prompt_type: str = PromptType.TEXT,
        validators: Optional[List[Validator]] = None,
        default: Optional[Any] = None,
        use_color: bool = True,
        output: Optional[TextIO] = None,
        input_stream: Optional[TextIO] = None,
    ):
        """
        Initialize the Prompt component.

        Args:
            prompt_text: Text to display as the prompt
            prompt_type: Type of prompt (text, number, choice, path, confirm)
            validators: List of validators to apply to input
            default: Default value if user provides no input
            use_color: Whether to apply ANSI color codes
            output: Output stream (defaults to stdout)
            input_stream: Input stream (defaults to stdin)
        """
        self.prompt_text = prompt_text
        self.prompt_type = prompt_type
        self.validators = validators or []
        self.default = default
        self.use_color = use_color
        self.output = output or sys.stdout
        self.input_stream = input_stream or sys.stdin

    def _format_prompt(self) -> str:
        """
        Format the prompt text with cursor indicator.

        Returns:
            Formatted prompt string
        """
        # Add default value hint if present
        if self.default is not None:
            prompt = f"{self.prompt_text} [{self.default}]: "
        else:
            prompt = f"{self.prompt_text}: "

        # Apply color if enabled
        if self.use_color:
            theme_engine = get_theme_engine()
            prompt = theme_engine.apply(prompt, "info")

        return prompt

    def _format_error(self, error_message: str) -> str:
        """
        Format an error message.

        Args:
            error_message: Error message text

        Returns:
            Formatted error string
        """
        error_glyph = GLYPHS["status"]["error"]

        if self.use_color:
            theme_engine = get_theme_engine()
            error_glyph = theme_engine.apply(error_glyph, "error")
            error_message = theme_engine.apply(error_message, "error")

        return f"{error_glyph} {error_message}"

    def _validate_input(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validate input against all validators.

        Args:
            value: Input value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        for validator in self.validators:
            is_valid, error_message = validator.validate(value)
            if not is_valid:
                return False, error_message

        return True, None

    def _convert_value(self, raw_value: str) -> Any:
        """
        Convert raw input string to appropriate type.

        Args:
            raw_value: Raw input string

        Returns:
            Converted value

        Raises:
            ValueError: If conversion fails
        """
        if self.prompt_type == PromptType.NUMBER:
            # Try int first, then float
            try:
                return int(raw_value)
            except ValueError:
                return float(raw_value)

        elif self.prompt_type == PromptType.PATH:
            return Path(raw_value)

        elif self.prompt_type == PromptType.CONFIRM:
            # Convert to boolean
            lower_value = raw_value.lower()
            if lower_value in ("y", "yes", "true", "1"):
                return True
            elif lower_value in ("n", "no", "false", "0"):
                return False
            else:
                raise ValueError("Invalid confirmation value")

        else:
            # TEXT and CHOICE remain as strings
            return raw_value

    def prompt(self) -> Any:
        """
        Display the prompt and collect user input.

        Handles validation, error display, and re-entry on validation failure.
        Supports CTRL+C cancellation with KeyboardInterrupt.

        Returns:
            Validated user input

        Raises:
            KeyboardInterrupt: If user presses CTRL+C
        """
        while True:
            try:
                # Display prompt
                self.output.write(self._format_prompt())
                self.output.flush()

                # Read input
                raw_input = self.input_stream.readline().strip()

                # Handle empty input with default
                if not raw_input and self.default is not None:
                    return self.default

                # Handle empty input without default
                if not raw_input:
                    error_msg = self._format_error("Input cannot be empty")
                    self.output.write(error_msg + "\n")
                    self.output.flush()
                    continue

                # Convert value to appropriate type
                try:
                    value = self._convert_value(raw_input)
                except ValueError as e:
                    error_msg = self._format_error(f"Invalid input: {str(e)}")
                    self.output.write(error_msg + "\n")
                    self.output.flush()
                    continue

                # Validate input
                is_valid, error_message = self._validate_input(value)

                if is_valid:
                    return value
                else:
                    # Display error and allow re-entry
                    error_msg = self._format_error(error_message)
                    self.output.write(error_msg + "\n")
                    self.output.flush()

            except KeyboardInterrupt:
                # User pressed CTRL+C
                self.output.write("\n")
                self.output.flush()
                raise

    def prompt_text_input(self) -> str:
        """
        Prompt for text input.

        Returns:
            Text input string
        """
        self.prompt_type = PromptType.TEXT
        return self.prompt()

    def prompt_number(
        self, min_value: Optional[float] = None, max_value: Optional[float] = None
    ) -> float:
        """
        Prompt for numeric input.

        Args:
            min_value: Minimum allowed value
            max_value: Maximum allowed value

        Returns:
            Numeric input
        """
        self.prompt_type = PromptType.NUMBER

        # Add range validator if bounds specified
        if min_value is not None or max_value is not None:
            self.validators.append(RangeValidator(min_value, max_value))

        return self.prompt()

    def prompt_choice(self, choices: List[Any], case_sensitive: bool = True) -> Any:
        """
        Prompt for choice from a list of options.

        Args:
            choices: List of allowed choices
            case_sensitive: Whether comparison is case-sensitive

        Returns:
            Selected choice
        """
        self.prompt_type = PromptType.CHOICE

        # Add enum validator
        self.validators.append(EnumValidator(choices, case_sensitive))

        return self.prompt()

    def prompt_path(
        self, must_exist: bool = False, must_be_file: bool = False, must_be_dir: bool = False
    ) -> Path:
        """
        Prompt for file/directory path.

        Args:
            must_exist: Whether path must exist
            must_be_file: Whether path must be a file
            must_be_dir: Whether path must be a directory

        Returns:
            Path object
        """
        self.prompt_type = PromptType.PATH

        # Add path validator
        self.validators.append(PathValidator(
            must_exist, must_be_file, must_be_dir))

        return self.prompt()

    def prompt_confirm(self, default: Optional[bool] = None) -> bool:
        """
        Prompt for yes/no confirmation.

        Args:
            default: Default value if user provides no input

        Returns:
            Boolean confirmation
        """
        self.prompt_type = PromptType.CONFIRM
        self.default = default

        return self.prompt()


__all__ = ["Prompt", "PromptType"]
