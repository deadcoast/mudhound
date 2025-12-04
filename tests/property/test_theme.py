"""
Property-based tests for the theme engine.

These tests verify universal properties that should hold across all theme configurations.
"""

import tempfile
from pathlib import Path
from hypothesis import given, strategies as st
import tomli_w

from mudhound.ui.theme import Theme, ThemeEngine, ANSI_COLORS
from mudhound.ui.renderer import UIRenderer
from mudhound.ui.frames import BorderStyle
from mudhound.core.exceptions import ConfigError


# Strategy for valid ANSI color names
ansi_color_names = st.sampled_from(list(ANSI_COLORS.keys()))

# Strategy for semantic color names
semantic_color_names = st.sampled_from([
    "primary", "secondary", "accent",
    "success", "error", "warning", "info",
    "frame_border", "frame_title", "frame_content",
    "text", "text_dim", "highlight"
])

# Strategy for animation color schemes
animation_schemes = st.one_of(
    st.none(),
    st.sampled_from(["rainbow", "dark-rainbow", "light-rainbow", "white", "theme"])
)


@given(
    theme_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters="-_")),
    colors=st.dictionaries(
        keys=semantic_color_names,
        values=ansi_color_names,
        min_size=1,
        max_size=15
    ),
    animation_scheme=animation_schemes
)
def test_theme_toml_loading(theme_name, colors, animation_scheme):
    """
    Feature: mudhound-full-implementation, Property 52: Theme TOML loading
    
    For any valid theme TOML file in the themes directory, the theme engine
    should load it successfully.
    
    Validates: Requirements 17.1
    """
    # Create a temporary directory for themes
    with tempfile.TemporaryDirectory() as tmpdir:
        themes_dir = Path(tmpdir)
        
        # Create theme TOML file
        theme_dict = {
            "name": theme_name,
            "colors": colors,
        }
        
        if animation_scheme is not None:
            theme_dict["animation"] = {"color_scheme": animation_scheme}
        
        theme_path = themes_dir / f"{theme_name}.toml"
        with open(theme_path, "wb") as f:
            tomli_w.dump(theme_dict, f)
        
        # Create theme engine with custom themes directory
        engine = ThemeEngine(themes_dir=themes_dir)
        
        # Load the theme
        loaded_theme = engine.load_theme(theme_name)
        
        # Verify theme was loaded successfully
        assert loaded_theme is not None
        assert loaded_theme.name == theme_name
        assert loaded_theme.colors == colors
        assert loaded_theme.animation_scheme == animation_scheme


@given(
    semantic_name=semantic_color_names
)
def test_semantic_color_resolution(semantic_name):
    """
    Feature: mudhound-full-implementation, Property 53: Semantic color resolution
    
    For any semantic color name (success, error, warning, info), the theme engine
    should resolve it to a valid terminal escape code.
    
    Validates: Requirements 17.2
    """
    # Create a theme engine with default theme
    engine = ThemeEngine()
    
    # Get the ANSI escape code for the semantic name
    escape_code = engine.get_color(semantic_name)
    
    # Verify it's a valid ANSI escape code (starts with \033[ and ends with m)
    assert escape_code.startswith("\033[")
    assert escape_code.endswith("m")
    
    # Verify it's one of the known ANSI color codes
    assert escape_code in ANSI_COLORS.values()


@given(
    requested_theme=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters="-_"))
)
def test_theme_fallback_behavior(requested_theme):
    """
    Feature: mudhound-full-implementation, Property 56: Theme fallback behavior
    
    For any requested theme that does not exist, the theme engine should fall back
    to the default theme.
    
    Validates: Requirements 17.5
    """
    # Create a temporary empty directory for themes
    with tempfile.TemporaryDirectory() as tmpdir:
        themes_dir = Path(tmpdir)
        
        # Create theme engine with empty themes directory
        engine = ThemeEngine(themes_dir=themes_dir)
        
        # Try to load a non-existent theme
        loaded_theme = engine.load_theme(requested_theme)
        
        # Verify it falls back to default theme
        assert loaded_theme is not None
        assert loaded_theme.name == "default"
        
        # Verify the default theme has expected semantic colors
        assert "success" in loaded_theme.colors
        assert "error" in loaded_theme.colors
        assert "warning" in loaded_theme.colors
        assert "info" in loaded_theme.colors



@given(
    content_lines=st.lists(
        st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_categories=("Cc", "Cs"))),
        min_size=1,
        max_size=10
    ),
    title=st.one_of(
        st.none(),
        st.text(min_size=1, max_size=30, alphabet=st.characters(blacklist_categories=("Cc", "Cs")))
    ),
    status=st.one_of(
        st.none(),
        st.text(min_size=1, max_size=30, alphabet=st.characters(blacklist_categories=("Cc", "Cs")))
    ),
    border_style=st.sampled_from(list(BorderStyle))
)
def test_theme_application_to_frames(content_lines, title, status, border_style):
    """
    Feature: mudhound-full-implementation, Property 3: Theme application to frames
    
    For any frame and any active theme, rendering the frame should apply the
    theme's color palette to all frame elements.
    
    Validates: Requirements 1.4
    """
    # Create a temporary directory for themes
    with tempfile.TemporaryDirectory() as tmpdir:
        themes_dir = Path(tmpdir)
        
        # Create a custom theme with specific colors
        theme_dict = {
            "name": "test_theme",
            "colors": {
                "frame_border": "bright_cyan",
                "frame_title": "bright_white",
                "frame_content": "white",
                "primary": "bright_magenta",
            }
        }
        
        theme_path = themes_dir / "test_theme.toml"
        with open(theme_path, "wb") as f:
            tomli_w.dump(theme_dict, f)
        
        # Create theme engine and load the custom theme
        theme_engine = ThemeEngine(themes_dir=themes_dir)
        theme_engine.set_active_theme("test_theme")
        
        # Create UI renderer with the custom theme engine
        renderer = UIRenderer(theme_engine=theme_engine)
        
        # Render a frame with theme application enabled
        frame_with_theme = renderer.render_frame(
            content=content_lines,
            title=title,
            status=status,
            style=border_style,
            apply_theme=True
        )
        
        # Render the same frame without theme application
        frame_without_theme = renderer.render_frame(
            content=content_lines,
            title=title,
            status=status,
            style=border_style,
            apply_theme=False
        )
        
        # Verify that frames are different (theme was applied)
        assert frame_with_theme != frame_without_theme
        
        # Verify that themed frame contains ANSI escape codes
        frame_text = "\n".join(frame_with_theme)
        assert "\033[" in frame_text, "Themed frame should contain ANSI escape codes"
        
        # Verify that the theme's frame_border color is present in the output
        expected_color = theme_engine.get_color("frame_border")
        
        # At least the top and bottom borders should have the theme color
        assert expected_color in frame_with_theme[0], "Top border should have theme color"
        assert expected_color in frame_with_theme[-1], "Bottom border should have theme color"
        
        # Verify that non-themed frame does NOT contain the specific theme color
        frame_text_no_theme = "\n".join(frame_without_theme)
        # Non-themed frame should not have ANSI codes (or at least not our specific theme color)
        assert expected_color not in frame_text_no_theme, "Non-themed frame should not have theme color"
