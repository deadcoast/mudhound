"""Demo script for the Confirmation component."""

from mudhound.ui.components.confirm import Confirmation, ConfirmationVariant


def demo_yesno():
    """Demo standard yes/no confirmation."""
    print("\n=== Standard Yes/No Confirmation (default NO) ===")
    confirmation = Confirmation(
        message="Do you want to proceed with this action?",
        variant=ConfirmationVariant.YESNO
    )
    # Uncomment to test interactively:
    # result = confirmation.confirm()
    # print(f"Result: {result}")
    print("Prompt format:", confirmation._format_prompt())
    print("Default value:", confirmation._get_default_value())


def demo_yesno_yes():
    """Demo yes/no confirmation with YES default."""
    print("\n=== Yes/No Confirmation (default YES) ===")
    confirmation = Confirmation(
        message="Continue with the installation?",
        variant=ConfirmationVariant.YESNO_YES
    )
    print("Prompt format:", confirmation._format_prompt())
    print("Default value:", confirmation._get_default_value())


def demo_destructive():
    """Demo destructive action confirmation."""
    print("\n=== Destructive Action Confirmation ===")
    confirmation = Confirmation(
        message="This will permanently delete all data!",
        variant=ConfirmationVariant.DESTRUCTIVE,
        confirmation_word="DELETE"
    )
    print("Message format:", confirmation._format_message())
    print("Prompt format:", confirmation._format_prompt())
    print("Default value:", confirmation._get_default_value())


def demo_timed():
    """Demo timed confirmation."""
    print("\n=== Timed Confirmation ===")
    confirmation = Confirmation(
        message="This action will timeout in 10 seconds",
        variant=ConfirmationVariant.TIMED,
        timeout=10.0
    )
    print("Prompt format:", confirmation._format_prompt())
    print("Default value:", confirmation._get_default_value())
    print("Timeout:", confirmation.timeout, "seconds")


if __name__ == "__main__":
    print("Confirmation Component Demo")
    print("=" * 50)

    demo_yesno()
    demo_yesno_yes()
    demo_destructive()
    demo_timed()

    print("\n" + "=" * 50)
    print("All demos completed!")
    print("\nTo test interactively, uncomment the confirmation.confirm() calls")
    print("in the demo functions and run again.")
