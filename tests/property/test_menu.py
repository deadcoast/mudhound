"""Property-based tests for menu component."""

from io import StringIO

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from mudhound.ui.components.menu import Menu


@given(
    options=st.lists(
        st.text(min_size=1, max_size=50, alphabet=st.characters(
            blacklist_categories=("Cs", "Cc"))),
        min_size=1,
        max_size=20,
        unique=True,
    ),
    selected_index=st.integers(min_value=0, max_value=19),
)
@settings(max_examples=100, deadline=None)
def test_menu_option_numbering(options, selected_index):
    """
    Feature: mudhound-full-implementation, Property 34: Menu option numbering

    For any menu displayed, all options should be numbered sequentially
    and a cursor indicator should be visible.

    Validates: Requirements 11.1
    """
    # Ensure selected_index is valid for the options list
    assume(selected_index < len(options))

    # Create output stream
    output = StringIO()

    # Create menu
    menu = Menu(
        options=options,
        selected_index=selected_index,
        use_color=False,  # Disable color for easier testing
        output=output,
    )

    # Render the menu
    rendered_menu = menu._render_menu()

    # Verify all options are numbered sequentially (1-based)
    for i, option in enumerate(options):
        option_number = i + 1

        # Check that the option number appears in the rendered menu
        assert f"{option_number}." in rendered_menu, (
            f"Option {option_number} should be numbered in the menu"
        )

        # Check that the option text appears in the rendered menu
        assert option in rendered_menu, f"Option text '{option}' should appear in the menu"

    # Verify cursor indicator is present for selected option
    # The cursor indicator should be ">>>" (from GLYPHS)
    lines = rendered_menu.split("\n")

    # Count how many lines have the cursor indicator
    cursor_count = sum(1 for line in lines if ">>>" in line)

    # Exactly one option should have the cursor indicator
    assert cursor_count == 1, (
        f"Exactly one option should have cursor indicator, found {cursor_count}"
    )

    # Verify the cursor is on the correct option
    # Find the line with the cursor
    cursor_line = None
    for line in lines:
        if ">>>" in line:
            cursor_line = line
            break

    assert cursor_line is not None, "Cursor line should be found"

    # The cursor line should contain the selected option number
    selected_number = selected_index + 1
    assert f"{selected_number}." in cursor_line, f"Cursor should be on option {selected_number}"

    # The cursor line should contain the selected option text
    selected_option = options[selected_index]
    assert selected_option in cursor_line, (
        f"Cursor line should contain selected option text '{selected_option}'"
    )

    # Verify all options are present in the menu
    assert len([line for line in lines if any(opt in line for opt in options)]) == len(options), (
        "All options should be present in the rendered menu"
    )
