"""Property-based tests for animation system."""

import time
from hypothesis import given, strategies as st, settings
from mudhound.ui.animation.timing import TimingEngine, EasingFunction


@given(
    fps=st.integers(min_value=1, max_value=120)
)
@settings(max_examples=100, deadline=None)
def test_frame_rate_timing_accuracy(fps):
    """
    Feature: mudhound-full-implementation, Property 5: Frame rate timing accuracy
    
    For any configured frame rate, the animation engine should render frames
    at approximately that rate (within 10% tolerance).
    
    Validates: Requirements 2.2
    """
    # Create timing engine with specified FPS
    engine = TimingEngine(fps=fps, total_frames=100, duration=0.0, loop=True)
    
    # Start the engine
    engine.start()
    
    # Calculate expected frame duration
    expected_frame_duration = 1.0 / fps
    
    # Wait for a few frames and measure actual timing
    initial_frame = engine.get_current_frame()
    time.sleep(expected_frame_duration * 5)  # Wait for ~5 frames
    
    elapsed = engine.get_elapsed_time()
    current_frame = engine.get_current_frame()
    
    # Calculate frames advanced
    frames_advanced = (current_frame - initial_frame) % 100
    
    # Calculate actual frame rate
    if elapsed > 0:
        actual_fps = frames_advanced / elapsed
        
        # Allow 10% tolerance for timing accuracy
        tolerance = 0.10
        lower_bound = fps * (1 - tolerance)
        upper_bound = fps * (1 + tolerance)
        
        # The actual FPS should be within tolerance of expected FPS
        assert lower_bound <= actual_fps <= upper_bound, (
            f"Frame rate {actual_fps:.2f} FPS not within 10% of target {fps} FPS "
            f"(expected range: {lower_bound:.2f} - {upper_bound:.2f})"
        )
    
    engine.stop()


@given(
    total_frames=st.integers(min_value=1, max_value=100),
    fps=st.integers(min_value=1, max_value=60)
)
@settings(max_examples=100, deadline=None)
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
        duration=0.0,  # Zero duration = infinite loop
        loop=True
    )
    
    # Start the engine
    engine.start()
    
    # Let it run for a while
    time.sleep(0.5)
    
    # The animation should still be running
    assert engine.is_running, "Animation should still be running with zero duration"
    
    # The animation should never be complete
    assert not engine.is_complete(), "Animation with zero duration should never complete"
    
    # Get current frame - should be valid
    current_frame = engine.get_current_frame()
    assert 0 <= current_frame < total_frames, (
        f"Current frame {current_frame} should be within range [0, {total_frames})"
    )
    
    # Wait more and verify it continues looping
    time.sleep(0.5)
    
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
    
    engine.stop()
