"""Demo script to visualize frame rendering."""

from mudhound.ui.frames import (
    BorderStyle,
    FrameRenderer,
    render_frame_with_header,
    render_simple_frame,
)


def demo_all_styles():
    """Demonstrate all border styles."""
    styles = [
        BorderStyle.DOUBLE,
        BorderStyle.SINGLE,
        BorderStyle.BOLD,
        BorderStyle.ROUNDED,
        BorderStyle.ASCII,
    ]

    for style in styles:
        print(f"\n{style.value.upper()} BORDER STYLE:")
        print("-" * 60)

        renderer = FrameRenderer(style, width=60)

        # Simple frame
        print(renderer.top_border(title="Simple Frame", tag="v1.0"))
        print(renderer.content_rows(
            ["This is a simple frame with content"])[0])
        print(renderer.bottom_border(status="Ready", pagination="1/1"))
        print()


def demo_frame_anatomy():
    """Demonstrate frame anatomy with all features."""
    print("\nFRAME ANATOMY DEMONSTRATION:")
    print("-" * 60)

    renderer = FrameRenderer(BorderStyle.DOUBLE, width=60)

    # Complete frame with all features
    print(renderer.top_border(title="MudHound Search", tag="v0.1.0"))
    print(renderer.header_row("Search Results", align="center"))
    print(renderer.divider(text="Results"))

    content = [
        "1. https://example.com - Example Domain",
        "2. https://python.org - Python Programming",
        "3. https://github.com - GitHub Platform",
    ]

    for row in renderer.content_rows(content):
        print(row)

    print(renderer.divider())
    print(renderer.footer_row("Press Enter to continue", align="center"))
    print(renderer.bottom_border(status="3 results", pagination="Page 1/1"))
    print()


def demo_dynamic_width():
    """Demonstrate dynamic width adjustment."""
    print("\nDYNAMIC WIDTH DEMONSTRATION:")
    print("-" * 60)

    widths = [40, 60, 80]

    for width in widths:
        print(f"\nWidth: {width} columns")
        frame = render_simple_frame(
            ["Content adapts to frame width"],
            width=width,
            title="Dynamic",
            status=f"Width: {width}",
        )
        for line in frame:
            print(line)


def demo_truncation():
    """Demonstrate text truncation for long content."""
    print("\nTEXT TRUNCATION DEMONSTRATION:")
    print("-" * 60)

    renderer = FrameRenderer(BorderStyle.DOUBLE, width=40)

    print(renderer.top_border(
        title="Very Long Title That Should Be Truncated", tag="Tag"))

    long_content = [
        "This is a very long line that will definitely be truncated because it exceeds the frame width"
    ]

    for row in renderer.content_rows(long_content):
        print(row)

    print(
        renderer.bottom_border(
            status="Very long status message that should be truncated", pagination="999/999"
        )
    )
    print()


def demo_convenience_functions():
    """Demonstrate convenience functions."""
    print("\nCONVENIENCE FUNCTIONS DEMONSTRATION:")
    print("-" * 60)

    # Simple frame
    print("\nSimple Frame:")
    frame = render_simple_frame(
        ["Line 1", "Line 2", "Line 3"], width=50, title="Simple", status="Complete"
    )
    for line in frame:
        print(line)

    # Frame with header
    print("\nFrame with Header:")
    frame = render_frame_with_header(
        "Important Header", ["Content line 1", "Content line 2"], width=50, title="Header Demo"
    )
    for line in frame:
        print(line)


if __name__ == "__main__":
    print("=" * 60)
    print("MUDHOUND FRAME RENDERING SYSTEM DEMO")
    print("=" * 60)

    demo_all_styles()
    demo_frame_anatomy()
    demo_dynamic_width()
    demo_truncation()
    demo_convenience_functions()

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
