"""Frame rendering system for terminal UI with multiple border styles."""

from enum import Enum
from typing import Dict, List, Optional


class BorderStyle(Enum):
    """Available border character sets."""
    DOUBLE = "double"
    SINGLE = "single"
    BOLD = "bold"
    ROUNDED = "rounded"
    ASCII = "ascii"


# Border character sets for each style
BORDER_CHARS: Dict[BorderStyle, Dict[str, str]] = {
    BorderStyle.DOUBLE: {
        "top_left": "╔",
        "top_right": "╗",
        "bottom_left": "╚",
        "bottom_right": "╝",
        "horizontal": "═",
        "vertical": "║",
        "left_t": "╠",
        "right_t": "╣",
        "top_t": "╦",
        "bottom_t": "╩",
        "cross": "╬",
    },
    BorderStyle.SINGLE: {
        "top_left": "┌",
        "top_right": "┐",
        "bottom_left": "└",
        "bottom_right": "┘",
        "horizontal": "─",
        "vertical": "│",
        "left_t": "├",
        "right_t": "┤",
        "top_t": "┬",
        "bottom_t": "┴",
        "cross": "┼",
    },
    BorderStyle.BOLD: {
        "top_left": "┏",
        "top_right": "┓",
        "bottom_left": "┗",
        "bottom_right": "┛",
        "horizontal": "━",
        "vertical": "┃",
        "left_t": "┣",
        "right_t": "┫",
        "top_t": "┳",
        "bottom_t": "┻",
        "cross": "╋",
    },
    BorderStyle.ROUNDED: {
        "top_left": "╭",
        "top_right": "╮",
        "bottom_left": "╰",
        "bottom_right": "╯",
        "horizontal": "─",
        "vertical": "│",
        "left_t": "├",
        "right_t": "┤",
        "top_t": "┬",
        "bottom_t": "┴",
        "cross": "┼",
    },
    BorderStyle.ASCII: {
        "top_left": "+",
        "top_right": "+",
        "bottom_left": "+",
        "bottom_right": "+",
        "horizontal": "-",
        "vertical": "|",
        "left_t": "+",
        "right_t": "+",
        "top_t": "+",
        "bottom_t": "+",
        "cross": "+",
    },
}


class FrameRenderer:
    """
    Renders terminal frames with borders, headers, footers, and content.
    
    Supports multiple border styles and dynamic width adjustment.
    """

    def __init__(self, style: BorderStyle = BorderStyle.DOUBLE, width: Optional[int] = None):
        """
        Initialize the frame renderer.
        
        Args:
            style: Border style to use
            width: Frame width in columns (None for dynamic)
        """
        self.style = style
        self.width = width
        self.chars = BORDER_CHARS[style]

    def set_width(self, width: int) -> None:
        """
        Set the frame width.
        
        Args:
            width: Frame width in columns
        """
        self.width = width

    def set_style(self, style: BorderStyle) -> None:
        """
        Change the border style.
        
        Args:
            style: New border style
        """
        self.style = style
        self.chars = BORDER_CHARS[style]

    def top_border(
        self,
        width: Optional[int] = None,
        title: Optional[str] = None,
        tag: Optional[str] = None
    ) -> str:
        """
        Render the top border of a frame.
        
        Args:
            width: Frame width (uses instance width if None)
            title: Optional title to display in the border
            tag: Optional tag to display on the right side
            
        Returns:
            str: Formatted top border line
        """
        w = width or self.width
        if w is None:
            raise ValueError("Width must be specified")

        # Calculate available space for content
        inner_width = w - 2  # Subtract corners

        if title and tag:
            # Format: ╔═ Title ═══...═══ Tag ═╗
            title_part = f" {title} "
            tag_part = f" {tag} "
            remaining = inner_width - len(title_part) - len(tag_part)

            if remaining < 0:
                # Not enough space, truncate title
                available = inner_width - len(tag_part) - 3  # 3 for " ..."
                if available > 0:
                    title_part = f" {title[:available]}... "
                    remaining = 0
                else:
                    # Even less space, just show tag
                    title_part = ""
                    remaining = inner_width - len(tag_part)

            line = (
                self.chars["top_left"]
                + self.chars["horizontal"]
                + title_part
                + self.chars["horizontal"] * max(0, remaining)
                + tag_part
                + self.chars["horizontal"]
                + self.chars["top_right"]
            )
        elif title:
            # Format: ╔═ Title ═══...═══╗
            title_part = f" {title} "
            remaining = inner_width - len(title_part)

            if remaining < 0:
                # Truncate title
                available = inner_width - 6  # 6 for "═ ... ═"
                if available > 0:
                    title_part = f" {title[:available]}... "
                    remaining = 0
                else:
                    title_part = ""
                    remaining = inner_width

            line = (
                self.chars["top_left"]
                + self.chars["horizontal"]
                + title_part
                + self.chars["horizontal"] * max(0, remaining)
                + self.chars["horizontal"]
                + self.chars["top_right"]
            )
        elif tag:
            # Format: ╔═══...═══ Tag ═╗
            tag_part = f" {tag} "
            remaining = inner_width - len(tag_part)

            line = (
                self.chars["top_left"]
                + self.chars["horizontal"] * max(0, remaining)
                + tag_part
                + self.chars["horizontal"]
                + self.chars["top_right"]
            )
        else:
            # Format: ╔═══...═══╗
            line = (
                self.chars["top_left"]
                + self.chars["horizontal"] * inner_width
                + self.chars["top_right"]
            )

        return line

    def bottom_border(
        self,
        width: Optional[int] = None,
        status: Optional[str] = None,
        pagination: Optional[str] = None
    ) -> str:
        """
        Render the bottom border of a frame.
        
        Args:
            width: Frame width (uses instance width if None)
            status: Optional status text to display
            pagination: Optional pagination info (e.g., "1/10")
            
        Returns:
            str: Formatted bottom border line
        """
        w = width or self.width
        if w is None:
            raise ValueError("Width must be specified")

        # Calculate available space for content
        inner_width = w - 2  # Subtract corners

        if status and pagination:
            # Format: ╚═ Status ═══...═══ Page ═╝
            status_part = f" {status} "
            page_part = f" {pagination} "
            remaining = inner_width - len(status_part) - len(page_part)

            if remaining < 0:
                # Not enough space, truncate status
                available = inner_width - len(page_part) - 3
                if available > 0:
                    status_part = f" {status[:available]}... "
                    remaining = 0
                else:
                    status_part = ""
                    remaining = inner_width - len(page_part)

            line = (
                self.chars["bottom_left"]
                + self.chars["horizontal"]
                + status_part
                + self.chars["horizontal"] * max(0, remaining)
                + page_part
                + self.chars["horizontal"]
                + self.chars["bottom_right"]
            )
        elif status:
            # Format: ╚═ Status ═══...═══╝
            status_part = f" {status} "
            remaining = inner_width - len(status_part)

            if remaining < 0:
                available = inner_width - 6
                if available > 0:
                    status_part = f" {status[:available]}... "
                    remaining = 0
                else:
                    status_part = ""
                    remaining = inner_width

            line = (
                self.chars["bottom_left"]
                + self.chars["horizontal"]
                + status_part
                + self.chars["horizontal"] * max(0, remaining)
                + self.chars["horizontal"]
                + self.chars["bottom_right"]
            )
        elif pagination:
            # Format: ╚═══...═══ Page ═╝
            page_part = f" {pagination} "
            remaining = inner_width - len(page_part)

            line = (
                self.chars["bottom_left"]
                + self.chars["horizontal"] * max(0, remaining)
                + page_part
                + self.chars["horizontal"]
                + self.chars["bottom_right"]
            )
        else:
            # Format: ╚═══...═══╝
            line = (
                self.chars["bottom_left"]
                + self.chars["horizontal"] * inner_width
                + self.chars["bottom_right"]
            )

        return line

    def header_row(self, text: str, width: Optional[int] = None, align: str = "left") -> str:
        """
        Render a header row with text inside the frame.
        
        Args:
            text: Header text to display
            width: Frame width (uses instance width if None)
            align: Text alignment ("left", "center", "right")
            
        Returns:
            str: Formatted header row
        """
        w = width or self.width
        if w is None:
            raise ValueError("Width must be specified")

        inner_width = w - 4  # Subtract borders and padding

        # Truncate text if too long
        if len(text) > inner_width:
            text = text[:inner_width - 3] + "..."

        # Apply alignment
        if align == "center":
            text = text.center(inner_width)
        elif align == "right":
            text = text.rjust(inner_width)
        else:  # left
            text = text.ljust(inner_width)

        return f"{self.chars['vertical']} {text} {self.chars['vertical']}"

    def footer_row(self, text: str, width: Optional[int] = None, align: str = "left") -> str:
        """
        Render a footer row with text inside the frame.
        
        Args:
            text: Footer text to display
            width: Frame width (uses instance width if None)
            align: Text alignment ("left", "center", "right")
            
        Returns:
            str: Formatted footer row
        """
        # Footer rows are rendered the same as header rows
        return self.header_row(text, width, align)

    def divider(self, width: Optional[int] = None, text: Optional[str] = None) -> str:
        """
        Render a horizontal divider line.
        
        Args:
            width: Frame width (uses instance width if None)
            text: Optional text to display in the divider
            
        Returns:
            str: Formatted divider line
        """
        w = width or self.width
        if w is None:
            raise ValueError("Width must be specified")

        inner_width = w - 2  # Subtract T-junctions

        if text:
            # Format: ╠═ Text ═══...═══╣
            text_part = f" {text} "
            remaining = inner_width - len(text_part)

            if remaining < 0:
                available = inner_width - 6
                if available > 0:
                    text_part = f" {text[:available]}... "
                    remaining = 0
                else:
                    text_part = ""
                    remaining = inner_width

            line = (
                self.chars["left_t"]
                + self.chars["horizontal"]
                + text_part
                + self.chars["horizontal"] * max(0, remaining)
                + self.chars["horizontal"]
                + self.chars["right_t"]
            )
        else:
            # Format: ╠═══...═══╣
            line = (
                self.chars["left_t"]
                + self.chars["horizontal"] * inner_width
                + self.chars["right_t"]
            )

        return line

    def content_rows(
        self,
        lines: List[str],
        width: Optional[int] = None,
        padding: int = 1
    ) -> List[str]:
        """
        Render multiple content rows with borders.
        
        Args:
            lines: List of content lines to render
            width: Frame width (uses instance width if None)
            padding: Left/right padding in spaces
            
        Returns:
            List[str]: Formatted content rows
        """
        w = width or self.width
        if w is None:
            raise ValueError("Width must be specified")

        inner_width = w - 2 - (2 * padding)  # Subtract borders and padding

        result = []
        for line in lines:
            # Truncate if too long
            if len(line) > inner_width:
                line = line[:inner_width - 3] + "..."

            # Pad to full width
            line = line.ljust(inner_width)

            # Add borders and padding
            formatted = (
                self.chars["vertical"]
                + " " * padding
                + line
                + " " * padding
                + self.chars["vertical"]
            )
            result.append(formatted)

        return result

    def empty_row(self, width: Optional[int] = None) -> str:
        """
        Render an empty content row.
        
        Args:
            width: Frame width (uses instance width if None)
            
        Returns:
            str: Formatted empty row
        """
        w = width or self.width
        if w is None:
            raise ValueError("Width must be specified")

        inner_width = w - 2
        return f"{self.chars['vertical']}{' ' * inner_width}{self.chars['vertical']}"


# Convenience functions for quick frame rendering

def render_simple_frame(
    content: List[str],
    width: int,
    style: BorderStyle = BorderStyle.DOUBLE,
    title: Optional[str] = None,
    status: Optional[str] = None
) -> List[str]:
    """
    Render a simple frame with content.
    
    Args:
        content: List of content lines
        width: Frame width
        style: Border style
        title: Optional title
        status: Optional status text
        
    Returns:
        List[str]: Complete frame as list of lines
    """
    renderer = FrameRenderer(style, width)

    frame = []
    frame.append(renderer.top_border(title=title))
    frame.extend(renderer.content_rows(content))
    frame.append(renderer.bottom_border(status=status))

    return frame


def render_frame_with_header(
    header: str,
    content: List[str],
    width: int,
    style: BorderStyle = BorderStyle.DOUBLE,
    title: Optional[str] = None
) -> List[str]:
    """
    Render a frame with a header section.
    
    Args:
        header: Header text
        content: List of content lines
        width: Frame width
        style: Border style
        title: Optional title
        
    Returns:
        List[str]: Complete frame as list of lines
    """
    renderer = FrameRenderer(style, width)

    frame = []
    frame.append(renderer.top_border(title=title))
    frame.append(renderer.header_row(header, align="center"))
    frame.append(renderer.divider())
    frame.extend(renderer.content_rows(content))
    frame.append(renderer.bottom_border())

    return frame
