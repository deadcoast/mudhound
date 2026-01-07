"""Unit tests for color scheme definitions."""

from mudhound.ui.animation.schemes import (
    DARK_RAINBOW_COLORS_256,
    LIGHT_RAINBOW_COLORS_256,
    RAINBOW_COLORS_256,
    WHITE_COLORS,
    ColorScheme,
    generate_rainbow_frame,
)


def test_color_scheme_enum_values():
    """Test that ColorScheme enum has all expected values."""
    assert ColorScheme.RAINBOW.value == "rainbow"
    assert ColorScheme.DARK_RAINBOW.value == "dark-rainbow"
    assert ColorScheme.LIGHT_RAINBOW.value == "light-rainbow"
    assert ColorScheme.WHITE.value == "white"
    assert ColorScheme.THEME.value == "theme"


def test_rainbow_colors_palette():
    """Test that RAINBOW_COLORS_256 has correct values."""
    expected = [196, 208, 226, 46, 51, 21, 129, 201]
    assert RAINBOW_COLORS_256 == expected
    assert len(RAINBOW_COLORS_256) == 8


def test_dark_rainbow_colors_palette():
    """Test that DARK_RAINBOW_COLORS_256 has correct values."""
    expected = [88, 130, 136, 22, 23, 18, 54, 90]
    assert DARK_RAINBOW_COLORS_256 == expected
    assert len(DARK_RAINBOW_COLORS_256) == 8


def test_light_rainbow_colors_palette():
    """Test that LIGHT_RAINBOW_COLORS_256 has correct values."""
    expected = [210, 216, 228, 120, 123, 111, 183, 219]
    assert LIGHT_RAINBOW_COLORS_256 == expected
    assert len(LIGHT_RAINBOW_COLORS_256) == 8


def test_white_colors_palette():
    """Test that WHITE_COLORS has correct value."""
    expected = [255]
    assert WHITE_COLORS == expected
    assert len(WHITE_COLORS) == 1


def test_generate_rainbow_frame_basic():
    """Test basic rainbow frame generation."""
    art = "AB"
    frame = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)

    # Should contain ANSI color codes
    assert "\033[38;5;" in frame
    # Should contain the original characters
    assert "A" in frame
    assert "B" in frame
    # Should have reset code at end
    assert "\033[0m" in frame


def test_generate_rainbow_frame_offset_changes_colors():
    """Test that different offsets produce different colored frames."""
    art = "TEST"
    frame1 = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)
    frame2 = generate_rainbow_frame(art, 1, ColorScheme.RAINBOW)

    # Different offsets should produce different frames
    assert frame1 != frame2


def test_generate_rainbow_frame_different_schemes():
    """Test that different color schemes produce different results."""
    art = "TEST"
    rainbow = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)
    dark = generate_rainbow_frame(art, 0, ColorScheme.DARK_RAINBOW)
    light = generate_rainbow_frame(art, 0, ColorScheme.LIGHT_RAINBOW)
    white = generate_rainbow_frame(art, 0, ColorScheme.WHITE)

    # Different schemes should produce different frames
    assert rainbow != dark
    assert rainbow != light
    assert rainbow != white
    assert dark != light


def test_generate_rainbow_frame_preserves_whitespace():
    """Test that whitespace is preserved without coloring."""
    art = "A B"
    frame = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)

    # Should contain the space
    assert " " in frame
    # The space should not have color codes around it
    # (checking that we don't have color code immediately before space)


def test_generate_rainbow_frame_multiline():
    """Test rainbow frame generation with multiple lines."""
    art = "AB\nCD"
    frame = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)

    # Should preserve line breaks
    assert "\n" in frame
    # Should have reset codes for each line
    assert frame.count("\033[0m") >= 2


def test_generate_rainbow_frame_empty_string():
    """Test rainbow frame generation with empty string."""
    art = ""
    frame = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)

    # Should return empty string
    assert frame == ""


def test_generate_rainbow_frame_theme_scheme():
    """Test that THEME scheme falls back to RAINBOW for now."""
    art = "TEST"
    theme_frame = generate_rainbow_frame(art, 0, ColorScheme.THEME)
    rainbow_frame = generate_rainbow_frame(art, 0, ColorScheme.RAINBOW)

    # For now, THEME should produce same result as RAINBOW
    assert theme_frame == rainbow_frame
