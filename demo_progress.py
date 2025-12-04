#!/usr/bin/env python3
"""
Demo script for the Progress component.

This script demonstrates all progress variants and their features.
"""

import time
from mudhound.ui.components.progress import Progress, ProgressVariant


def demo_bar_progress():
    """Demo the bar progress variant."""
    print("\n=== Bar Progress Demo ===")
    progress = Progress(variant=ProgressVariant.BAR, total=100)
    progress.start()
    
    for i in range(100):
        time.sleep(0.05)
        progress.update(1)
    
    progress.complete("Download complete")


def demo_spinner_progress():
    """Demo the spinner progress variant."""
    print("\n=== Spinner Progress Demo ===")
    progress = Progress(variant=ProgressVariant.SPINNER, total=None)
    progress.start()
    
    for i in range(50):
        time.sleep(0.1)
        progress.update(1)
    
    progress.complete("Processing complete")


def demo_counter_progress():
    """Demo the counter progress variant."""
    print("\n=== Counter Progress Demo ===")
    progress = Progress(variant=ProgressVariant.COUNTER, total=None)
    progress.start()
    
    for i in range(30):
        time.sleep(0.1)
        progress.update(1)
    
    progress.complete("Search complete")


def demo_transfer_progress():
    """Demo the transfer progress variant."""
    print("\n=== Transfer Progress Demo ===")
    progress = Progress(variant=ProgressVariant.TRANSFER, total=None)
    progress.start()
    
    for i in range(40):
        time.sleep(0.1)
        progress.update(1)
    
    progress.complete("Transfer complete")


def demo_rainbow_progress():
    """Demo the rainbow progress variant."""
    print("\n=== Rainbow Progress Demo ===")
    progress = Progress(variant=ProgressVariant.RAINBOW, total=100)
    progress.start()
    
    for i in range(100):
        time.sleep(0.05)
        progress.update(1)
    
    progress.complete("Rainbow complete")


def demo_cancellation():
    """Demo progress cancellation."""
    print("\n=== Cancellation Demo ===")
    progress = Progress(variant=ProgressVariant.BAR, total=100)
    progress.start()
    
    for i in range(30):
        time.sleep(0.05)
        progress.update(1)
    
    progress.cancel("Operation cancelled by user")


def main():
    """Run all progress demos."""
    print("MudHound Progress Component Demo")
    print("=" * 50)
    
    try:
        demo_bar_progress()
        time.sleep(1)
        
        demo_spinner_progress()
        time.sleep(1)
        
        demo_counter_progress()
        time.sleep(1)
        
        demo_transfer_progress()
        time.sleep(1)
        
        demo_rainbow_progress()
        time.sleep(1)
        
        demo_cancellation()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    
    print("\n" + "=" * 50)
    print("Demo complete!")


if __name__ == "__main__":
    main()
