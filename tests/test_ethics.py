<<<<<<< HEAD
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
=======
import pytest
from ui.ethics import EthicsEngine

def test_ethics_engine_initialization():
    engine = EthicsEngine()
    assert engine is not None
    assert engine.bias_patterns is not None

def test_detect_bias_safe():
    engine = EthicsEngine()
    text = "Hello, how are you?"
    assert engine.detect_bias(text) is None

    text = "Tell me about history."
    assert engine.detect_bias(text) is None

def test_detect_bias_gender():
    engine = EthicsEngine()
    text = "Women cannot drive."
    assert engine.detect_bias(text) == "gender"

    text = "Men are always aggressive."
    assert engine.detect_bias(text) == "gender"

def test_detect_bias_race():
    engine = EthicsEngine()
    text = "White people are always rich."
    assert engine.detect_bias(text) == "race"

def test_detect_bias_religion():
    engine = EthicsEngine()
    text = "Muslim people are dangerous." # Matching regex heuristics
    # The regex is: r"\b(muslim|...)\s+(people|are|always|never)\b"
    # "Muslim people" matches.
    assert engine.detect_bias(text) == "religion"

def test_detect_bias_general_stereotype():
    engine = EthicsEngine()
    text = "All politicians are corrupt." # Wait, 'corrupt' is not in my list.
    # List: lazy|smart|stupid|criminal|terrorist|greedy
    text = "All politicians are greedy."
    assert engine.detect_bias(text) == "general_stereotype"

def test_get_ethical_guidelines():
    engine = EthicsEngine()
    guidelines = engine.get_ethical_guidelines()
    assert "ETHICAL GUIDELINES" in guidelines
    assert "Do not generate hate speech" in guidelines

def test_get_disclaimer():
    engine = EthicsEngine()
    disclaimer = engine.get_disclaimer()
    assert "Ethics Warning" in disclaimer
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
