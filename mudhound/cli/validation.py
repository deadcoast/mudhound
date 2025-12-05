"""
CLI argument validation utilities.

Provides validation functions for command-line arguments to ensure
they meet requirements before command execution.
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple

from mudhound.adapters.registry import AdapterRegistry
from mudhound.core.exceptions import ValidationError


def validate_format(format_value: str) -> Tuple[bool, Optional[str]]:
    """Validate export format argument.
    
    Args:
        format_value: The format string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is None
        If invalid, error_message contains the error description
    """
    valid_formats = ['json', 'csv', 'txt', 'urls']
    
    if format_value not in valid_formats:
        return False, (
            f"Invalid format: {format_value}. "
            f"Must be one of: {', '.join(valid_formats)}"
        )
    
    return True, None


def validate_max_results(max_results: int) -> Tuple[bool, Optional[str]]:
    """Validate max_results argument.
    
    Args:
        max_results: The maximum number of results
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if max_results < 1:
        return False, f"max_results must be at least 1, got {max_results}"
    
    if max_results > 1000:
        return False, f"max_results must be at most 1000, got {max_results}"
    
    return True, None


def validate_engine(engine_name: str) -> Tuple[bool, Optional[str]]:
    """Validate search engine name.
    
    Args:
        engine_name: The engine name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Get available engines from registry
    try:
        available_engines = AdapterRegistry.list_available()
        
        if engine_name not in available_engines:
            return False, (
                f"Invalid engine: {engine_name}. "
                f"Available engines: {', '.join(available_engines)}"
            )
        
        return True, None
        
    except Exception as e:
        return False, f"Failed to validate engine: {e}"


def validate_region(region: str) -> Tuple[bool, Optional[str]]:
    """Validate region code.
    
    Args:
        region: The region code to validate (e.g., 'us-en', 'wt-wt')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Region codes should be in format: xx-xx (e.g., us-en, wt-wt)
    pattern = r'^[a-z]{2}-[a-z]{2}$'
    
    if not re.match(pattern, region):
        return False, (
            f"Invalid region format: {region}. "
            f"Expected format: xx-xx (e.g., us-en, wt-wt)"
        )
    
    return True, None


def validate_safesearch(safesearch: str) -> Tuple[bool, Optional[str]]:
    """Validate safesearch setting.
    
    Args:
        safesearch: The safesearch setting to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_values = ['off', 'moderate', 'strict']
    
    if safesearch not in valid_values:
        return False, (
            f"Invalid safesearch: {safesearch}. "
            f"Must be one of: {', '.join(valid_values)}"
        )
    
    return True, None


def validate_query(query: str) -> Tuple[bool, Optional[str]]:
    """Validate search query.
    
    Args:
        query: The search query to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not query or len(query.strip()) == 0:
        return False, "Query cannot be empty"
    
    if len(query) > 1000:
        return False, f"Query is too long ({len(query)} characters, max 1000)"
    
    return True, None


def validate_output_path(output_path: str) -> Tuple[bool, Optional[str]]:
    """Validate output file path.
    
    Args:
        output_path: The output path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import os
    
    if not output_path or len(output_path.strip()) == 0:
        return False, "Output path cannot be empty"
    
    # Check for invalid characters (platform-specific)
    if os.name == 'nt':  # Windows
        invalid_chars = ['<', '>', '"', '|', '?', '*']
        # Windows paths can have : in drive letters (C:)
        path_without_drive = (
            output_path[2:] if len(output_path) > 2 and output_path[1] == ':'
            else output_path
        )
        
        for char in invalid_chars:
            if char in path_without_drive:
                return False, f"Output path contains invalid character: {char}"
    
    # Check path length
    max_path_length = 260 if os.name == 'nt' else 4096
    if len(output_path) > max_path_length:
        return False, (
            f"Output path is too long ({len(output_path)} characters, "
            f"max {max_path_length})"
        )
    
    # Try to create a Path object
    try:
        path = Path(output_path)
        
        # Check if parent directory exists
        parent = path.parent
        if not parent.exists():
            return False, f"Parent directory does not exist: {parent}"
        
        # Check if parent is writable
        if not os.access(parent, os.W_OK):
            return False, f"Parent directory is not writable: {parent}"
        
        return True, None
        
    except (ValueError, OSError) as e:
        return False, f"Invalid output path: {e}"


def validate_limit(limit: int) -> Tuple[bool, Optional[str]]:
    """Validate limit argument for history list.
    
    Args:
        limit: The limit value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if limit < 1:
        return False, f"Limit must be at least 1, got {limit}"
    
    if limit > 10000:
        return False, f"Limit must be at most 10000, got {limit}"
    
    return True, None


def validate_all_arguments(
    query: Optional[str] = None,
    max_results: Optional[int] = None,
    engine: Optional[str] = None,
    region: Optional[str] = None,
    safesearch: Optional[str] = None,
    output_path: Optional[str] = None,
    format_value: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[str]:
    """Validate all provided arguments and return list of errors.
    
    Args:
        query: Search query (optional)
        max_results: Maximum results (optional)
        engine: Engine name (optional)
        region: Region code (optional)
        safesearch: Safesearch setting (optional)
        output_path: Output file path (optional)
        format_value: Export format (optional)
        limit: History limit (optional)
        
    Returns:
        List of error messages (empty if all valid)
    """
    errors = []
    
    if query is not None:
        is_valid, error = validate_query(query)
        if not is_valid:
            errors.append(error)
    
    if max_results is not None:
        is_valid, error = validate_max_results(max_results)
        if not is_valid:
            errors.append(error)
    
    if engine is not None:
        is_valid, error = validate_engine(engine)
        if not is_valid:
            errors.append(error)
    
    if region is not None:
        is_valid, error = validate_region(region)
        if not is_valid:
            errors.append(error)
    
    if safesearch is not None:
        is_valid, error = validate_safesearch(safesearch)
        if not is_valid:
            errors.append(error)
    
    if output_path is not None:
        is_valid, error = validate_output_path(output_path)
        if not is_valid:
            errors.append(error)
    
    if format_value is not None:
        is_valid, error = validate_format(format_value)
        if not is_valid:
            errors.append(error)
    
    if limit is not None:
        is_valid, error = validate_limit(limit)
        if not is_valid:
            errors.append(error)
    
    return errors
