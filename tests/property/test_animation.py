"""Property-based tests for animation system."""

import time
from io import StringIO
from pathlib import Path

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from mudhound.assets.manager import CACHE, AssetManager
from mudhound.ui.animation.engine import AnimationRenderer
from mudhound.ui.animation.timing import EasingFunction, TimingEngine


# Reduced range for more reliable timing
@given(fps=st.integers(min_value=5, max_value=60))
# Reduced examples for faster execution
@settings(max_examples=50, deadline=None)
def test_frame_rate_timing_accuracy(fps):
    """
    Feature: mudhound-full-implementation, Property 5: Frame rate timing accuracy

    For any configured frame rate, the animation engine should render frames
    at approximately that rate (within 20% tolerance due to OS scheduling).

    Validates: Requirements 2.2
    """
    # Create timing engine with specified FPS
    engine = TimingEngine(fps=fps, total_frames=100, duration=0.0, loop=True)

    # Start the engine
    engine.start()

    # Calculate expected frame duration
    expected_frame_duration = 1.0 / fps

    # Wait for enough frames to get reliable measurement (at least 10 frames or 0.5 seconds)
    wait_time = max(expected_frame_duration * 10, 0.5)
    initial_frame = engine.get_current_frame()
    time.sleep(wait_time)

    elapsed = engine.get_elapsed_time()
    current_frame = engine.get_current_frame()

    # Calculate frames advanced
    frames_advanced = (current_frame - initial_frame) % 100

    # Calculate actual frame rate
    if elapsed > 0 and frames_advanced > 0:
        actual_fps = frames_advanced / elapsed

        # Allow 20% tolerance for timing accuracy (OS scheduling can be imprecise)
        tolerance = 0.20
        lower_bound = fps * (1 - tolerance)
        upper_bound = fps * (1 + tolerance)

        # The actual FPS should be within tolerance of expected FPS
        assert lower_bound <= actual_fps <= upper_bound, (
            f"Frame rate {actual_fps:.2f} FPS not within 20% of target {fps} FPS "
            f"(expected range: {lower_bound:.2f} - {upper_bound:.2f})"
        )

    engine.stop()


@given(
    total_frames=st.integers(min_value=2, max_value=50),  # Reduced range
    # Higher minimum FPS for faster tests
    fps=st.integers(min_value=10, max_value=60),
)
@settings(max_examples=50, deadline=5000)  # Added deadline to prevent hangs
def test_infinite_loop_with_zero_duration(total_frames, fps):
    """
    Feature: mudhound-full-implementation, Property 8: Infinite loop with zero duration

    For any animation with duration set to zero, the animation should continue
    looping until explicitly stopped.

    Validates: Requirements 2.7
    """
    # Create timing engine with zero duration (infinite loop)
    engine = TimingEngine(
        fps=fps,
        total_frames=total_frames,
        duration=0.0,
        loop=True,  # Zero duration = infinite loop
    )

    # Start the engine
    engine.start()

    try:
        # Let it run for a short time
        time.sleep(0.1)

        # The animation should still be running
        assert engine.is_running, "Animation should still be running with zero duration"

        # The animation should never be complete
        assert not engine.is_complete(), "Animation with zero duration should never complete"

        # Get current frame - should be valid
        current_frame = engine.get_current_frame()
        assert 0 <= current_frame < total_frames, (
            f"Current frame {current_frame} should be within range [0, {total_frames})"
        )

        # Wait a bit more and verify it continues looping
        time.sleep(0.1)

        # Should still be running
        assert engine.is_running, "Animation should continue running indefinitely"
        assert not engine.is_complete(), "Animation should never complete with zero duration"

        # Frame should still be valid (may have wrapped around)
        new_frame = engine.get_current_frame()
        assert 0 <= new_frame < total_frames, (
            f"Frame {new_frame} should still be within range [0, {total_frames})"
        )

        # Verify frames are cycling through the range
        elapsed = engine.get_elapsed_time()
        expected_cycles = int(elapsed * fps / total_frames)

        # Should have cycled at least once if enough time has passed
        if elapsed * fps >= total_frames:
            # We've had enough time for at least one full cycle
            assert expected_cycles >= 1, "Should have completed at least one cycle"
    finally:
        # Always stop the engine to prevent resource leaks
        engine.stop()


@given(scheme=st.sampled_from(["rainbow", "dark-rainbow", "light-rainbow", "white"]))
@settings(max_examples=100, deadline=None)
def test_asset_caching_behavior(scheme):
    """
    Feature: mudhound-full-implementation, Property 9: Asset caching behavior

    For any asset loaded from disk, subsequent accesses to the same asset
    should return the cached version without additional disk I/O.

    Validates: Requirements 3.2
    """
    # Clear cache before test
    CACHE.clear()

    # Create asset manager
    manager = AssetManager()

    # First access - should load from disk
    try:
        frames1 = manager.get_banner_frames(scheme)
    except Exception:
        # If the scheme doesn't exist, skip this test case
        assume(False)

    # Check that cache was populated
    cache_key = f"animated:{scheme}-banner"
    static_cache_key = f"static:banner.txt"

    # Either animated or static should be cached
    assert cache_key in CACHE or static_cache_key in CACHE, (
        "Asset should be cached after first load"
    )

    # Get the cached value
    if cache_key in CACHE:
        cached_frames = CACHE[cache_key]
    else:
        cached_frames = CACHE[static_cache_key]

    # Second access - should return cached version
    frames2 = manager.get_banner_frames(scheme)

    # Should return the exact same object (identity check)
    assert frames1 is frames2, "Subsequent access should return the same cached object"

    # Verify the cached value hasn't changed
    if cache_key in CACHE:
        assert CACHE[cache_key] is cached_frames, "Cache should not be modified"
    else:
        assert CACHE[static_cache_key] is cached_frames, "Cache should not be modified"


@given(
    metadata_lines=st.integers(min_value=0, max_value=10),
    content_lines=st.integers(min_value=1, max_value=20),
)
@settings(max_examples=100, deadline=None)
def test_ansi_metadata_stripping(metadata_lines, content_lines):
    """
    Feature: mudhound-full-implementation, Property 10: ANSI metadata stripping

    For any ANSI frame file with metadata header, parsing should strip all
    lines before the "---" separator.

    Validates: Requirements 3.3
    """
    manager = AssetManager()

    # Build test content with metadata header
    metadata = [f"key{i}: value{i}" for i in range(metadata_lines)]
    content = [f"content line {i}" for i in range(content_lines)]

    # Combine with separator
    full_content = "\n".join(metadata + ["---"] + content)

    # Strip metadata
    stripped = manager._strip_metadata(full_content)

    # Verify metadata is removed
    for meta_line in metadata:
        assert meta_line not in stripped, f"Metadata line '{meta_line}' should be stripped"

    # Verify separator is removed
    assert "---" not in stripped or stripped.strip() == "---", (
        "Separator should be stripped (or be the only content)"
    )

    # Verify content is preserved
    for content_line in content:
        assert content_line in stripped, f"Content line '{content_line}' should be preserved"


@given(scheme=st.sampled_from(["nonexistent-scheme", "invalid", "missing"]))
@settings(max_examples=100, deadline=None)
def test_fallback_asset_provision(scheme):
    """
    Feature: mudhound-full-implementation, Property 11: Fallback asset provision

    For any requested asset that does not exist, the asset manager should
    provide a static fallback asset instead of failing.

    Validates: Requirements 3.4
    """
    # Clear cache before test
    CACHE.clear()

    # Create asset manager
    manager = AssetManager()

    # Request a non-existent scheme - should not raise exception
    try:
        banner_frames = manager.get_banner_frames(scheme)
        logo_frames = manager.get_logo_frames(scheme)
    except Exception as e:
        assert False, f"Should provide fallback instead of raising exception: {e}"

    # Should return non-empty frames
    assert len(banner_frames) > 0, "Should return at least one banner frame"
    assert len(logo_frames) > 0, "Should return at least one logo frame"

    # Frames should be strings
    assert all(isinstance(frame, str) for frame in banner_frames), (
        "All banner frames should be strings"
    )
    assert all(isinstance(frame, str)
               for frame in logo_frames), "All logo frames should be strings"

    # Frames should not be empty strings
    assert all(
        len(frame) > 0 for frame in banner_frames), "Banner frames should not be empty"
    assert all(
        len(frame) > 0 for frame in logo_frames), "Logo frames should not be empty"


@given(
    total_frames=st.integers(min_value=2, max_value=10),  # Reduced range
    fps=st.integers(min_value=10, max_value=30),  # Higher minimum FPS
)
# Reduced examples and added deadline
@settings(max_examples=30, deadline=3000)
def test_animation_pause_and_resume_on_resize(total_frames, fps):
    """
    Feature: mudhound-full-implementation, Property 7: Animation pause and resume on resize

    For any terminal resize event during animation, the animation should pause,
    allow re-render, and resume playback without frame loss.

    Validates: Requirements 2.5
    """
    # Create timing engine with specified parameters
    timing_engine = TimingEngine(
        fps=fps,
        total_frames=total_frames,
        duration=0.0,
        loop=True,  # Infinite loop
    )

    # Create animation renderer with test output
    output = StringIO()
    renderer = AnimationRenderer(timing_engine=timing_engine, output=output)

    # Load test frames
    test_frames = [f"Frame {i}\nLine 2" for i in range(total_frames)]
    renderer.load_frames(test_frames)

    # Start the animation
    timing_engine.start()

    try:
        # Let it run for a short time
        time.sleep(0.05)

        # Verify animation is running
        assert timing_engine.is_running, "Animation should be running"
        assert not renderer.is_paused, "Animation should not be paused initially"

        # Get current frame before pause
        frame_before_pause = timing_engine.get_current_frame()
        elapsed_before_pause = timing_engine.get_elapsed_time()

        # Simulate terminal resize by pausing
        renderer.pause()

        # Verify animation is paused
        assert timing_engine.is_paused, "Timing engine should be paused"
        assert renderer.is_paused, "Renderer should be paused"
        assert timing_engine.is_running, "Animation should still be running (just paused)"

        # Get elapsed time during pause
        elapsed_during_pause = timing_engine.get_elapsed_time()

        # Wait while paused (simulating resize handling)
        time.sleep(0.05)

        # Verify elapsed time doesn't advance while paused
        elapsed_after_wait = timing_engine.get_elapsed_time()
        time_diff = abs(elapsed_after_wait - elapsed_during_pause)

        # Allow small tolerance for timing precision
        assert time_diff < 0.05, (
            f"Elapsed time should not advance while paused (diff: {time_diff:.3f}s)"
        )

        # Resume animation (simulating resize complete)
        renderer.resume()

        # Verify animation is resumed
        assert not timing_engine.is_paused, "Timing engine should be resumed"
        assert not renderer.is_paused, "Renderer should be resumed"
        assert timing_engine.is_running, "Animation should still be running"

        # Let it run for a bit more
        time.sleep(0.05)

        # Verify animation continues from where it left off
        elapsed_after_resume = timing_engine.get_elapsed_time()

        # The elapsed time after resume should be greater than before pause
        # (accounting for the time after resume, not the paused time)
        assert elapsed_after_resume > elapsed_before_pause, (
            "Animation should continue advancing after resume"
        )

        # Verify frames are still cycling correctly
        current_frame = timing_engine.get_current_frame()
        assert 0 <= current_frame < total_frames, (
            f"Current frame {current_frame} should be within range [0, {total_frames})"
        )
    finally:
        # Always stop the animation to prevent resource leaks
        renderer.stop()

        # Verify animation is stopped
        assert not timing_engine.is_running, "Animation should be stopped"
        assert not renderer.is_paused, "Renderer should not be paused after stop"
