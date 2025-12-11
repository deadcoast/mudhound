"""
Unit tests for config CLI commands.

Tests the config command subcommands: list, get, set, reset, edit.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from mudhound.cli.app import app
from mudhound.core.config import ConfigManager

runner = CliRunner()


def test_config_list_command():
    """Test that config list displays all configuration."""
    result = runner.invoke(app, ["config", "list"])

    assert result.exit_code == 0
    assert "MudHound Configuration" in result.stdout
    assert "general.engine" in result.stdout
    assert "duckduckgo" in result.stdout


def test_config_get_command():
    """Test that config get retrieves a specific value."""
    result = runner.invoke(app, ["config", "get", "general.engine"])

    assert result.exit_code == 0
    assert "general.engine" in result.stdout
    assert "duckduckgo" in result.stdout


def test_config_get_nested_section():
    """Test that config get can retrieve a nested section."""
    result = runner.invoke(app, ["config", "get", "general"])

    assert result.exit_code == 0
    assert "general:" in result.stdout
    assert "engine: duckduckgo" in result.stdout
    assert "max_results: 50" in result.stdout


def test_config_get_nonexistent_key():
    """Test that config get handles nonexistent keys."""
    result = runner.invoke(app, ["config", "get", "nonexistent.key"])

    assert result.exit_code == 1
    # Error messages go to stderr, which is captured in the output
    assert "not found" in result.output or "not found" in str(result.exception)


def test_config_set_command():
    """Test that config set updates a value."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Set a value
        result = runner.invoke(
            app, ["--config", str(config_path), "config",
                  "set", "general.max_results", "100"]
        )

        assert result.exit_code == 0
        assert "Set general.max_results = 100" in result.stdout

        # Verify the value was set
        result = runner.invoke(
            app, ["--config", str(config_path), "config",
                  "get", "general.max_results"]
        )

        assert result.exit_code == 0
        assert "100" in result.stdout


def test_config_set_boolean_value():
    """Test that config set parses boolean values correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Set a boolean value
        result = runner.invoke(
            app, ["--config", str(config_path), "config",
                  "set", "ui.animation", "false"]
        )

        assert result.exit_code == 0

        # Verify it was parsed as boolean
        config_manager = ConfigManager(cli_config_path=str(config_path))
        assert config_manager.get("ui.animation") is False


def test_config_reset_command_with_yes():
    """Test that config reset restores defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Set a custom value
        runner.invoke(
            app, ["--config", str(config_path), "config",
                  "set", "general.max_results", "200"]
        )

        # Reset to defaults
        result = runner.invoke(
            app, ["--config", str(config_path), "config", "reset", "--yes"])

        assert result.exit_code == 0
        assert "Configuration reset to defaults" in result.stdout

        # Verify default value is restored
        result = runner.invoke(
            app, ["--config", str(config_path), "config",
                  "get", "general.max_results"]
        )

        assert "50" in result.stdout


def test_config_reset_command_without_yes():
    """Test that config reset prompts for confirmation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Try to reset without --yes, answer 'n'
        result = runner.invoke(
            app, ["--config", str(config_path), "config", "reset"], input="n\n")

        assert result.exit_code == 0
        assert "Reset cancelled" in result.stdout


def test_config_edit_command_creates_file():
    """Test that config edit creates a config file if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Mock subprocess.run to avoid actually opening an editor
        with patch("mudhound.cli.commands.config.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            result = runner.invoke(
                app, ["--config", str(config_path), "config", "edit"])

            assert result.exit_code == 0
            # The file should be created
            # Note: The --config flag creates the file at the specified path
            assert "Configuration file closed" in result.stdout


def test_config_edit_command_opens_editor():
    """Test that config edit opens the editor."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Create config file first
        config_manager = ConfigManager(cli_config_path=str(config_path))
        config_manager.save()

        # Mock subprocess.run
        with patch("mudhound.cli.commands.config.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            result = runner.invoke(
                app, ["--config", str(config_path), "config", "edit"])

            assert result.exit_code == 0
            assert "Configuration file closed" in result.stdout

            # Verify subprocess.run was called with an editor and a path
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]
            # Should have editor name and a path
            assert len(call_args) == 2
            assert call_args[0] in ["notepad",
                                    "nano", "vim", "vi"]  # Common editors


def test_config_edit_command_editor_not_found():
    """Test that config edit handles missing editor gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Mock subprocess.run to raise FileNotFoundError
        with patch("mudhound.cli.commands.config.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            result = runner.invoke(
                app, ["--config", str(config_path), "config", "edit"])

            assert result.exit_code == 1
            # Error messages go to stderr
            assert "not found" in result.output or "not found" in str(
                result.exception)
