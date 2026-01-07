"""
Integration tests for CLI argument validation.

Tests that the CLI commands properly validate arguments and exit
with appropriate error codes.
"""

from typer.testing import CliRunner

from mudhound.cli.app import app

runner = CliRunner()


class TestCLIValidationIntegration:
    """Integration tests for CLI validation."""

    def test_config_get_empty_key(self):
        """Test that config get rejects empty keys."""
        result = runner.invoke(app, ["config", "get", ""])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "empty" in result.output.lower()

    def test_config_set_empty_key(self):
        """Test that config set rejects empty keys."""
        result = runner.invoke(app, ["config", "set", "", "value"])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "empty" in result.output.lower()

    def test_config_set_empty_value(self):
        """Test that config set rejects empty values."""
        result = runner.invoke(app, ["config", "set", "test.key", ""])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "empty" in result.output.lower()

    def test_history_show_empty_id(self):
        """Test that history show rejects empty session IDs."""
        result = runner.invoke(app, ["history", "show", ""])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "empty" in result.output.lower()

    def test_history_delete_empty_id(self):
        """Test that history delete rejects empty session IDs."""
        result = runner.invoke(app, ["history", "delete", "", "--yes"])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "empty" in result.output.lower()

    def test_history_replay_empty_id(self):
        """Test that history replay rejects empty session IDs."""
        result = runner.invoke(app, ["history", "replay", ""])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "empty" in result.output.lower()

    def test_history_list_invalid_limit(self):
        """Test that history list rejects invalid limit values."""
        # Test negative limit
        result = runner.invoke(app, ["history", "list", "--limit", "-1"])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "Validation" in result.output

    def test_history_list_zero_limit(self):
        """Test that history list rejects zero limit."""
        result = runner.invoke(app, ["history", "list", "--limit", "0"])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "Validation" in result.output

    def test_history_list_too_large_limit(self):
        """Test that history list rejects limits over 10000."""
        result = runner.invoke(app, ["history", "list", "--limit", "10001"])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "Validation" in result.output

    def test_global_options_conflict(self):
        """Test that conflicting global options are rejected."""
        # Test --verbose and --quiet together
        result = runner.invoke(app, ["--verbose", "--quiet", "version"])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "Cannot" in result.output

    def test_global_options_invalid_config_path(self):
        """Test that invalid config paths are rejected."""
        result = runner.invoke(
            app, ["--config", "/nonexistent/path/config.toml", "version"])

        # Should exit with error
        assert result.exit_code != 0

        # Should display error message
        assert "Error" in result.output or "not found" in result.output.lower()

    def test_version_command_success(self):
        """Test that version command works without validation errors."""
        result = runner.invoke(app, ["version"])

        # Should succeed
        assert result.exit_code == 0

        # Should display version
        assert "MudHound" in result.output or "version" in result.output.lower()
