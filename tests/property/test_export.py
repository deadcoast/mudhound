"""
Property-based tests for export functionality.

Tests universal properties for the export system.
"""

import csv
import json
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from mudhound.cli.commands.export import (
    export_csv,
    export_json,
    export_txt,
    export_urls,
)
from mudhound.core.exceptions import ExportError
from mudhound.core.result import SearchResult


# Strategy for generating SearchResult instances
@st.composite
def search_result_strategy(draw):
    """Generate random SearchResult instances."""
    # Exclude control characters and line breaks to avoid issues with file formats
    safe_chars = st.characters(
        # Exclude control and surrogate characters
        blacklist_categories=("Cc", "Cs"),
        blacklist_characters="\r\n\t",  # Explicitly exclude line breaks and tabs
    )

    return SearchResult(
        url=draw(st.text(min_size=10, max_size=200, alphabet=safe_chars)),
        title=draw(st.text(min_size=1, max_size=100, alphabet=safe_chars)),
        snippet=draw(st.text(min_size=1, max_size=500, alphabet=safe_chars)),
        source=draw(st.text(min_size=1, max_size=50, alphabet=safe_chars)),
        rank=draw(st.integers(min_value=1, max_value=1000)),
        metadata=draw(
            st.dictionaries(
                st.text(min_size=1, max_size=20, alphabet=safe_chars),
                st.text(max_size=100, alphabet=safe_chars),
                max_size=5,
            )
        ),
    )


@given(results=st.lists(search_result_strategy(), min_size=1, max_size=50))
@settings(max_examples=100)
def test_json_export_round_trip(results):
    """
    Feature: mudhound-full-implementation, Property 29: JSON export round trip
    Validates: Requirements 9.1

    For any search results, exporting to JSON then parsing the JSON should
    produce equivalent result data.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "results.json"

        # Export to JSON
        export_json(results, output_path)

        # Verify file was created
        assert output_path.exists()

        # Parse the JSON back
        with open(output_path, encoding="utf-8") as f:
            parsed_data = json.load(f)

        # Verify we got the same number of results
        assert len(parsed_data) == len(results)

        # Verify each result matches
        for original, parsed in zip(results, parsed_data):
            assert parsed["url"] == original.url
            assert parsed["title"] == original.title
            assert parsed["snippet"] == original.snippet
            assert parsed["source"] == original.source
            assert parsed["rank"] == original.rank
            assert parsed["metadata"] == original.metadata


@given(results=st.lists(search_result_strategy(), min_size=1, max_size=50))
@settings(max_examples=100)
def test_csv_export_round_trip(results):
    """
    Feature: mudhound-full-implementation, Property 30: CSV export round trip
    Validates: Requirements 9.2

    For any search results, exporting to CSV then parsing the CSV should
    produce equivalent result data.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "results.csv"

        # Export to CSV
        export_csv(results, output_path)

        # Verify file was created
        assert output_path.exists()

        # Parse the CSV back
        with open(output_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            parsed_data = list(reader)

        # Verify we got the same number of results
        assert len(parsed_data) == len(results)

        # Verify each result matches (CSV stores everything as strings)
        for original, parsed in zip(results, parsed_data):
            assert parsed["url"] == original.url
            assert parsed["title"] == original.title
            assert parsed["snippet"] == original.snippet
            assert parsed["source"] == original.source
            assert int(parsed["rank"]) == original.rank


@given(results=st.lists(search_result_strategy(), min_size=1, max_size=50))
@settings(max_examples=100)
def test_urls_export_format(results):
    """
    Feature: mudhound-full-implementation, Property 31: URLs export format
    Validates: Requirements 9.4

    For any search results, exporting with format "urls" should produce
    one URL per line with no additional formatting.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "results.txt"

        # Export URLs
        export_urls(results, output_path)

        # Verify file was created
        assert output_path.exists()

        # Read the file back
        with open(output_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Verify we got the same number of lines as results
        assert len(lines) == len(results)

        # Verify each line contains only the URL (with newline)
        for original, line in zip(results, lines):
            assert line == f"{original.url}\n"
            # Verify no additional formatting (only one newline at the end)
            assert line.count("\n") == 1


@given(results=st.lists(search_result_strategy(), min_size=1, max_size=20))
@settings(max_examples=50)
def test_txt_export_contains_all_fields(results):
    """
    Test that TXT export includes all required fields in a readable format.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "results.txt"

        # Export to TXT
        export_txt(results, output_path)

        # Verify file was created
        assert output_path.exists()

        # Read the file back
        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Verify all results are present in the output
        for result in results:
            # Each result should have its rank, title, URL, source, and snippet
            assert f"[{result.rank}]" in content
            assert result.title in content
            assert result.url in content
            assert result.source in content
            assert result.snippet in content


def test_export_json_handles_empty_list():
    """
    Test that JSON export handles empty result list.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "empty.json"

        # Export empty list
        export_json([], output_path)

        # Verify file was created
        assert output_path.exists()

        # Parse the JSON back
        with open(output_path, encoding="utf-8") as f:
            parsed_data = json.load(f)

        # Should be an empty array
        assert parsed_data == []


def test_export_csv_handles_empty_list():
    """
    Test that CSV export handles empty result list.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "empty.csv"

        # Export empty list
        export_csv([], output_path)

        # Verify file was created
        assert output_path.exists()

        # Parse the CSV back
        with open(output_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            parsed_data = list(reader)

        # Should be empty (only headers)
        assert len(parsed_data) == 0


def test_export_urls_handles_empty_list():
    """
    Test that URLs export handles empty result list.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "empty.txt"

        # Export empty list
        export_urls([], output_path)

        # Verify file was created
        assert output_path.exists()

        # Read the file back
        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Should be empty
        assert content == ""


def test_export_json_raises_error_on_io_failure():
    """
    Test that JSON export raises ExportError on I/O failure.
    """
    # Try to write to an invalid path
    invalid_path = Path("/nonexistent/directory/results.json")

    result = SearchResult(
        url="https://example.com",
        title="Test",
        snippet="Test snippet",
        source="example.com",
        rank=1,
        metadata={},
    )

    with pytest.raises(ExportError) as exc_info:
        export_json([result], invalid_path)

    assert "Failed to write JSON file" in str(exc_info.value)


def test_export_csv_raises_error_on_io_failure():
    """
    Test that CSV export raises ExportError on I/O failure.
    """
    # Try to write to an invalid path
    invalid_path = Path("/nonexistent/directory/results.csv")

    result = SearchResult(
        url="https://example.com",
        title="Test",
        snippet="Test snippet",
        source="example.com",
        rank=1,
        metadata={},
    )

    with pytest.raises(ExportError) as exc_info:
        export_csv([result], invalid_path)

    assert "Failed to write CSV file" in str(exc_info.value)


def test_export_urls_raises_error_on_io_failure():
    """
    Test that URLs export raises ExportError on I/O failure.
    """
    # Try to write to an invalid path
    invalid_path = Path("/nonexistent/directory/results.txt")

    result = SearchResult(
        url="https://example.com",
        title="Test",
        snippet="Test snippet",
        source="example.com",
        rank=1,
        metadata={},
    )

    with pytest.raises(ExportError) as exc_info:
        export_urls([result], invalid_path)

    assert "Failed to write URLs file" in str(exc_info.value)
