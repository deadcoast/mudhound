"""Demo script for Logo animation."""

import time

from mudhound.ui.components import Logo, LogoPosition


def demo_logo_animation():
    """Demonstrate logo animation."""
    print("Logo Animation Demo")
    print("=" * 60)
    print()

    # Create logo with header position
    logo = Logo(position=LogoPosition.HEADER, scheme="rainbow")

    print("Rendering animated frames (3 frames)...")
    print()

    # Render a few frames manually to show animation
    for i in range(3):
        logo.render_animated_frame(i)
        time.sleep(0.5)

    print()
    print("Animation demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    demo_logo_animation()
