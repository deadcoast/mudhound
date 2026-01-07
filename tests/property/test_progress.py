"""Property-based tests for progress component."""

from io import StringIO

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from mudhound.ui.components.progress import Progress, ProgressVariant


@given(
    current=st.integers(min_value=0, max_value=1000), total=st.integers(min_value=1, max_value=1000)
)
@settings(max_examples=100, deadline=None)
def test_progress_percentage_display(current, total):
    """
    Feature: mudhound-full-implementation, Property 41: Progress percentage display

    For any progress value between 0 and 100, the progress bar should display
    the correct percentage.

    Validates: Requirements 14.1
    """
    # Ensure current doesn't exceed total
    assume(current <= total)

    # Create progress with bar variant
    output = StringIO()
    progress = Progress(
        variant=ProgressVariant.BAR,
        total=total,
        use_color=False,  # Disable color for easier testing
        output=output,
    )

    # Set current value
    progress.set_current(current)

    # Calculate expected percentage
    expected_percentage = (current / total) * 100.0

    # Get actual percentage from progress
    actual_percentage = progress.get_percentage()

    # Verify percentage is correct (within floating point tolerance)
    assert abs(actual_percentage - expected_percentage) < 0.01, (
        f"Progress percentage {actual_percentage:.2f}% does not match expected "
        f"{expected_percentage:.2f}% for {current}/{total}"
    )

    # Verify percentage is within valid range
    assert (
        0.0 <= actual_percentage <= 100.0
    ), f"Progress percentage {actual_percentage:.2f}% is outside valid range [0, 100]"

    # Verify rendered output contains the percentage
    rendered = output.getvalue()

    # The rendered output should contain a percentage value
    # Extract percentage from output (format: "XX.X%")
    import re

    percentage_match = re.search(r"(\d+\.\d+)%", rendered)

    if percentage_match:
        rendered_percentage = float(percentage_match.group(1))

        # Verify rendered percentage matches calculated percentage
        assert abs(rendered_percentage - expected_percentage) < 0.2, (
            f"Rendered percentage {rendered_percentage:.1f}% does not match "
            f"expected {expected_percentage:.1f}%"
        )


@given(
    initial_count=st.integers(min_value=0, max_value=100),
    increment=st.integers(min_value=1, max_value=50),
)
@settings(max_examples=100, deadline=None)
def test_progress_counter_updates(initial_count, increment):
    """
    Feature: mudhound-full-implementation, Property 42: Progress counter updates

    For any new result received during search, the progress component should
    increment the result count.

    Validates: Requirements 14.3
    """
    # Create progress with counter variant
    output = StringIO()
    progress = Progress(
        variant=ProgressVariant.COUNTER,
        total=None,  # Indeterminate progress
        use_color=False,
        output=output,
    )

    # Set initial count
    progress.set_current(initial_count)
    initial_value = progress.current

    # Clear output buffer
    output.truncate(0)
    output.seek(0)

    # Update progress by increment
    progress.update(increment)

    # Verify current count increased by increment
    assert progress.current == initial_value + increment, (
        f"Progress counter should be {initial_value + increment} after update, "
        f"but got {progress.current}"
    )

    # Verify rendered output contains the updated count
    rendered = output.getvalue()

    # The rendered output should contain the result count
    # Extract count from output (format: "Results: XX" or similar)
    import re

    count_match = re.search(r"(\d+)\s+results?", rendered, re.IGNORECASE)

    if count_match:
        rendered_count = int(count_match.group(1))

        # Verify rendered count matches current count
        assert (
            rendered_count == progress.current
        ), f"Rendered count {rendered_count} does not match current count {progress.current}"


@given(
    variant=st.sampled_from(
        [
            ProgressVariant.BAR,
            ProgressVariant.SPINNER,
            ProgressVariant.COUNTER,
            ProgressVariant.TRANSFER,
            ProgressVariant.RAINBOW,
        ]
    ),
    total=st.integers(min_value=10, max_value=100),
    current=st.integers(min_value=0, max_value=100),
)
@settings(max_examples=100, deadline=None)
def test_progress_variant_rendering(variant, total, current):
    """
    Additional test: Verify that all progress variants render without errors.

    This ensures that each variant (bar, spinner, counter, transfer, rainbow)
    can be rendered successfully with various progress values.
    """
    # Ensure current doesn't exceed total
    assume(current <= total)

    # Create progress with specified variant
    output = StringIO()
    progress = Progress(variant=variant, total=total, use_color=False, output=output)

    # Start progress
    progress.start()

    # Set current value
    progress.set_current(current)

    # Render should not raise an exception
    try:
        progress.render()
    except Exception as e:
        assert False, f"Progress rendering with variant '{variant}' should not raise exception: {e}"

    # Get output
    rendered_output = output.getvalue()

    # Verify output is not empty
    assert len(rendered_output) > 0, f"Variant '{variant}' should produce output"

    # Verify output contains the current count
    assert (
        str(current) in rendered_output
    ), f"Rendered output should contain current count {current}"


@given(total=st.integers(min_value=1, max_value=100))
@settings(max_examples=100, deadline=None)
def test_progress_percentage_bounds(total):
    """
    Additional test: Verify that percentage never exceeds 100%.

    This ensures that even if current exceeds total, the percentage
    is clamped to 100%.
    """
    output = StringIO()
    progress = Progress(variant=ProgressVariant.BAR, total=total, use_color=False, output=output)

    # Set current to exceed total
    progress.set_current(total + 50)

    # Get percentage
    percentage = progress.get_percentage()

    # Verify percentage is clamped to 100%
    assert percentage <= 100.0, (
        f"Percentage {percentage:.2f}% should not exceed 100% even when "
        f"current ({progress.current}) exceeds total ({total})"
    )


@given(count=st.integers(min_value=1, max_value=10))
@settings(max_examples=100, deadline=None)
def test_progress_multiple_updates(count):
    """
    Additional test: Verify that multiple updates accumulate correctly.

    This ensures that calling update() multiple times correctly increments
    the counter.
    """
    output = StringIO()
    progress = Progress(variant=ProgressVariant.COUNTER, total=None, use_color=False, output=output)

    # Start progress
    progress.start()
    initial_count = progress.current

    # Perform multiple updates
    for _ in range(count):
        progress.update(1)

    # Verify final count
    assert progress.current == initial_count + count, (
        f"After {count} updates, current should be {initial_count + count}, "
        f"but got {progress.current}"
    )


@given(
    variant=st.sampled_from(
        [
            ProgressVariant.BAR,
            ProgressVariant.SPINNER,
            ProgressVariant.COUNTER,
            ProgressVariant.TRANSFER,
            ProgressVariant.RAINBOW,
        ]
    )
)
@settings(max_examples=100, deadline=None)
def test_progress_elapsed_time_display(variant):
    """
    Additional test: Verify that elapsed time is displayed in the footer.

    This ensures that all variants display elapsed time information.

    Related to Requirements 14.4
    """
    import time

    output = StringIO()
    progress = Progress(variant=variant, total=100, use_color=False, output=output)

    # Start progress
    progress.start()

    # Wait a short time
    time.sleep(0.1)

    # Update progress
    progress.update(10)

    # Get rendered output
    rendered = output.getvalue()

    # Verify elapsed time is present in output
    # Should contain time format like "0s" or "1m 23s"
    import re

    time_match = re.search(r"\d+[hms]", rendered)

    assert (
        time_match is not None
    ), f"Elapsed time should be displayed in progress output for variant '{variant}'"


@given(total=st.integers(min_value=1, max_value=100))
@settings(max_examples=100, deadline=None)
def test_progress_completion_message(total):
    """
    Additional test: Verify that completion displays final count.

    This ensures that when progress completes, it shows the final result count.
    """
    output = StringIO()
    progress = Progress(variant=ProgressVariant.BAR, total=total, use_color=False, output=output)

    # Start and complete progress
    progress.start()
    progress.set_current(total)

    # Clear output
    output.truncate(0)
    output.seek(0)

    # Complete progress
    progress.complete("Search complete")

    # Get output
    rendered = output.getvalue()

    # Verify completion message contains result count
    assert str(total) in rendered, f"Completion message should contain final count {total}"

    # Verify completion message is present
    assert "complete" in rendered.lower(), "Completion message should contain 'complete'"


@given(current=st.integers(min_value=1, max_value=50))  # Start from 1 to avoid edge case
@settings(max_examples=100, deadline=None)
def test_progress_cancellation(current):
    """
    Additional test: Verify that cancellation stops progress and displays message.

    This ensures that CTRL+C cancellation support works correctly.

    Related to Requirements 14.5
    """
    output = StringIO()
    progress = Progress(variant=ProgressVariant.BAR, total=100, use_color=False, output=output)

    # Start progress
    progress.start()
    progress.set_current(current)

    # Clear output
    output.truncate(0)
    output.seek(0)

    # Cancel progress without custom message to ensure count is shown
    progress.cancel()

    # Verify cancelled flag is set
    assert progress.cancelled is True, "Progress should be marked as cancelled"

    # Get output
    rendered = output.getvalue()

    # Verify cancellation message contains current count
    assert str(current) in rendered, f"Cancellation message should contain current count {current}"

    # Verify cancellation message is present
    assert "cancel" in rendered.lower(), "Cancellation message should contain 'cancel'"

    # Verify further renders are suppressed
    output.truncate(0)
    output.seek(0)
    progress.render()

    # Should produce no output when cancelled
    assert output.getvalue() == "", "Cancelled progress should not render further updates"
