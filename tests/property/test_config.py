"""
Property-based tests for configuration management.

Tests universal properties of the ConfigManager including priority chain,
round-trip persistence, and configuration operations.
"""

import os
import tempfile
from pathlib import Path

import tomli_w
from hypothesis import given
from hypothesis import strategies as st

from mudhound.core.config import ConfigManager


@given(
    config_value=st.text(min_size=1, max_size=50),
    key_name=st.sampled_from(["engine", "max_results", "theme", "fps", "level"]),
)
def test_config_priority_chain(config_value, key_name):
    """
    Feature: mudhound-full-implementation, Property 21: Config file priority chain

    For any set of configuration files present, the configuration manager should load
    from the first file found in priority order (CLI override → env var → current dir
    → XDG → legacy → defaults).

    Validates: Requirements 7.1
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Create two config files with different values
        cli_config_path = tmpdir_path / "cli_config.toml"
        env_config_path = tmpdir_path / "env_config.toml"

        # CLI config has priority
        cli_config = {"general": {key_name: f"cli_{config_value}"}}
        with open(cli_config_path, "wb") as f:
            tomli_w.dump(cli_config, f)

        # Env config has lower priority
        env_config = {"general": {key_name: f"env_{config_value}"}}
        with open(env_config_path, "wb") as f:
            tomli_w.dump(env_config, f)

        # Test 1: CLI override takes precedence over env var
        old_env = os.environ.get("MUDHOUND_CONFIG")
        try:
            os.environ["MUDHOUND_CONFIG"] = str(env_config_path)

            # Load with CLI path - should use CLI config
            manager = ConfigManager(cli_config_path=str(cli_config_path))

            # Should get the CLI value, not the env value
            assert manager.get(f"general.{key_name}") == f"cli_{config_value}"

        finally:
            if old_env is None:
                os.environ.pop("MUDHOUND_CONFIG", None)
            else:
                os.environ["MUDHOUND_CONFIG"] = old_env

        # Test 2: Env var takes precedence when no CLI path
        old_env = os.environ.get("MUDHOUND_CONFIG")
        try:
            os.environ["MUDHOUND_CONFIG"] = str(env_config_path)

            # Load without CLI path - should use env config
            manager = ConfigManager()

            # Should get the env value
            assert manager.get(f"general.{key_name}") == f"env_{config_value}"

        finally:
            if old_env is None:
                os.environ.pop("MUDHOUND_CONFIG", None)
            else:
                os.environ["MUDHOUND_CONFIG"] = old_env


@given(
    key=st.sampled_from(
        ["general.engine", "ui.theme", "animation.fps", "search.timeout", "logging.level"]
    ),
    value=st.one_of(
        st.text(min_size=1, max_size=50), st.integers(min_value=1, max_value=1000), st.booleans()
    ),
)
def test_config_set_get_round_trip(key, value):
    """
    Feature: mudhound-full-implementation, Property 23: Config set-get round trip

    For any key-value pair, setting a config value then getting it should return
    the same value.

    Validates: Requirements 7.3
    """
    manager = ConfigManager()

    # Set the value
    manager.set(key, value)

    # Get the value back
    retrieved = manager.get(key)

    # Should be equal
    assert retrieved == value


@given(
    nested_key=st.text(
        min_size=1,
        max_size=20,
        alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd"), whitelist_characters="_"),
    ),
    value=st.integers(min_value=0, max_value=1000),
)
def test_config_nested_key_creation(nested_key, value):
    """
    Test that setting a nested key creates intermediate dictionaries.

    For any nested key path, setting a value should create all intermediate
    dictionaries as needed.
    """
    manager = ConfigManager()

    # Create a nested key path
    key_path = f"custom.{nested_key}.setting"

    # Set the value
    manager.set(key_path, value)

    # Should be able to retrieve it
    assert manager.get(key_path) == value

    # Intermediate dictionaries should exist
    assert isinstance(manager.get("custom"), dict)
    assert isinstance(manager.get(f"custom.{nested_key}"), dict)


@given(
    config_data=st.dictionaries(
        keys=st.sampled_from(["general", "ui", "animation", "search"]),
        values=st.dictionaries(
            keys=st.text(
                min_size=1,
                max_size=20,
                alphabet=st.characters(whitelist_categories=("Ll",), whitelist_characters="_"),
            ),
            values=st.one_of(st.text(min_size=1, max_size=50), st.integers(1, 100)),
        ),
        min_size=1,
        max_size=4,
    )
)
def test_config_save_load_round_trip(config_data):
    """
    Test that saving and loading configuration preserves data.

    For any configuration data, saving to a file and loading it back should
    produce equivalent configuration.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"

        # Create manager and set values
        manager1 = ConfigManager()
        for section, settings in config_data.items():
            for key, value in settings.items():
                manager1.set(f"{section}.{key}", value)

        # Save to file
        manager1.save(config_path)

        # Load from file
        manager2 = ConfigManager(cli_config_path=str(config_path))

        # All values should match
        for section, settings in config_data.items():
            for key, value in settings.items():
                assert manager2.get(f"{section}.{key}") == value
