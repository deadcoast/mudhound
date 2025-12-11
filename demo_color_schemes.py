#!/usr/bin/env python3
"""Demo script to visualize color schemes."""

from mudhound.ui.animation.schemes import (
    DARK_RAINBOW_COLORS_256,
    LIGHT_RAINBOW_COLORS_256,
    RAINBOW_COLORS_256,
    ColorScheme,
    generate_rainbow_frame,
)

# Sample ASCII art
art = """
███╗   ███╗██╗   ██╗██████╗ ██╗  ██╗ ██████╗ ██╗   ██╗███╗   ██╗██████╗ 
████╗ ████║██║   ██║██╔══██╗██║  ██║██╔═══██╗██║   ██║████╗  ██║██╔══██╗
██╔████╔██║██║   ██║██║  ██║███████║██║   ██║██║   ██║██╔██╗ ██║██║  ██║
██║╚██╔╝██║██║   ██║██║  ██║██╔══██║██║   ██║██║   ██║██║╚██╗██║██║  ██║
██║ ╚═╝ ██║╚██████╔╝██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 
"""

print("=" * 80)
print("COLOR SCHEME DEMONSTRATION")
print("=" * 80)

schemes = [
    (ColorScheme.RAINBOW, "RAINBOW (Full Spectrum)"),
    (ColorScheme.DARK_RAINBOW, "DARK RAINBOW (Muted)"),
    (ColorScheme.LIGHT_RAINBOW, "LIGHT RAINBOW (Pastel)"),
    (ColorScheme.WHITE, "WHITE (Monochrome)"),
]

for scheme, name in schemes:
    print(f"\n{name}:")
    print("-" * 80)
    frame = generate_rainbow_frame(art, 0, scheme)
    print(frame)
    print()

print("=" * 80)
print("ANIMATION FRAMES (offset cycling)")
print("=" * 80)

simple_art = "MUDHOUND"
print("\nRAINBOW scheme with different offsets:")
for offset in range(4):
    frame = generate_rainbow_frame(simple_art, offset, ColorScheme.RAINBOW)
    print(f"Offset {offset}: {frame}")

print("\n" + "=" * 80)
print("Color palettes:")
print(f"RAINBOW:       {RAINBOW_COLORS_256}")
print(f"DARK_RAINBOW:  {DARK_RAINBOW_COLORS_256}")
print(f"LIGHT_RAINBOW: {LIGHT_RAINBOW_COLORS_256}")
print("=" * 80)
