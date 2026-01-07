"""
Property-based tests for terminal layout management.

Tests universal properties of the LayoutManager including content width
calculations and resize handling.
"""

from hypothesis import given
from hypothesis import strategies as st

from mudhound.ui.layout import LayoutManager


@given(
    terminal_width=st.integers(min_value=60, max_value=300),
    terminal_height=st.integers(min_value=10, max_value=100),
)
def test_content_width_calculation(terminal_width, terminal_height):
    """
    Feature: mudhound-full-implementation, Property 2: Content width calculation correctness

    For any terminal width, the calculated content width should equal terminal width
    minus frame borders minus padding (term_width - 4 for double borders with standard padding).

    Validates: Requirements 1.2
    """
    layout_manager = LayoutManager()

    # Mock the terminal size
    layout_manager._cached_size = (terminal_width, terminal_height)

    # Override get_terminal_size to return our test values
    original_get_size = layout_manager.get_terminal_size
    layout_manager.get_terminal_size = lambda: (
        terminal_width, terminal_height)

    try:
        content_width = layout_manager.get_content_width()

        # Content width should be terminal width minus border width (4 chars)
        expected_width = terminal_width - LayoutManager.BORDER_WIDTH
        assert content_width == expected_width

    finally:
        # Restore original method
        layout_manager.get_terminal_size = original_get_size


@given(
    initial_width=st.integers(min_value=60, max_value=200),
    initial_height=st.integers(min_value=10, max_value=80),
    new_width=st.integers(min_value=60, max_value=200),
    new_height=st.integers(min_value=10, max_value=80),
)
def test_resize_detection(initial_width, initial_height, new_width, new_height):
    """
    Test that resize detection correctly identifies terminal size changes.

    For any two different terminal sizes, detect_resize should return True
    when the size changes and False when it stays the same.
    """
    layout_manager = LayoutManager()

    # Track calls to get_terminal_size
    call_count = [0]
    sizes = [(initial_width, initial_height), (new_width, new_height)]

    def mock_get_size():
        idx = min(call_count[0], len(sizes) - 1)
        call_count[0] += 1
        return sizes[idx]

    layout_manager.get_terminal_size = mock_get_size

    # First call should not detect resize (initializes cache)
    first_check = layout_manager.detect_resize()
    assert first_check is False

    # Second call should detect resize only if size actually changed
    second_check = layout_manager.detect_resize()

    if (initial_width, initial_height) != (new_width, new_height):
        assert second_check is True
    else:
        assert second_check is False


@given(
    width=st.integers(min_value=60, max_value=300), height=st.integers(min_value=10, max_value=100)
)
def test_minimum_dimensions_enforcement(width, height):
    """
    Test that minimum dimension checking correctly validates terminal size.

    For any terminal size, check_minimum_dimensions should return True only
    when both width >= 60 and height >= 10.
    """
    layout_manager = LayoutManager()
    layout_manager.get_terminal_size = lambda: (width, height)

    result = layout_manager.check_minimum_dimensions()

    expected = width >= LayoutManager.MIN_WIDTH and height >= LayoutManager.MIN_HEIGHT
    assert result == expected


@given(
    terminal_width=st.integers(min_value=60, max_value=300),
    terminal_height=st.integers(min_value=10, max_value=100),
)
def test_content_height_calculation(terminal_width, terminal_height):
    """
    Test that content height accounts for top and bottom borders.

    For any terminal height, content height should be terminal height minus 2
    (for top and bottom borders).
    """
    layout_manager = LayoutManager()
    layout_manager.get_terminal_size = lambda: (
        terminal_width, terminal_height)

    content_height = layout_manager.get_content_height()

    # Content height should be terminal height minus 2 (top and bottom borders)
    expected_height = terminal_height - 2
    assert content_height == expected_height


@given(
    initial_width=st.integers(min_value=60, max_value=200),
    initial_height=st.integers(min_value=10, max_value=80),
    new_width=st.integers(min_value=60, max_value=200),
    new_height=st.integers(min_value=10, max_value=80),
)
def test_terminal_resize_triggers_rerender(initial_width, initial_height, new_width, new_height):
    """
    Feature: mudhound-full-implementation, Property 1: Terminal resize triggers re-render

    For any terminal resize event, all visible components should be re-rendered with
    dimensions recalculated to match the new terminal size.

    Validates: Requirements 1.1
    """
    layout_manager = LayoutManager()

    # Track if callbacks were invoked
    resize_callback_invoked = [False]
    animation_paused = [False]
    animation_resumed = [False]

    def resize_callback():
        resize_callback_invoked[0] = True

    def pause_animation():
        animation_paused[0] = True

    def resume_animation():
        animation_resumed[0] = True

    # Register callbacks
    layout_manager.register_resize_callback(resize_callback)
    layout_manager.set_animation_callbacks(
        pause_callback=pause_animation, resume_callback=resume_animation
    )

    # Mock terminal size changes
    call_count = [0]
    sizes = [(initial_width, initial_height), (new_width, new_height)]

    def mock_get_size():
        idx = min(call_count[0], len(sizes) - 1)
        call_count[0] += 1
        return sizes[idx]

    layout_manager.get_terminal_size = mock_get_size

    # First check initializes cache
    layout_manager.detect_resize()

    # Check and handle resize
    resize_detected = layout_manager.check_and_handle_resize()

    # If size changed, callbacks should have been invoked
    if (initial_width, initial_height) != (new_width, new_height):
        assert resize_detected is True
        assert resize_callback_invoked[0] is True
        assert animation_paused[0] is True
        assert animation_resumed[0] is True
    else:
        # If size didn't change, no callbacks should be invoked
        assert resize_detected is False
        assert resize_callback_invoked[0] is False
        assert animation_paused[0] is False
        assert animation_resumed[0] is False
