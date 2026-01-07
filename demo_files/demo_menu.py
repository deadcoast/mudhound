"""Demo script for Menu component."""

from mudhound.ui.components.menu import Menu


def main():
    """Demonstrate the Menu component."""
    print("=== Menu Component Demo ===\n")

    # Create a simple menu
    options = ["Search for URLs", "View history",
               "Export results", "Configure settings", "Quit"]

    menu = Menu(options=options, title="Main Menu", use_color=True)

    print("Menu will be displayed. Use:")
    print("  - Numbers (1-5) for direct selection")
    print("  - 'up' or 'u' to move up")
    print("  - 'down' or 'd' to move down")
    print("  - Enter to confirm")
    print("  - 'esc' to cancel")
    print()

    try:
        selected_index = menu.show()

        if selected_index is not None:
            print(f"\nYou selected: {options[selected_index]}")
        else:
            print("\nSelection cancelled")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")


if __name__ == "__main__":
    main()
