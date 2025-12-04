"""Unit tests for frame rendering system."""

import pytest
from mudhound.ui.frames import (
    BorderStyle,
    FrameRenderer,
    render_simple_frame,
    render_frame_with_header,
)


class TestFrameRenderer:
    """Test the FrameRenderer class."""
    
    def test_initialization(self):
        """Test frame renderer initialization."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=80)
        assert renderer.style == BorderStyle.DOUBLE
        assert renderer.width == 80
    
    def test_set_width(self):
        """Test setting frame width."""
        renderer = FrameRenderer(BorderStyle.DOUBLE)
        renderer.set_width(100)
        assert renderer.width == 100
    
    def test_set_style(self):
        """Test changing border style."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=80)
        renderer.set_style(BorderStyle.SINGLE)
        assert renderer.style == BorderStyle.SINGLE
    
    def test_top_border_simple(self):
        """Test simple top border without title or tag."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=20)
        border = renderer.top_border()
        assert border.startswith("╔")
        assert border.endswith("╗")
        assert len(border) == 20
    
    def test_top_border_with_title(self):
        """Test top border with title."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        border = renderer.top_border(title="Test")
        assert "Test" in border
        assert border.startswith("╔")
        assert border.endswith("╗")
    
    def test_top_border_with_title_and_tag(self):
        """Test top border with both title and tag."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=40)
        border = renderer.top_border(title="Title", tag="v1.0")
        assert "Title" in border
        assert "v1.0" in border
    
    def test_bottom_border_simple(self):
        """Test simple bottom border."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=20)
        border = renderer.bottom_border()
        assert border.startswith("╚")
        assert border.endswith("╝")
        assert len(border) == 20
    
    def test_bottom_border_with_status(self):
        """Test bottom border with status."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        border = renderer.bottom_border(status="Ready")
        assert "Ready" in border
    
    def test_bottom_border_with_pagination(self):
        """Test bottom border with pagination."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        border = renderer.bottom_border(pagination="1/10")
        assert "1/10" in border
    
    def test_header_row_left_align(self):
        """Test header row with left alignment."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        row = renderer.header_row("Header", align="left")
        assert "Header" in row
        assert row.startswith("║")
        assert row.endswith("║")
    
    def test_header_row_center_align(self):
        """Test header row with center alignment."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        row = renderer.header_row("Header", align="center")
        assert "Header" in row
    
    def test_header_row_right_align(self):
        """Test header row with right alignment."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        row = renderer.header_row("Header", align="right")
        assert "Header" in row
    
    def test_divider_simple(self):
        """Test simple divider."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=20)
        div = renderer.divider()
        assert div.startswith("╠")
        assert div.endswith("╣")
        assert "═" in div
    
    def test_divider_with_text(self):
        """Test divider with text."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        div = renderer.divider(text="Section")
        assert "Section" in div
    
    def test_content_rows(self):
        """Test rendering content rows."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        lines = ["Line 1", "Line 2", "Line 3"]
        rows = renderer.content_rows(lines)
        assert len(rows) == 3
        for row in rows:
            assert row.startswith("║")
            assert row.endswith("║")
    
    def test_content_rows_truncation(self):
        """Test content row truncation for long lines."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=20)
        lines = ["This is a very long line that should be truncated"]
        rows = renderer.content_rows(lines)
        assert len(rows) == 1
        assert "..." in rows[0]
    
    def test_empty_row(self):
        """Test empty row rendering."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=20)
        row = renderer.empty_row()
        assert row.startswith("║")
        assert row.endswith("║")
        assert len(row) == 20
    
    def test_width_required_error(self):
        """Test that width is required when not set."""
        renderer = FrameRenderer(BorderStyle.DOUBLE)
        with pytest.raises(ValueError, match="Width must be specified"):
            renderer.top_border()


class TestBorderStyles:
    """Test different border styles."""
    
    def test_double_border_style(self):
        """Test double border characters."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=20)
        border = renderer.top_border()
        assert "╔" in border
        assert "╗" in border
        assert "═" in border
    
    def test_single_border_style(self):
        """Test single border characters."""
        renderer = FrameRenderer(BorderStyle.SINGLE, width=20)
        border = renderer.top_border()
        assert "┌" in border
        assert "┐" in border
        assert "─" in border
    
    def test_bold_border_style(self):
        """Test bold border characters."""
        renderer = FrameRenderer(BorderStyle.BOLD, width=20)
        border = renderer.top_border()
        assert "┏" in border
        assert "┓" in border
        assert "━" in border
    
    def test_rounded_border_style(self):
        """Test rounded border characters."""
        renderer = FrameRenderer(BorderStyle.ROUNDED, width=20)
        border = renderer.top_border()
        assert "╭" in border
        assert "╮" in border
    
    def test_ascii_border_style(self):
        """Test ASCII border characters."""
        renderer = FrameRenderer(BorderStyle.ASCII, width=20)
        border = renderer.top_border()
        assert "+" in border
        assert "-" in border


class TestConvenienceFunctions:
    """Test convenience functions for frame rendering."""
    
    def test_render_simple_frame(self):
        """Test simple frame rendering."""
        content = ["Line 1", "Line 2"]
        frame = render_simple_frame(content, width=30)
        assert len(frame) == 4  # top + 2 content + bottom
        assert frame[0].startswith("╔")
        assert frame[-1].startswith("╚")
    
    def test_render_simple_frame_with_title(self):
        """Test simple frame with title."""
        content = ["Line 1"]
        frame = render_simple_frame(content, width=30, title="Test")
        assert "Test" in frame[0]
    
    def test_render_simple_frame_with_status(self):
        """Test simple frame with status."""
        content = ["Line 1"]
        frame = render_simple_frame(content, width=30, status="Ready")
        assert "Ready" in frame[-1]
    
    def test_render_frame_with_header(self):
        """Test frame with header section."""
        content = ["Line 1", "Line 2"]
        frame = render_frame_with_header("Header", content, width=30)
        assert len(frame) == 6  # top + header + divider + 2 content + bottom
        assert "Header" in frame[1]
        assert frame[2].startswith("╠")  # divider


class TestDynamicWidth:
    """Test dynamic width adjustment."""
    
    def test_width_override(self):
        """Test overriding instance width."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=30)
        border = renderer.top_border(width=40)
        assert len(border) == 40
    
    def test_width_consistency(self):
        """Test that all frame parts have consistent width."""
        renderer = FrameRenderer(BorderStyle.DOUBLE, width=50)
        top = renderer.top_border()
        content = renderer.content_rows(["Test"])
        bottom = renderer.bottom_border()
        
        assert len(top) == 50
        assert len(content[0]) == 50
        assert len(bottom) == 50
