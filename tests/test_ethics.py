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
    disclaimer = guardian.get_disclaimer("sensitive_content")
    assert "historical biases" in disclaimer

    disclaimer = guardian.get_disclaimer("controversial_topic")
    assert "controversial subjects" in disclaimer

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
