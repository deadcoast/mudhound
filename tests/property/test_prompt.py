"""Property-based tests for prompt component."""

from io import StringIO
from hypothesis import given, strategies as st, settings, assume
from mudhound.ui.components.prompt import Prompt, PromptType
from mudhound.utils.validators import (
    RangeValidator,
    PatternValidator,
    LengthValidator,
    EnumValidator,
)


@given(
    prompt_text=st.text(min_size=1, max_size=100, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))),
    default_value=st.one_of(st.none(), st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))))
)
@settings(max_examples=100, deadline=None)
def test_prompt_text_and_cursor_display(prompt_text, default_value):
    """
    Feature: mudhound-full-implementation, Property 35: Prompt text and cursor display
    
    For any prompt displayed, both the prompt text and input cursor should be visible.
    
    Validates: Requirements 12.1
    """
    # Create output stream
    output = StringIO()
    
    # Create prompt
    prompt = Prompt(
        prompt_text=prompt_text,
        prompt_type=PromptType.TEXT,
        default=default_value,
        use_color=False,  # Disable color for easier testing
        output=output
    )
    
    # Format the prompt (this is what gets displayed)
    formatted_prompt = prompt._format_prompt()
    
    # Verify prompt text is present
    assert prompt_text in formatted_prompt, (
        f"Prompt text '{prompt_text}' should be visible in formatted prompt"
    )

    
    # Verify cursor indicator (colon and space) is present
    assert ": " in formatted_prompt, (
        "Cursor indicator ': ' should be visible in formatted prompt"
    )
    
    # If default value is provided, verify it's shown
    if default_value is not None:
        assert f"[{default_value}]" in formatted_prompt, (
            f"Default value '[{default_value}]' should be visible in formatted prompt"
        )
    
    # Verify the formatted prompt is not empty
    assert len(formatted_prompt) > 0, "Formatted prompt should not be empty"


@given(
    prompt_text=st.text(min_size=1, max_size=100, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))),
    invalid_input=st.text(min_size=0, max_size=4, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))),
    min_length=st.integers(min_value=5, max_value=20)
)
@settings(max_examples=100, deadline=None)
def test_validation_error_feedback(prompt_text, invalid_input, min_length):
    """
    Feature: mudhound-full-implementation, Property 36: Validation error feedback
    
    For any invalid input to a prompt, an error message should be displayed
    and re-entry should be allowed.
    
    Validates: Requirements 12.3
    """
    # Only test cases where input is actually invalid (shorter than min_length)
    assume(len(invalid_input) < min_length)
    
    # Create output stream
    output = StringIO()
    
    # Create prompt with length validator
    prompt = Prompt(
        prompt_text=prompt_text,
        prompt_type=PromptType.TEXT,
        validators=[LengthValidator(min_length=min_length)],
        use_color=False,  # Disable color for easier testing
        output=output
    )
    
    # Test validation directly (not the full prompt flow to avoid hanging)
    is_valid, error_message = prompt._validate_input(invalid_input)
    
    # Verify validation failed
    assert not is_valid, (
        f"Input '{invalid_input}' with length {len(invalid_input)} should fail validation (min_length={min_length})"
    )
    
    # Verify error message is provided
    assert error_message is not None, (
        "Error message should be provided for invalid input"
    )
    
    # Verify error message mentions the constraint
    assert str(min_length) in error_message, (
        f"Error message should mention the minimum length {min_length}"
    )
    
    # Test that error formatting works
    formatted_error = prompt._format_error(error_message)
    assert len(formatted_error) > 0, (
        "Formatted error message should not be empty"
    )
    
    # Verify error indicator is present (glyph or text)
    assert "[!]" in formatted_error or "error" in formatted_error.lower(), (
        "Formatted error should contain error indicator"
    )



@given(
    min_value=st.floats(min_value=-1000, max_value=0, allow_nan=False, allow_infinity=False),
    max_value=st.floats(min_value=1, max_value=1000, allow_nan=False, allow_infinity=False),
    test_value=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=100, deadline=None)
def test_validation_rule_application_range(min_value, max_value, test_value):
    """
    Feature: mudhound-full-implementation, Property 37: Validation rule application
    
    For any validation rule (range, pattern, length, enum, custom), the prompt
    should correctly apply the rule to input.
    
    This test focuses on range validation.
    
    Validates: Requirements 12.5
    """
    # Ensure min < max
    assume(min_value < max_value)
    
    # Create range validator
    validator = RangeValidator(min_value=min_value, max_value=max_value)
    
    # Create output stream
    output = StringIO()
    
    # Create prompt with range validator
    prompt = Prompt(
        prompt_text="Enter number",
        prompt_type=PromptType.NUMBER,
        validators=[validator],
        use_color=False,
        output=output
    )
    
    # Test validation directly
    is_valid, error_message = prompt._validate_input(test_value)
    
    # Determine expected validity
    expected_valid = min_value <= test_value <= max_value
    
    # Verify validation result matches expectation
    assert is_valid == expected_valid, (
        f"Validation of {test_value} should be {expected_valid} for range [{min_value}, {max_value}]"
    )
    
    # If invalid, verify error message is provided
    if not expected_valid:
        assert error_message is not None, (
            "Error message should be provided for out-of-range value"
        )
        # Error message should mention the constraint
        assert "at least" in error_message or "at most" in error_message, (
            "Error message should mention the range constraint"
        )


@given(
    pattern=st.sampled_from([r"^\d+$", r"^[a-z]+$", r"^[A-Z][a-z]*$", r"^\w+@\w+\.\w+$"]),
    test_input=st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_categories=('Cs', 'Cc')))
)
@settings(max_examples=100, deadline=None)
def test_validation_rule_application_pattern(pattern, test_input):
    """
    Feature: mudhound-full-implementation, Property 37: Validation rule application
    
    This test focuses on pattern validation.
    
    Validates: Requirements 12.5
    """
    import re
    
    # Create pattern validator
    validator = PatternValidator(pattern=pattern)
    
    # Create output stream
    output = StringIO()
    
    # Create prompt with pattern validator
    prompt = Prompt(
        prompt_text="Enter text",
        prompt_type=PromptType.TEXT,
        validators=[validator],
        use_color=False,
        output=output
    )
    
    # Test validation directly
    is_valid, error_message = prompt._validate_input(test_input)
    
    # Determine expected validity
    expected_valid = bool(re.match(pattern, test_input))
    
    # Verify validation result matches expectation
    assert is_valid == expected_valid, (
        f"Validation of '{test_input}' should be {expected_valid} for pattern '{pattern}'"
    )
    
    # If invalid, verify error message is provided
    if not expected_valid:
        assert error_message is not None, (
            "Error message should be provided for non-matching pattern"
        )
        # Error message should mention pattern or matching
        assert "pattern" in error_message.lower() or "match" in error_message.lower(), (
            "Error message should mention pattern matching"
        )



@given(
    min_length=st.integers(min_value=1, max_value=20),
    max_length=st.integers(min_value=21, max_value=100),
    test_length=st.integers(min_value=0, max_value=100)
)
@settings(max_examples=100, deadline=None)
def test_validation_rule_application_length(min_length, max_length, test_length):
    """
    Feature: mudhound-full-implementation, Property 37: Validation rule application
    
    This test focuses on length validation.
    
    Validates: Requirements 12.5
    """
    # Ensure min < max
    assume(min_length < max_length)
    
    # Create length validator
    validator = LengthValidator(min_length=min_length, max_length=max_length)
    
    # Create test input of specified length
    test_input = "x" * test_length
    
    # Create output stream
    output = StringIO()
    
    # Create prompt with length validator
    prompt = Prompt(
        prompt_text="Enter text",
        prompt_type=PromptType.TEXT,
        validators=[validator],
        use_color=False,
        output=output
    )
    
    # Test validation directly
    is_valid, error_message = prompt._validate_input(test_input)
    
    # Determine expected validity
    expected_valid = min_length <= test_length <= max_length
    
    # Verify validation result matches expectation
    assert is_valid == expected_valid, (
        f"Validation of input with length {test_length} should be {expected_valid} for range [{min_length}, {max_length}]"
    )
    
    # If invalid, verify error message is provided
    if not expected_valid:
        assert error_message is not None, (
            "Error message should be provided for invalid length"
        )
        # Error message should mention the length constraint
        assert "characters" in error_message.lower() or "length" in error_message.lower(), (
            "Error message should mention length constraint"
        )


@given(
    choices=st.lists(st.text(min_size=1, max_size=20, alphabet=st.characters(blacklist_categories=('Cs', 'Cc'))), min_size=2, max_size=10, unique=True),
    choice_index=st.integers(min_value=0, max_value=9),
    invalid_choice=st.text(min_size=1, max_size=20, alphabet=st.characters(blacklist_categories=('Cs', 'Cc')))
)
@settings(max_examples=100, deadline=None)
def test_validation_rule_application_enum(choices, choice_index, invalid_choice):
    """
    Feature: mudhound-full-implementation, Property 37: Validation rule application
    
    This test focuses on enum validation.
    
    Validates: Requirements 12.5
    """
    # Ensure choice_index is valid
    assume(choice_index < len(choices))
    
    # Ensure invalid_choice is actually invalid
    assume(invalid_choice not in choices)
    
    # Create enum validator
    validator = EnumValidator(allowed_values=choices)
    
    # Select a valid choice
    valid_choice = choices[choice_index]
    
    # Create output stream
    output = StringIO()
    
    # Create prompt with enum validator
    prompt = Prompt(
        prompt_text="Select option",
        prompt_type=PromptType.CHOICE,
        validators=[validator],
        use_color=False,
        output=output
    )
    
    # Test validation of valid choice
    is_valid, error_message = prompt._validate_input(valid_choice)
    
    assert is_valid, (
        f"Valid choice '{valid_choice}' should pass validation"
    )
    assert error_message is None, (
        "No error message should be provided for valid choice"
    )
    
    # Test validation of invalid choice
    is_valid_invalid, error_message_invalid = prompt._validate_input(invalid_choice)
    
    assert not is_valid_invalid, (
        f"Invalid choice '{invalid_choice}' should fail validation"
    )
    assert error_message_invalid is not None, (
        "Error message should be provided for invalid choice"
    )
    # Error message should mention the allowed values
    assert "one of" in error_message_invalid.lower(), (
        "Error message should mention allowed values"
    )
