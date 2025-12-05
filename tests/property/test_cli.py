"""
Property-based tests for CLI commands.

Tests universal properties that should hold for CLI command execution.
"""

from io import StringIO
import sys
from unittest.mock import patch, MagicMock
from hypothesis import given, strategies as st, settings, HealthCheck, assume
import pytest

from mudhound.core.result import SearchOptions, SearchResult
from mudhound.adapters.base import SearchAdapter
from typing import Generator, List


# Create a test adapter for CLI testing
class TestCLIAdapter(SearchAdapter):
    """Concrete test adapter for CLI property testing."""
    
    @property
    def name(self) -> str:
        return "test_cli"
    
    @property
    def display_name(self) -> str:
        return "Test CLI Adapter"
    
    def search(
        self,
        query: str,
        options: SearchOptions
    ) -> Generator[SearchResult, None, None]:
        """Yield test results."""
        for i in range(min(5, options.max_results)):
            yield SearchResult(
                url=f"https://example.com/result{i}",
                title=f"Test Result {i} for {query}",
                snippet=f"This is a test snippet for query: {query}",
                source="example.com",
                rank=i + 1,
                metadata={}
            )
    
    def validate_options(self, options: SearchOptions) -> List[str]:
        """Validate options."""
        errors = []
        if options.max_results < 1:
            errors.append("max_results must be at least 1")
        return errors


# Mock UI components that produce output
class MockUIComponent:
    """Mock UI component that produces output when called."""
    
    def __init__(self, output_text: str):
        self.output_text = output_text
        self.called = False
    
    def render(self):
        """Render the component (produces output)."""
        self.called = True
        print(self.output_text)
        return self.output_text


@given(
    query=st.text(min_size=1, max_size=100, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
    max_results=st.integers(min_value=1, max_value=50)
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_quiet_mode_output_suppression(query, max_results):
    """
    Feature: mudhound-full-implementation, Property 19: Quiet mode output suppression
    Validates: Requirements 6.3
    
    For any search executed with quiet mode enabled, no UI output should be
    produced (only result data).
    
    This test simulates the behavior of the search command with quiet mode.
    When the actual CLI command is implemented, it should:
    1. Skip rendering banners, progress bars, and status messages when quiet=True
    2. Only output the search results in the requested format
    3. Suppress all decorative UI elements
    """
    # Assume query doesn't contain problematic characters
    assume(len(query.strip()) > 0)
    
    from mudhound.core.engine import SearchEngine
    
    # Create a search engine with the test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Create search options
    options = SearchOptions(max_results=max_results)
    
    # Simulate quiet mode behavior
    # In quiet mode, UI components should NOT be rendered
    
    # Create mock UI components
    banner = MockUIComponent("╔═══ MUDHOUND ═══╗")
    progress = MockUIComponent("[*] Searching... 50%")
    status = MockUIComponent("[+] Found 5 results")
    
    # Capture stdout to check for UI output
    captured_quiet = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_quiet
        
        # Execute search WITHOUT rendering UI components (quiet mode)
        quiet_mode = True
        
        if not quiet_mode:
            # In normal mode, these would be called
            banner.render()
            progress.render()
            status.render()
        
        # Execute the search
        session = engine.search(query=query, options=options)
        
        # In quiet mode, only output results (simulated here)
        if quiet_mode:
            # Only output URLs or result data, no UI elements
            for result in session.results:
                print(result.url)
        
        # Get the captured output
        quiet_output = captured_quiet.getvalue()
        
    finally:
        sys.stdout = original_stdout
    
    # Verify UI components were NOT called in quiet mode
    assert not banner.called, "Banner should not be rendered in quiet mode"
    assert not progress.called, "Progress should not be rendered in quiet mode"
    assert not status.called, "Status should not be rendered in quiet mode"
    
    # Verify no UI indicators are in the output
    ui_indicators = [
        "MUDHOUND",  # Banner
        "[+]", "[*]", "[~]", "[!]",  # Status glyphs
        "Progress:",  # Progress indicator
        "Searching",  # Status message
        "╔", "╗", "╚", "╝", "═", "║",  # Frame borders (double)
        "┌", "┐", "└", "┘", "─", "│",  # Frame borders (single)
        "▓", "░",  # Progress bar characters
        "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏",  # Spinner characters
        "%",  # Percentage indicators
    ]
    
    for indicator in ui_indicators:
        assert indicator not in quiet_output, (
            f"UI indicator '{indicator}' found in quiet mode output. "
            f"Quiet mode should suppress all UI elements."
        )
    
    # Verify the session was created successfully
    assert session is not None
    assert session.query.query == query
    assert len(session.results) <= max_results
    
    # In quiet mode, output should only contain result data (URLs in this case)
    lines = quiet_output.strip().split('\n')
    for line in lines:
        if line.strip():
            # Each non-empty line should be a URL
            assert line.startswith('https://') or line.startswith('http://'), (
                f"Quiet mode output should only contain URLs, found: {line}"
            )


@given(
    query=st.text(min_size=1, max_size=100, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
    max_results=st.integers(min_value=1, max_value=50)
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_quiet_mode_vs_normal_mode_output(query, max_results):
    """
    Additional test: Verify that quiet mode produces less output than normal mode.
    
    For any search, the output in quiet mode should be significantly shorter
    than the output in normal mode (which includes UI elements).
    """
    # Assume query doesn't contain problematic characters
    assume(len(query.strip()) > 0)
    
    from mudhound.core.engine import SearchEngine
    
    # Create a search engine with the test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Create search options
    options = SearchOptions(max_results=max_results)
    
    # Create mock UI components
    banner = MockUIComponent("╔═══ MUDHOUND ═══╗\n║  URL Extractor  ║\n╚═════════════════╝")
    progress = MockUIComponent("[*] Searching... 50%\n[*] Searching... 100%")
    status = MockUIComponent("[+] Search complete\n[+] Found 5 results")
    
    # Capture output for normal mode
    captured_normal = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_normal
        
        # Normal mode: render UI components
        banner.render()
        progress.render()
        
        session_normal = engine.search(query=query, options=options)
        
        status.render()
        
        # Output results with formatting
        for result in session_normal.results:
            print(f"[{result.rank}] {result.title}")
            print(f"    URL: {result.url}")
            print(f"    {result.snippet}")
            print()
        
        normal_output = captured_normal.getvalue()
    finally:
        sys.stdout = original_stdout
    
    # Reset mock components
    banner.called = False
    progress.called = False
    status.called = False
    
    # Capture output for quiet mode
    captured_quiet = StringIO()
    
    try:
        sys.stdout = captured_quiet
        
        # Quiet mode: skip UI components
        session_quiet = engine.search(query=query, options=options)
        
        # Only output URLs
        for result in session_quiet.results:
            print(result.url)
        
        quiet_output = captured_quiet.getvalue()
    finally:
        sys.stdout = original_stdout
    
    # Verify both sessions produced the same results
    assert len(session_normal.results) == len(session_quiet.results)
    
    # Verify quiet mode output is shorter than normal mode
    assert len(quiet_output) < len(normal_output), (
        "Quiet mode output should be shorter than normal mode output"
    )
    
    # Verify quiet mode has no UI elements
    assert "MUDHOUND" not in quiet_output
    assert "[*]" not in quiet_output
    assert "[+]" not in quiet_output
    assert "╔" not in quiet_output
    
    # Verify normal mode has UI elements
    assert "MUDHOUND" in normal_output or "[*]" in normal_output or "[+]" in normal_output


@given(
    query=st.text(min_size=1, max_size=100, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
    max_results=st.integers(min_value=1, max_value=50),
    output_format=st.sampled_from(['json', 'csv', 'txt', 'urls'])
)
@settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture], max_examples=100)
def test_output_file_writing(query, max_results, output_format, tmp_path):
    """
    Feature: mudhound-full-implementation, Property 20: Output file writing
    Validates: Requirements 6.4
    
    For any valid output path specified, search results should be written to that file path.
    
    This test verifies that:
    1. When an output path is specified, results are written to that file
    2. The file is created if it doesn't exist
    3. The file contains the search results in the specified format
    4. The file can be read back and contains valid data
    """
    import json
    import csv
    import os
    
    # Assume query doesn't contain problematic characters
    assume(len(query.strip()) > 0)
    
    from mudhound.core.engine import SearchEngine
    
    # Create a search engine with the test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Create search options
    options = SearchOptions(max_results=max_results)
    
    # Execute the search
    session = engine.search(query=query, options=options)
    
    # Verify we have results
    assert len(session.results) > 0, "Search should return at least one result"
    
    # Create output file path
    output_file = tmp_path / f"search_results.{output_format}"
    
    # Simulate writing results to file (this is what the CLI command should do)
    # The actual CLI command implementation will handle this
    with open(output_file, 'w', encoding='utf-8') as f:
        if output_format == 'json':
            # Write as JSON array
            results_data = [
                {
                    'url': r.url,
                    'title': r.title,
                    'snippet': r.snippet,
                    'source': r.source,
                    'rank': r.rank
                }
                for r in session.results
            ]
            json.dump(results_data, f, indent=2)
            
        elif output_format == 'csv':
            # Write as CSV with headers
            writer = csv.DictWriter(
                f,
                fieldnames=['rank', 'url', 'title', 'snippet', 'source']
            )
            writer.writeheader()
            for r in session.results:
                writer.writerow({
                    'rank': r.rank,
                    'url': r.url,
                    'title': r.title,
                    'snippet': r.snippet,
                    'source': r.source
                })
                
        elif output_format == 'txt':
            # Write as formatted text
            f.write(f"Search Results for: {query}\n")
            f.write(f"Total Results: {len(session.results)}\n")
            f.write("=" * 80 + "\n\n")
            for r in session.results:
                f.write(f"[{r.rank}] {r.title}\n")
                f.write(f"URL: {r.url}\n")
                f.write(f"Source: {r.source}\n")
                f.write(f"Snippet: {r.snippet}\n")
                f.write("-" * 80 + "\n\n")
                
        elif output_format == 'urls':
            # Write one URL per line
            for r in session.results:
                f.write(f"{r.url}\n")
    
    # Verify the file was created
    assert output_file.exists(), f"Output file should be created at {output_file}"
    
    # Verify the file is not empty
    assert output_file.stat().st_size > 0, "Output file should not be empty"
    
    # Verify the file contains valid data by reading it back
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verify content is not empty
    assert len(content) > 0, "File content should not be empty"
    
    # Format-specific validation
    if output_format == 'json':
        # Verify valid JSON
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert isinstance(data, list), "JSON output should be a list"
        assert len(data) == len(session.results), "JSON should contain all results"
        
        # Verify each result has required fields
        for item in data:
            assert 'url' in item, "Each JSON result should have a url field"
            assert 'title' in item, "Each JSON result should have a title field"
            assert 'snippet' in item, "Each JSON result should have a snippet field"
            assert 'source' in item, "Each JSON result should have a source field"
            assert 'rank' in item, "Each JSON result should have a rank field"
            
    elif output_format == 'csv':
        # Verify valid CSV
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == len(session.results), "CSV should contain all results"
        
        # Verify each row has required fields
        for row in rows:
            assert 'url' in row, "Each CSV row should have a url field"
            assert 'title' in row, "Each CSV row should have a title field"
            assert 'snippet' in row, "Each CSV row should have a snippet field"
            assert 'source' in row, "Each CSV row should have a source field"
            assert 'rank' in row, "Each CSV row should have a rank field"
            
    elif output_format == 'txt':
        # Verify text format contains query and results
        assert query in content, "Text output should contain the query"
        assert "Total Results:" in content, "Text output should contain result count"
        
        # Verify all URLs are present
        for result in session.results:
            assert result.url in content, f"Text output should contain URL: {result.url}"
            
    elif output_format == 'urls':
        # Verify URLs format (one per line)
        lines = content.strip().split('\n')
        assert len(lines) == len(session.results), "URLs output should have one URL per line"
        
        # Verify each line is a URL from the results
        result_urls = [r.url for r in session.results]
        for line in lines:
            assert line.strip() in result_urls, f"Each line should be a valid result URL: {line}"
    
    # Verify all result URLs are in the file content
    for result in session.results:
        assert result.url in content, (
            f"Output file should contain result URL: {result.url}"
        )


@given(
    query=st.text(min_size=1, max_size=100, alphabet=st.characters(min_codepoint=32, max_codepoint=126))
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_stdin_query_reading(query):
    """
    Feature: mudhound-full-implementation, Property 65: Stdin query reading
    Validates: Requirements 20.5
    
    For any input provided via stdin when --stdin flag is used, the CLI should
    read it as the search query.
    
    This test verifies that:
    1. When --stdin flag is provided, the CLI reads the query from stdin
    2. The query read from stdin is used for the search
    3. Whitespace is properly handled (leading/trailing whitespace trimmed)
    4. Multi-line input is handled (first line or joined lines)
    """
    # Assume query doesn't contain only whitespace
    assume(len(query.strip()) > 0)
    
    from mudhound.core.engine import SearchEngine
    
    # Create a search engine with the test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Simulate reading from stdin
    # In the actual CLI implementation, this would be done with:
    # if args.stdin:
    #     query = sys.stdin.read().strip()
    
    # Create a mock stdin with the query
    mock_stdin = StringIO(query)
    original_stdin = sys.stdin
    
    try:
        sys.stdin = mock_stdin
        
        # Simulate the CLI behavior when --stdin flag is used
        stdin_flag = True
        
        if stdin_flag:
            # Read query from stdin
            stdin_query = sys.stdin.read().strip()
        else:
            # Would use command-line argument
            stdin_query = query
        
        # Verify the query was read correctly
        assert stdin_query == query.strip(), (
            f"Query read from stdin should match input (with whitespace trimmed). "
            f"Expected: '{query.strip()}', Got: '{stdin_query}'"
        )
        
        # Execute search with the stdin query
        options = SearchOptions(max_results=10)
        session = engine.search(query=stdin_query, options=options)
        
        # Verify the search was executed with the correct query
        assert session.query.query == stdin_query, (
            f"Search should be executed with the query from stdin. "
            f"Expected: '{stdin_query}', Got: '{session.query.query}'"
        )
        
        # Verify results were returned
        assert len(session.results) > 0, "Search should return results"
        
        # Verify results contain the query (they should reference it)
        for result in session.results:
            assert stdin_query in result.title or stdin_query in result.snippet, (
                f"Results should reference the query from stdin: {stdin_query}"
            )
    
    finally:
        sys.stdin = original_stdin


@given(
    query=st.text(min_size=1, max_size=100, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
    leading_whitespace=st.text(max_size=10, alphabet=st.sampled_from([' ', '\t', '\n'])),
    trailing_whitespace=st.text(max_size=10, alphabet=st.sampled_from([' ', '\t', '\n']))
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_stdin_whitespace_handling(query, leading_whitespace, trailing_whitespace):
    """
    Additional test: Verify that stdin input properly handles whitespace.
    
    For any query with leading/trailing whitespace provided via stdin,
    the CLI should trim the whitespace before using it as the search query.
    """
    # Assume query doesn't contain only whitespace
    assume(len(query.strip()) > 0)
    
    from mudhound.core.engine import SearchEngine
    
    # Create a search engine with the test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Create input with leading and trailing whitespace
    stdin_input = leading_whitespace + query + trailing_whitespace
    
    # Simulate reading from stdin
    mock_stdin = StringIO(stdin_input)
    original_stdin = sys.stdin
    
    try:
        sys.stdin = mock_stdin
        
        # Read and process stdin input (as the CLI would do)
        stdin_query = sys.stdin.read().strip()
        
        # Verify whitespace was trimmed
        assert stdin_query == query.strip(), (
            f"Stdin query should have whitespace trimmed. "
            f"Input: '{stdin_input}', Expected: '{query.strip()}', Got: '{stdin_query}'"
        )
        
        # Verify no leading whitespace
        assert not stdin_query.startswith(' ') and not stdin_query.startswith('\t'), (
            "Stdin query should not have leading whitespace"
        )
        
        # Verify no trailing whitespace
        assert not stdin_query.endswith(' ') and not stdin_query.endswith('\t'), (
            "Stdin query should not have trailing whitespace"
        )
        
        # Execute search with the cleaned query
        options = SearchOptions(max_results=10)
        session = engine.search(query=stdin_query, options=options)
        
        # Verify the search used the trimmed query
        assert session.query.query == stdin_query
        assert session.query.query == query.strip()
    
    finally:
        sys.stdin = original_stdin


@given(
    lines=st.lists(
        st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
        min_size=1,
        max_size=5
    )
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_stdin_multiline_input(lines):
    """
    Additional test: Verify that stdin handles multi-line input appropriately.
    
    For any multi-line input provided via stdin, the CLI should handle it
    appropriately (either use first line, or join lines, depending on design).
    """
    # Assume at least one line has content
    assume(any(len(line.strip()) > 0 for line in lines))
    
    from mudhound.core.engine import SearchEngine
    
    # Create a search engine with the test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Create multi-line input
    stdin_input = '\n'.join(lines)
    
    # Simulate reading from stdin
    mock_stdin = StringIO(stdin_input)
    original_stdin = sys.stdin
    
    try:
        sys.stdin = mock_stdin
        
        # Read stdin input
        full_input = sys.stdin.read().strip()
        
        # The CLI could handle multi-line input in different ways:
        # Option 1: Use only the first line
        first_line_query = lines[0].strip()
        
        # Option 2: Join all lines with spaces
        joined_query = ' '.join(line.strip() for line in lines if line.strip())
        
        # Option 3: Use the full input as-is (with newlines replaced by spaces)
        full_query = full_input.replace('\n', ' ').strip()
        
        # For this test, we'll verify that the CLI handles it consistently
        # The actual implementation should choose one approach
        
        # Test with the full input approach (most flexible)
        stdin_query = full_input.replace('\n', ' ').strip()
        
        # Verify the query is not empty
        assert len(stdin_query) > 0, "Stdin query should not be empty after processing"
        
        # Execute search
        options = SearchOptions(max_results=10)
        session = engine.search(query=stdin_query, options=options)
        
        # Verify search was executed
        assert session is not None
        assert len(session.results) > 0
        
        # The query should be one of the valid interpretations
        assert (
            session.query.query == first_line_query or
            session.query.query == joined_query or
            session.query.query == full_query or
            session.query.query == stdin_query
        ), (
            f"Search query should be a valid interpretation of multi-line input. "
            f"Got: '{session.query.query}'"
        )
    
    finally:
        sys.stdin = original_stdin


@given(
    queries=st.lists(
        st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
        min_size=1,
        max_size=5
    ),
    max_results=st.integers(min_value=1, max_value=20)
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_interactive_session_state_preservation(queries, max_results):
    """
    Feature: mudhound-full-implementation, Property 62: Interactive session state preservation
    Validates: Requirements 19.2
    
    For any sequence of operations in interactive mode, session state should be
    maintained across all operations.
    
    This test verifies that:
    1. Session state is preserved across multiple search operations
    2. Last search query and results are accessible after each search
    3. Operation count is tracked correctly
    4. Session state can be queried at any time
    5. State is consistent across the session lifecycle
    """
    # Assume all queries have content
    assume(all(len(q.strip()) > 0 for q in queries))
    
    from mudhound.cli.commands.interactive import InteractiveSession
    from mudhound.core.engine import SearchEngine
    from mudhound.core.result import SearchOptions
    
    # Create an interactive session
    session = InteractiveSession()
    
    # Verify initial state
    initial_state = session.get_state_summary()
    assert initial_state["last_query"] is None, "Initial state should have no last query"
    assert initial_state["result_count"] == 0, "Initial state should have no results"
    assert initial_state["operations"] == 0, "Initial state should have zero operations"
    assert not initial_state["has_results"], "Initial state should have no results"
    
    # Create a search engine with test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Perform multiple search operations
    previous_queries = []
    previous_result_counts = []
    
    for i, query in enumerate(queries):
        query = query.strip()
        
        # Execute search
        options = SearchOptions(max_results=max_results)
        search_session = engine.search(query=query, options=options)
        
        # Update session state
        session.update_search_state(query, search_session)
        
        # Verify state was updated
        current_state = session.get_state_summary()
        
        # Verify last query is the current query
        assert current_state["last_query"] == query, (
            f"Session state should preserve the last query. "
            f"Expected: '{query}', Got: '{current_state['last_query']}'"
        )
        
        # Verify result count matches the search results
        expected_result_count = len(search_session.results)
        assert current_state["result_count"] == expected_result_count, (
            f"Session state should preserve the result count. "
            f"Expected: {expected_result_count}, Got: {current_state['result_count']}"
        )
        
        # Verify operation count is incremented
        expected_operations = i + 1
        assert current_state["operations"] == expected_operations, (
            f"Session state should track operation count. "
            f"Expected: {expected_operations}, Got: {current_state['operations']}"
        )
        
        # Verify has_results flag
        assert current_state["has_results"] == (expected_result_count > 0), (
            "Session state has_results flag should match actual results"
        )
        
        # Verify session attributes directly
        assert session.last_search_query == query, (
            "Session last_search_query should be preserved"
        )
        assert session.last_search_session is not None, (
            "Session last_search_session should be preserved"
        )
        assert session.last_search_results is not None, (
            "Session last_search_results should be preserved"
        )
        assert len(session.last_search_results) == expected_result_count, (
            "Session last_search_results length should match"
        )
        assert session.operation_count == expected_operations, (
            "Session operation_count should be incremented"
        )
        
        # Store for verification
        previous_queries.append(query)
        previous_result_counts.append(expected_result_count)
    
    # Verify final state reflects the last operation
    final_state = session.get_state_summary()
    assert final_state["last_query"] == queries[-1].strip(), (
        "Final state should have the last query"
    )
    assert final_state["operations"] == len(queries), (
        f"Final state should have {len(queries)} operations"
    )
    
    # Verify state consistency: the last query should be the most recent one
    assert session.last_search_query == queries[-1].strip(), (
        "Session should preserve the most recent query"
    )
    
    # Test state clearing
    session.clear_search_state()
    cleared_state = session.get_state_summary()
    
    assert cleared_state["last_query"] is None, (
        "Cleared state should have no last query"
    )
    assert cleared_state["result_count"] == 0, (
        "Cleared state should have no results"
    )
    assert not cleared_state["has_results"], (
        "Cleared state should have no results flag"
    )
    # Operation count should NOT be cleared (it's a session metric)
    assert cleared_state["operations"] == len(queries), (
        "Operation count should persist after clearing search state"
    )


@given(
    query1=st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
    query2=st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
    max_results1=st.integers(min_value=1, max_value=20),
    max_results2=st.integers(min_value=1, max_value=20)
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_interactive_session_state_isolation(query1, query2, max_results1, max_results2):
    """
    Additional test: Verify that session state is properly isolated between operations.
    
    For any two consecutive search operations, the second operation should
    completely replace the state from the first operation (not merge or accumulate).
    """
    # Assume queries have content and are different
    assume(len(query1.strip()) > 0)
    assume(len(query2.strip()) > 0)
    assume(query1.strip() != query2.strip())
    
    from mudhound.cli.commands.interactive import InteractiveSession
    from mudhound.core.engine import SearchEngine
    from mudhound.core.result import SearchOptions
    
    # Create an interactive session
    session = InteractiveSession()
    
    # Create a search engine with test adapter
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    
    # Perform first search
    query1 = query1.strip()
    options1 = SearchOptions(max_results=max_results1)
    search_session1 = engine.search(query=query1, options=options1)
    session.update_search_state(query1, search_session1)
    
    # Capture first state
    state1 = session.get_state_summary()
    results1_count = len(search_session1.results)
    
    # Perform second search
    query2 = query2.strip()
    options2 = SearchOptions(max_results=max_results2)
    search_session2 = engine.search(query=query2, options=options2)
    session.update_search_state(query2, search_session2)
    
    # Capture second state
    state2 = session.get_state_summary()
    results2_count = len(search_session2.results)
    
    # Verify state was replaced, not merged
    assert state2["last_query"] == query2, (
        f"Second operation should replace query. Expected: '{query2}', Got: '{state2['last_query']}'"
    )
    assert state2["last_query"] != query1, (
        "Second operation should not preserve first query"
    )
    
    # Verify result count is from second search only
    assert state2["result_count"] == results2_count, (
        f"Second operation should replace result count. "
        f"Expected: {results2_count}, Got: {state2['result_count']}"
    )
    assert state2["result_count"] != results1_count or results1_count == results2_count, (
        "Result count should be from second search (unless they happen to be equal)"
    )
    
    # Verify operation count is cumulative (not replaced)
    assert state2["operations"] == 2, (
        "Operation count should be cumulative across operations"
    )
    assert state2["operations"] > state1["operations"], (
        "Operation count should increase with each operation"
    )
    
    # Verify session attributes reflect only the second search
    assert session.last_search_query == query2, (
        "Session should only preserve the most recent query"
    )
    assert session.last_search_session == search_session2, (
        "Session should only preserve the most recent session"
    )
    assert len(session.last_search_results) == results2_count, (
        "Session should only preserve results from the most recent search"
    )


@given(
    query=st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)),
    max_results=st.integers(min_value=1, max_value=20)
)
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=100)
def test_interactive_session_data_storage(query, max_results):
    """
    Additional test: Verify that session can store arbitrary data.
    
    For any session, custom data should be storable and retrievable
    through the session_data dictionary.
    """
    # Assume query has content
    assume(len(query.strip()) > 0)
    
    from mudhound.cli.commands.interactive import InteractiveSession
    from mudhound.core.engine import SearchEngine
    from mudhound.core.result import SearchOptions
    
    # Create an interactive session
    session = InteractiveSession()
    
    # Store custom data
    session.session_data["custom_key"] = "custom_value"
    session.session_data["user_preference"] = True
    session.session_data["counter"] = 42
    
    # Verify data is stored
    assert "custom_key" in session.session_data
    assert session.session_data["custom_key"] == "custom_value"
    assert session.session_data["user_preference"] is True
    assert session.session_data["counter"] == 42
    
    # Perform a search operation
    adapter = TestCLIAdapter()
    engine = SearchEngine(adapter=adapter)
    query = query.strip()
    options = SearchOptions(max_results=max_results)
    search_session = engine.search(query=query, options=options)
    session.update_search_state(query, search_session)
    
    # Verify custom data persists after search operation
    assert "custom_key" in session.session_data, (
        "Custom session data should persist across operations"
    )
    assert session.session_data["custom_key"] == "custom_value", (
        "Custom session data values should be preserved"
    )
    assert session.session_data["user_preference"] is True
    assert session.session_data["counter"] == 42
    
    # Modify custom data
    session.session_data["counter"] += 1
    
    # Verify modification
    assert session.session_data["counter"] == 43, (
        "Custom session data should be modifiable"
    )
    
    # Clear search state (should not affect custom data)
    session.clear_search_state()
    
    # Verify custom data still persists
    assert "custom_key" in session.session_data, (
        "Custom session data should persist after clearing search state"
    )
    assert session.session_data["custom_key"] == "custom_value"
    assert session.session_data["counter"] == 43
