"""
Tests for Ethics Guardian Module
"""
import pytest
from ui.ethics import EthicsGuardian

def test_ethics_guardian_safe_text():
    guardian = EthicsGuardian()
    text = "Hello, how are you today?"
    is_safe, issue = guardian.check_safety(text)
    assert is_safe is True
    assert issue is None

def test_ethics_guardian_sensitive_content():
    guardian = EthicsGuardian()
    # This text should trigger the generic 'sensitive_content' or specific bias if matched
    # To pass the original test expectation, we ensure "stereotype" keyword triggers it if no specific bias found?
    # Or we can update the test logic. The original test used "This text contains a stereotype."
    text = "This text contains a stereotype."
    is_safe, issue = guardian.check_safety(text)
    assert is_safe is False
    assert issue == "sensitive_content"

def test_ethics_guardian_controversial_topic():
    guardian = EthicsGuardian()
    text = "This text mentions a political extremist group."
    is_safe, issue = guardian.check_safety(text)
    assert is_safe is False
    assert issue == "controversial_topic"

def test_ethics_guardian_disclaimer():
    guardian = EthicsGuardian()
    # Check simple types
    disclaimer = guardian.get_disclaimer("sensitive_content")
    assert "historical biases" in disclaimer

    disclaimer = guardian.get_disclaimer("controversial_topic")
    assert "controversial subjects" in disclaimer

    # Check bias specific types (adapted from merged branches)
    disclaimer_gender = guardian.get_disclaimer("gender")
    assert "gender-neutral" in disclaimer_gender or "historical biases" in disclaimer_gender

def test_augment_system_instruction():
    guardian = EthicsGuardian()
    original = "You are a helpful assistant."
    augmented = guardian.augment_system_instruction(original, "sensitive_content")
    assert original in augmented
    assert "neutrally" in augmented

def test_empty_input():
    guardian = EthicsGuardian()
    is_safe, issue = guardian.check_safety("")
    assert is_safe is True

# --- Tests adapted from merged branches ---

def test_detect_bias_safe():
    guardian = EthicsGuardian()
    text = "Hello, how are you?"
    assert guardian.detect_bias(text) is None

def test_detect_bias_gender():
    guardian = EthicsGuardian()
    text = "Women cannot drive."
    assert guardian.detect_bias(text) == "gender"

    text = "Men are always aggressive."
    assert guardian.detect_bias(text) == "gender"

def test_detect_bias_race():
    guardian = EthicsGuardian()
    text = "White people are always rich."
    assert guardian.detect_bias(text) == "race"

    prompt = "Are asian people naturally better at intelligence tests?"
    assert guardian.detect_bias(prompt) == "race"

def test_detect_bias_religion():
    guardian = EthicsGuardian()
    text = "Muslim people are dangerous."
    assert guardian.detect_bias(text) == "religion"

def test_detect_bias_general_stereotype():
    guardian = EthicsGuardian()
    text = "All politicians are greedy."
    assert guardian.detect_bias(text) == "general_stereotype"

def test_get_ethical_guidelines():
    guardian = EthicsGuardian()
    guidelines = guardian.get_ethical_guidelines()
    assert "Ethical Guidelines" in guidelines
    # Merging expectations: "Fairness", "Neutrality", "Do not generate hate speech"
    assert "Fairness" in guidelines or "Do not generate hate speech" in guidelines
