"""Demo script for testing the Banner component."""

from mudhound.ui.components.banner import Banner, BannerStyle

# Test different banner styles
print("=" * 60)
print("Testing Banner Component")
print("=" * 60)

# Test NONE style
print("\n1. NONE style (should produce no output):")
banner_none = Banner(style=BannerStyle.NONE)
banner_none.render()

# Test MINIMAL style
print("\n2. MINIMAL style:")
banner_minimal = Banner(style=BannerStyle.MINIMAL)
banner_minimal.render()

# Test STATIC style
print("\n3. STATIC style:")
banner_static = Banner(style=BannerStyle.STATIC, scheme="rainbow")
banner_static.render()

# Test ANIMATED style (single frame)
print("\n4. ANIMATED style (single frame):")
banner_animated = Banner(style=BannerStyle.ANIMATED, scheme="rainbow")
banner_animated.render()

print("\n" + "=" * 60)
print("Banner component demo complete!")
print("=" * 60)
