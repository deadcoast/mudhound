"""
Unit tests for interactive mode.

Tests basic functionality of the interactive mode command.
"""

from io import StringIO
from unittest.mock import MagicMock, patch

from mudhound.cli.commands.interactive import (
    InteractiveMode,
    InteractiveSession,
    interactive_command,
)


class TestInteractiveSession:
    """Tests for InteractiveSession class."""

    def test_initial_state(self):
        """Test that session starts with correct initial state."""
        session = InteractiveSession()

        state = session.get_state_summary()
        assert state["last_query"] is None
        assert state["result_count"] == 0
        assert state["operations"] == 0
        assert not state["has_results"]

    def test_update_search_state(self):
        """Test that search state is updated correctly."""
        session = InteractiveSession()

        # Create a mock search session
        mock_session = MagicMock()
        mock_session.results = [MagicMock(), MagicMock(), MagicMock()]

        # Update state
        session.update_search_state("test query", mock_session)

        # Verify state
        assert session.last_search_query == "test query"
        assert session.last_search_session == mock_session
        assert len(session.last_search_results) == 3
        assert session.operation_count == 1

    def test_clear_search_state(self):
        """Test that search state can be cleared."""
        session = InteractiveSession()

        # Set some state
        mock_session = MagicMock()
        mock_session.results = [MagicMock()]
        session.update_search_state("test query", mock_session)

        # Clear state
        session.clear_search_state()

        # Verify cleared
        assert session.last_search_query is None
        assert session.last_search_results is None
        assert session.last_search_session is None
        # Operation count should persist
        assert session.operation_count == 1

    def test_session_data_storage(self):
        """Test that arbitrary data can be stored in session."""
        session = InteractiveSession()

        # Store data
        session.session_data["key1"] = "value1"
        session.session_data["key2"] = 42

        # Verify storage
        assert session.session_data["key1"] == "value1"
        assert session.session_data["key2"] == 42


class TestInteractiveMode:
    """Tests for InteractiveMode class."""

    def test_initialization(self):
        """Test that interactive mode initializes correctly."""
        output = StringIO()
        mode = InteractiveMode(output=output)

        assert mode.session is not None
        assert mode.config_manager is not None
        assert mode.result_store is not None
        assert mode.use_color is True
        assert mode.use_animation is True

    def test_show_goodbye(self, capsys):
        """Test that goodbye message is displayed."""
        output = StringIO()
        mode = InteractiveMode(use_color=False, output=output)

        mode._show_goodbye()

        # Logo writes to the output stream, StatusComponent prints to stdout
        output_text = output.getvalue()
        captured = capsys.readouterr()

        # Check Logo output (contains "MH") or StatusComponent output (contains "Thank you")
        has_logo = "MH" in output_text or "mh" in output_text.lower()
        has_thank_you = "Thank you" in captured.out

        assert has_logo or has_thank_you, f"Expected logo or thank you message. Output: {output_text}, Stdout: {captured.out}"

    @patch('mudhound.cli.commands.interactive.Menu')
    def test_show_main_menu(self, mock_menu_class):
        """Test that main menu is displayed."""
        output = StringIO()
        mode = InteractiveMode(output=output)

        # Mock menu to return selection
        mock_menu = MagicMock()
        mock_menu.show.return_value = 0  # Select first option (Search)
        mock_menu_class.return_value = mock_menu

        result = mode._show_main_menu()

        assert result == "search"
        mock_menu_class.assert_called_once()
        mock_menu.show.assert_called_once()

    @patch('mudhound.cli.commands.interactive.Menu')
    def test_show_main_menu_quit(self, mock_menu_class):
        """Test that quit option works in main menu."""
        output = StringIO()
        mode = InteractiveMode(output=output)

        # Mock menu to return quit option (index 4)
        mock_menu = MagicMock()
        mock_menu.show.return_value = 4  # Quit option
        mock_menu_class.return_value = mock_menu

        result = mode._show_main_menu()

        assert result == "quit"

    @patch('mudhound.cli.commands.interactive.Menu')
    def test_show_main_menu_cancel(self, mock_menu_class):
        """Test that cancelling menu returns None."""
        output = StringIO()
        mode = InteractiveMode(output=output)

        # Mock menu to return None (cancelled)
        mock_menu = MagicMock()
        mock_menu.show.return_value = None
        mock_menu_class.return_value = mock_menu

        result = mode._show_main_menu()

        assert result is None

    @patch('mudhound.cli.commands.interactive.Menu')
    def test_show_main_menu_keyboard_interrupt(self, mock_menu_class):
        """Test that CTRL+C in menu returns quit."""
        output = StringIO()
        mode = InteractiveMode(output=output)

        # Mock menu to raise KeyboardInterrupt
        mock_menu = MagicMock()
        mock_menu.show.side_effect = KeyboardInterrupt()
        mock_menu_class.return_value = mock_menu

        result = mode._show_main_menu()

        assert result == "quit"


def test_interactive_command_function():
    """Test that interactive_command function can be called."""
    # This is a smoke test - just verify the function exists and can be imported
    assert callable(interactive_command)
