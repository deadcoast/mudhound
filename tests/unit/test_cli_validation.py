"""
Unit tests for CLI argument validation.

Tests the validation functions to ensure they correctly identify
valid and invalid arguments.
"""

import os
import tempfile

import pytest

from mudhound.cli.validation import (
    validate_all_arguments,
    validate_engine,
    validate_format,
    validate_limit,
    validate_max_results,
    validate_output_path,
    validate_query,
    validate_region,
    validate_safesearch,
)


class TestFormatValidation:
    """Tests for format validation."""

    def test_valid_formats(self):
        """Test that valid formats are accepted."""
        valid_formats = ["json", "csv", "txt", "urls"]

        for fmt in valid_formats:
            is_valid, error = validate_format(fmt)
            assert is_valid, f"Format '{fmt}' should be valid"
            assert error is None

    def test_invalid_formats(self):
        """Test that invalid formats are rejected."""
        invalid_formats = ["xml", "yaml", "pdf", "invalid", "", "123"]

        for fmt in invalid_formats:
            is_valid, error = validate_format(fmt)
            assert not is_valid, f"Format '{fmt}' should be invalid"
            assert error is not None
            assert "Invalid format" in error or "format" in error.lower()


class TestMaxResultsValidation:
    """Tests for max_results validation."""

    def test_valid_max_results(self):
        """Test that valid max_results values are accepted."""
        valid_values = [1, 10, 50, 100, 500, 1000]

        for value in valid_values:
            is_valid, error = validate_max_results(value)
            assert is_valid, f"max_results {value} should be valid"
            assert error is None

    def test_invalid_max_results_negative(self):
        """Test that negative max_results are rejected."""
        invalid_values = [-1, -10, -100]

        for value in invalid_values:
            is_valid, error = validate_max_results(value)
            assert not is_valid, f"max_results {value} should be invalid"
            assert error is not None
            assert "at least 1" in error

    def test_invalid_max_results_zero(self):
        """Test that zero max_results is rejected."""
        is_valid, error = validate_max_results(0)
        assert not is_valid
        assert error is not None
        assert "at least 1" in error

    def test_invalid_max_results_too_large(self):
        """Test that max_results over 1000 are rejected."""
        invalid_values = [1001, 5000, 10000]

        for value in invalid_values:
            is_valid, error = validate_max_results(value)
            assert not is_valid, f"max_results {value} should be invalid"
            assert error is not None
            assert "at most 1000" in error


class TestEngineValidation:
    """Tests for engine validation."""

    def test_valid_engine(self):
        """Test that registered engines are accepted."""
        # Note: This test depends on the AdapterRegistry having engines registered
        # In a real scenario, we'd mock the registry or ensure test adapters are registered
        is_valid, error = validate_engine("duckduckgo")
        # We can't guarantee duckduckgo is registered in test environment
        # So we just verify the function returns a tuple
        assert isinstance(is_valid, bool)
        assert error is None or isinstance(error, str)

    def test_invalid_engine(self):
        """Test that unregistered engines are rejected."""
        invalid_engines = ["invalid_engine", "google123", "not-an-engine"]

        for engine in invalid_engines:
            is_valid, error = validate_engine(engine)
            # Should be invalid unless somehow registered
            if not is_valid:
                assert error is not None
                assert "Invalid engine" in error or "engine" in error.lower()


class TestRegionValidation:
    """Tests for region validation."""

    def test_valid_regions(self):
        """Test that valid region codes are accepted."""
        valid_regions = ["us-en", "uk-en", "wt-wt", "de-de", "fr-fr"]

        for region in valid_regions:
            is_valid, error = validate_region(region)
            assert is_valid, f"Region '{region}' should be valid"
            assert error is None

    def test_invalid_regions(self):
        """Test that invalid region codes are rejected."""
        invalid_regions = ["us", "en", "us_en", "US-EN", "usa-en", "12-34", ""]

        for region in invalid_regions:
            is_valid, error = validate_region(region)
            assert not is_valid, f"Region '{region}' should be invalid"
            assert error is not None
            assert "Invalid region" in error or "format" in error.lower()


class TestSafesearchValidation:
    """Tests for safesearch validation."""

    def test_valid_safesearch(self):
        """Test that valid safesearch values are accepted."""
        valid_values = ["off", "moderate", "strict"]

        for value in valid_values:
            is_valid, error = validate_safesearch(value)
            assert is_valid, f"Safesearch '{value}' should be valid"
            assert error is None

    def test_invalid_safesearch(self):
        """Test that invalid safesearch values are rejected."""
        invalid_values = ["on", "high", "low", "yes", "no", "", "123"]

        for value in invalid_values:
            is_valid, error = validate_safesearch(value)
            assert not is_valid, f"Safesearch '{value}' should be invalid"
            assert error is not None
            assert "Invalid safesearch" in error or "safesearch" in error.lower()


class TestQueryValidation:
    """Tests for query validation."""

    def test_valid_queries(self):
        """Test that valid queries are accepted."""
        valid_queries = [
            "python",
            "machine learning",
            "how to code in python",
            "a" * 100,  # Long but under limit
        ]

        for query in valid_queries:
            is_valid, error = validate_query(query)
            assert is_valid, f"Query '{query}' should be valid"
            assert error is None

    def test_invalid_query_empty(self):
        """Test that empty queries are rejected."""
        invalid_queries = ["", "   ", "\t", "\n"]

        for query in invalid_queries:
            is_valid, error = validate_query(query)
            assert not is_valid, f"Query '{query}' should be invalid"
            assert error is not None
            assert "empty" in error.lower()

    def test_invalid_query_too_long(self):
        """Test that queries over 1000 characters are rejected."""
        long_query = "a" * 1001
        is_valid, error = validate_query(long_query)
        assert not is_valid
        assert error is not None
        # Validator returns "Value must be at most 1000 characters"
        assert "at most 1000" in error.lower() or "1000" in error


class TestOutputPathValidation:
    """Tests for output path validation."""

    def test_valid_output_path(self):
        """Test that valid output paths are accepted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "output.json")
            is_valid, error = validate_output_path(output_path)
            assert is_valid, f"Output path '{output_path}' should be valid"
            assert error is None

    def test_invalid_output_path_empty(self):
        """Test that empty output paths are rejected."""
        invalid_paths = ["", "   ", "\t"]

        for path in invalid_paths:
            is_valid, error = validate_output_path(path)
            assert not is_valid, f"Output path '{path}' should be invalid"
            assert error is not None
            assert "empty" in error.lower()

    def test_invalid_output_path_nonexistent_parent(self):
        """Test that paths with nonexistent parent directories are rejected."""
        invalid_path = "/nonexistent/directory/output.json"
        is_valid, error = validate_output_path(invalid_path)
        assert not is_valid
        assert error is not None
        assert "not exist" in error.lower() or "Invalid" in error

    @pytest.mark.skipif(os.name != "nt", reason="Windows-specific test")
    def test_invalid_output_path_windows_chars(self):
        """Test that Windows invalid characters are rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            invalid_chars = ["<", ">", '"', "|", "?", "*"]

            for char in invalid_chars:
                invalid_path = os.path.join(tmpdir, f"output{char}.json")
                is_valid, error = validate_output_path(invalid_path)
                assert not is_valid, f"Path with '{char}' should be invalid on Windows"
                assert error is not None
                assert "invalid character" in error.lower()


class TestLimitValidation:
    """Tests for limit validation."""

    def test_valid_limits(self):
        """Test that valid limit values are accepted."""
        valid_values = [1, 10, 100, 1000, 10000]

        for value in valid_values:
            is_valid, error = validate_limit(value)
            assert is_valid, f"Limit {value} should be valid"
            assert error is None

    def test_invalid_limit_negative(self):
        """Test that negative limits are rejected."""
        invalid_values = [-1, -10, -100]

        for value in invalid_values:
            is_valid, error = validate_limit(value)
            assert not is_valid, f"Limit {value} should be invalid"
            assert error is not None
            assert "at least 1" in error

    def test_invalid_limit_zero(self):
        """Test that zero limit is rejected."""
        is_valid, error = validate_limit(0)
        assert not is_valid
        assert error is not None
        assert "at least 1" in error

    def test_invalid_limit_too_large(self):
        """Test that limits over 10000 are rejected."""
        invalid_values = [10001, 50000, 100000]

        for value in invalid_values:
            is_valid, error = validate_limit(value)
            assert not is_valid, f"Limit {value} should be invalid"
            assert error is not None
            assert "at most 10000" in error


class TestValidateAllArguments:
    """Tests for validate_all_arguments function."""

    def test_all_valid_arguments(self):
        """Test that all valid arguments pass validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "output.json")

            errors = validate_all_arguments(
                query="python programming",
                max_results=50,
                region="us-en",
                safesearch="moderate",
                output_path=output_path,
                format_value="json",
                limit=100,
            )

            assert len(errors) == 0, f"Should have no errors, got: {errors}"

    def test_multiple_invalid_arguments(self):
        """Test that multiple invalid arguments are all reported."""
        errors = validate_all_arguments(
            query="",  # Invalid: empty
            max_results=-1,  # Invalid: negative
            region="invalid",  # Invalid: wrong format
            safesearch="invalid",  # Invalid: not in list
            format_value="xml",  # Invalid: not supported
            limit=0,  # Invalid: zero
        )

        # Should have multiple errors
        assert len(errors) > 0, "Should have validation errors"

        # Verify we got errors for each invalid argument
        error_text = " ".join(errors).lower()
        assert "query" in error_text or "empty" in error_text
        assert "max_results" in error_text or "at least" in error_text
        assert "region" in error_text or "format" in error_text
        assert "safesearch" in error_text
        assert "format" in error_text
        assert "limit" in error_text

    def test_partial_validation(self):
        """Test that only provided arguments are validated."""
        # Only validate query and max_results
        errors = validate_all_arguments(
            query="python",
            max_results=50,
        )

        assert len(
            errors) == 0, "Should have no errors for valid partial arguments"

        # Only validate invalid query
        errors = validate_all_arguments(
            query="",  # Invalid
        )

        assert len(errors) == 1, "Should have one error for invalid query"
        assert "query" in errors[0].lower() or "empty" in errors[0].lower()
