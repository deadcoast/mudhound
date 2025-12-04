"""
Input validation utilities for prompts.

This module provides validators for different types of user input including
range validation, pattern matching, length constraints, enum validation,
and custom validation functions.
"""

import re
from typing import Optional, Callable, Any, List
from pathlib import Path


class Validator:
    """Base validator class."""
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validate a value.
        
        Args:
            value: Value to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        raise NotImplementedError


class RangeValidator(Validator):
    """Validates that a numeric value is within a specified range."""
    
    def __init__(self, min_value: Optional[float] = None, max_value: Optional[float] = None):
        """
        Initialize range validator.
        
        Args:
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)
        """
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate that value is within range."""
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return False, "Value must be a number"
        
        if self.min_value is not None and num_value < self.min_value:
            return False, f"Value must be at least {self.min_value}"
        
        if self.max_value is not None and num_value > self.max_value:
            return False, f"Value must be at most {self.max_value}"
        
        return True, None


class PatternValidator(Validator):
    """Validates that a string matches a regex pattern."""
    
    def __init__(self, pattern: str, error_message: Optional[str] = None):
        """
        Initialize pattern validator.
        
        Args:
            pattern: Regular expression pattern
            error_message: Custom error message (defaults to generic message)
        """
        self.pattern = re.compile(pattern)
        self.error_message = error_message or f"Value must match pattern: {pattern}"
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate that value matches pattern."""
        str_value = str(value)
        
        if self.pattern.match(str_value):
            return True, None
        
        return False, self.error_message


class LengthValidator(Validator):
    """Validates that a string has a length within specified bounds."""
    
    def __init__(self, min_length: Optional[int] = None, max_length: Optional[int] = None):
        """
        Initialize length validator.
        
        Args:
            min_length: Minimum allowed length (inclusive)
            max_length: Maximum allowed length (inclusive)
        """
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate that value length is within bounds."""
        str_value = str(value)
        length = len(str_value)
        
        if self.min_length is not None and length < self.min_length:
            return False, f"Value must be at least {self.min_length} characters"
        
        if self.max_length is not None and length > self.max_length:
            return False, f"Value must be at most {self.max_length} characters"
        
        return True, None


class EnumValidator(Validator):
    """Validates that a value is one of a set of allowed values."""
    
    def __init__(self, allowed_values: List[Any], case_sensitive: bool = True):
        """
        Initialize enum validator.
        
        Args:
            allowed_values: List of allowed values
            case_sensitive: Whether string comparison is case-sensitive
        """
        self.allowed_values = allowed_values
        self.case_sensitive = case_sensitive
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate that value is in allowed set."""
        if self.case_sensitive:
            if value in self.allowed_values:
                return True, None
        else:
            # Case-insensitive comparison for strings
            if isinstance(value, str):
                value_lower = value.lower()
                for allowed in self.allowed_values:
                    if isinstance(allowed, str) and allowed.lower() == value_lower:
                        return True, None
            elif value in self.allowed_values:
                return True, None
        
        allowed_str = ", ".join(str(v) for v in self.allowed_values)
        return False, f"Value must be one of: {allowed_str}"


class PathValidator(Validator):
    """Validates that a path exists or is valid."""
    
    def __init__(self, must_exist: bool = False, must_be_file: bool = False, must_be_dir: bool = False):
        """
        Initialize path validator.
        
        Args:
            must_exist: Whether path must exist
            must_be_file: Whether path must be a file
            must_be_dir: Whether path must be a directory
        """
        self.must_exist = must_exist
        self.must_be_file = must_be_file
        self.must_be_dir = must_be_dir
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate path."""
        try:
            path = Path(value)
        except (TypeError, ValueError):
            return False, "Invalid path"
        
        if self.must_exist and not path.exists():
            return False, "Path does not exist"
        
        if self.must_be_file and path.exists() and not path.is_file():
            return False, "Path must be a file"
        
        if self.must_be_dir and path.exists() and not path.is_dir():
            return False, "Path must be a directory"
        
        return True, None


class CustomValidator(Validator):
    """Validates using a custom function."""
    
    def __init__(self, func: Callable[[Any], tuple[bool, Optional[str]]]):
        """
        Initialize custom validator.
        
        Args:
            func: Validation function that returns (is_valid, error_message)
        """
        self.func = func
    
    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate using custom function."""
        return self.func(value)


__all__ = [
    "Validator",
    "RangeValidator",
    "PatternValidator",
    "LengthValidator",
    "EnumValidator",
    "PathValidator",
    "CustomValidator",
]
