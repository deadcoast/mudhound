"""Demo script to test the AnimationRenderer."""

import time
from io import StringIO
from mudhound.ui.animation.engine import AnimationRenderer
from mudhound.ui.animation.timing import TimingEngine

def main():
    # Create test frames
    test_frames = [
        "Frame 1\n========\nThis is frame 1",
        "Frame 2\n========\nThis is frame 2",
        "Frame 3\n========\nThis is frame 3",
        "Frame 4\n========\nThis is frame 4",
    ]
    
    # Create timing engine (10 FPS, infinite loop)
    timing_engine = TimingEngine(
        fps=10,
        total_frames=len(test_frames),
        duration=0.0,
        loop=True
    )
    
    # Create animation renderer
    renderer = AnimationRenderer(timing_engine=timing_engine)
    
    # Load frames
    renderer.load_frames(test_frames)
    
    print("Testing AnimationRenderer...")
    print("Starting animation for 2 seconds...")
    
    # Start animation
    timing_engine.start()
    
    # Render frames for 2 seconds
    start_time = time.time()
    while time.time() - start_time < 2.0:
        renderer.render_frame()
        time.sleep(timing_engine.frame_duration)
    
    print("\nTesting pause/resume...")
    
    # Pause
    renderer.pause()
    print("Paused for 1 second...")
    time.sleep(1.0)
    
    # Resume
    renderer.resume()
    print("Resumed...")
    
    # Continue for 1 more second
    start_time = time.time()
    while time.time() - start_time < 1.0:
        renderer.render_frame()
        time.sleep(timing_engine.frame_duration)
    
    # Stop
    renderer.stop()
    renderer.clear()
    
    print("\nAnimation test complete!")
    print(f"Paused: {renderer.is_paused}")
    print(f"Running: {timing_engine.is_running}")

if __name__ == "__main__":
    main()
