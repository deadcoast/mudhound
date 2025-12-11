"""Demo script for Logo component."""

from mudhound.assets.manager import AssetManager
from mudhound.core.config import ConfigManager
from mudhound.ui.components import Logo, LogoPosition


def demo_logo_positions():
    """Demonstrate different logo positions."""
    print("=" * 60)
    print("Logo Component Demo")
    print("=" * 60)
    print()

    # Test inline position
    print("1. Inline Position:")
    logo_inline = Logo(position=LogoPosition.INLINE, scheme="rainbow")
    logo_inline.render()
    print(" <- Logo appears inline with text")
    print()

    # Test header position
    print("2. Header Position:")
    logo_header = Logo(position=LogoPosition.HEADER, scheme="rainbow")
    logo_header.render()
    print("Content appears below the header logo")
    print()

    # Test footer position
    print("3. Footer Position:")
    print("Content appears above the footer logo")
    logo_footer = Logo(position=LogoPosition.FOOTER, scheme="rainbow")
    logo_footer.render()
    print()

    # Test floating position (centered)
    print("4. Floating Position (Centered):")
    logo_floating = Logo(position=LogoPosition.FLOATING, scheme="rainbow")
    logo_floating.render()
    print()

    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_logo_positions()
