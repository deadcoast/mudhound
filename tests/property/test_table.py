"""Property-based tests for table component."""

from io import StringIO

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from mudhound.core.result import SearchResult
from mudhound.ui.components.table import Table
from mudhound.ui.layout import LayoutManager


# Strategy for generating valid SearchResult objects
@st.composite
def search_result_strategy(draw):
    """Generate a valid SearchResult."""
    rank = draw(st.integers(min_value=1, max_value=1000))
    url = draw(st.text(min_size=10, max_size=200, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        whitelist_characters='.-_/:?=&'
    )))
    title = draw(st.text(min_size=5, max_size=100, alphabet=st.characters(
        blacklist_categories=('Cs', 'Cc')
    )))
    snippet = draw(st.text(min_size=10, max_size=300, alphabet=st.characters(
        blacklist_categories=('Cs', 'Cc')
    )))
    source = draw(st.text(min_size=3, max_size=50, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        whitelist_characters='.-_'
    )))

    return SearchResult(
        url=url,
        title=title,
        snippet=snippet,
        source=source,
        rank=rank,
        metadata={}
    )


@given(
    results=st.lists(search_result_strategy(), min_size=1, max_size=50)
)
@settings(max_examples=100, deadline=None)
def test_table_column_rendering(results):
    """
    Feature: mudhound-full-implementation, Property 38: Table column rendering
    
    For any search results displayed in a table, columns for rank, URL,
    and source should all be rendered.
    
    Validates: Requirements 13.1
    """
    # Create a layout manager with a reasonable terminal size
    layout_manager = LayoutManager()
    layout_manager._cached_size = (100, 24)

    # Create table
    table = Table(
        results=results,
        layout_manager=layout_manager,
        use_color=False,  # Disable color for easier testing
        output=StringIO()
    )

    # Render the table
    rendered_lines = table.render()

    # Verify we have at least header + separator + data rows
    assert len(rendered_lines) >= 3, "Table should have header, separator, and at least one data row"

    # Check header line (first line)
    header_line = rendered_lines[0]

    # Verify all three column names are present in the header
    assert "Rank" in header_line, "Header should contain 'Rank' column"
    assert "URL" in header_line, "Header should contain 'URL' column"
    assert "Source" in header_line, "Header should contain 'Source' column"

    # Check separator line (second line)
    separator_line = rendered_lines[1]
    assert "─" in separator_line or "-" in separator_line, "Separator line should contain horizontal line characters"

    # Check data rows (starting from line 3)
    data_lines = rendered_lines[2:]

    # Filter out empty lines and info lines
    actual_data_lines = [
        line for line in data_lines
        if line.strip() and not line.startswith("Filter:") and not line.startswith("Page")
    ]

    # Verify we have data rows
    assert len(actual_data_lines) > 0, "Table should have at least one data row"

    # For each result, verify its data appears in the table
    for result in results[:min(len(results), table.page_size)]:  # Only check first page
        # Check that rank appears somewhere in the rendered output
        rank_str = str(result.rank)
        found_rank = any(rank_str in line for line in actual_data_lines)
        assert found_rank, f"Rank {result.rank} should appear in table"

        # Check that URL appears (possibly truncated)
        # We check for at least the first 10 characters of the URL
        url_prefix = result.url[:min(10, len(result.url))]
        found_url = any(url_prefix in line for line in actual_data_lines)
        assert found_url, f"URL '{url_prefix}...' should appear in table"

        # Check that source appears (possibly truncated)
        source_prefix = result.source[:min(10, len(result.source))]
        found_source = any(source_prefix in line for line in actual_data_lines)
        assert found_source, f"Source '{source_prefix}...' should appear in table"


@given(
    results=st.lists(search_result_strategy(), min_size=1, max_size=20),
    terminal_width=st.integers(min_value=60, max_value=200)
)
@settings(max_examples=100, deadline=None)
def test_table_column_auto_sizing(results, terminal_width):
    """
    Feature: mudhound-full-implementation, Property 39: Table column auto-sizing
    
    For any content and terminal dimensions, table columns should be sized
    to fit within the terminal width.
    
    Validates: Requirements 13.2
    """
    # Create a layout manager with the specified terminal width
    layout_manager = LayoutManager()
    layout_manager._cached_size = (terminal_width, 24)

    # Create table
    table = Table(
        results=results,
        layout_manager=layout_manager,
        use_color=False,
        output=StringIO()
    )

    # Calculate column widths
    widths = table._calculate_column_widths()

    # Verify we have widths for all columns
    assert len(widths) == len(table.columns), "Should have width for each column"

    # Verify all widths are positive
    for width in widths:
        assert width > 0, f"Column width should be positive, got {width}"

    # Verify total width fits within terminal (accounting for separators and borders)
    total_width = sum(widths)
    separator_width = len(widths) - 1  # Spaces between columns
    frame_border_width = 4  # Frame borders

    total_used_width = total_width + separator_width + frame_border_width

    assert total_used_width <= terminal_width, (
        f"Total table width ({total_used_width}) should fit within terminal width ({terminal_width})"
    )

    # Verify each column respects its min/max constraints
    for i, (width, col) in enumerate(zip(widths, table.columns)):
        assert width >= col.min_width, (
            f"Column {col.name} width ({width}) should be >= min_width ({col.min_width})"
        )

        if col.max_width is not None:
            assert width <= col.max_width, (
                f"Column {col.name} width ({width}) should be <= max_width ({col.max_width})"
            )

        if col.width is not None:
            # Fixed width columns should have exact width
            assert width == col.width, (
                f"Fixed width column {col.name} should have width {col.width}, got {width}"
            )


@given(
    url=st.text(min_size=50, max_size=200, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        whitelist_characters='.-_/:?=&'
    )),
    column_width=st.integers(min_value=10, max_value=40)
)
@settings(max_examples=100, deadline=None)
def test_url_truncation_with_ellipsis(url, column_width):
    """
    Feature: mudhound-full-implementation, Property 40: URL truncation with ellipsis
    
    For any URL exceeding the column width, the table should truncate it
    and append ellipsis.
    
    Validates: Requirements 13.3
    """
    # Assume URL is longer than column width to test truncation
    assume(len(url) > column_width)

    # Create a simple result
    result = SearchResult(
        url=url,
        title="Test Title",
        snippet="Test snippet",
        source="test.com",
        rank=1,
        metadata={}
    )

    # Create a layout manager
    layout_manager = LayoutManager()
    layout_manager._cached_size = (100, 24)

    # Create table
    table = Table(
        results=[result],
        layout_manager=layout_manager,
        use_color=False,
        output=StringIO()
    )

    # Test the truncation method directly
    truncated = table._truncate_text(url, column_width)

    # Verify truncated text fits within width
    assert len(truncated) <= column_width, (
        f"Truncated text length ({len(truncated)}) should be <= column width ({column_width})"
    )

    # Verify ellipsis is present when text is truncated
    if len(url) > column_width:
        assert truncated.endswith("..."), (
            "Truncated text should end with ellipsis"
        )

        # Verify the truncated text contains the beginning of the original
        # (minus the ellipsis)
        prefix_length = column_width - 3  # Account for "..."
        if prefix_length > 0:
            expected_prefix = url[:prefix_length]
            actual_prefix = truncated[:-3]
            assert actual_prefix == expected_prefix, (
                f"Truncated text should preserve prefix: expected '{expected_prefix}', got '{actual_prefix}'"
            )

    # Also test in the context of rendering
    rendered_lines = table.render()

    # Find the data line (skip header and separator)
    data_lines = [line for line in rendered_lines[2:] if line.strip() and not line.startswith("Filter:")]

    if data_lines:
        data_line = data_lines[0]

        # The URL should appear in the line, possibly truncated
        # Check that if the full URL doesn't appear, then "..." appears
        if url not in data_line:
            assert "..." in data_line, (
                "If full URL doesn't appear, ellipsis should be present"
            )
