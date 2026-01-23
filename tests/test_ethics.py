import pytest
from ui.ethics import analyze_prompt_for_bias, get_ethics_guidelines, get_disclaimer

def test_analyze_prompt_for_bias_no_bias():
    prompt = "What is the capital of France?"
    flags = analyze_prompt_for_bias(prompt)
    assert flags == []

def test_analyze_prompt_for_bias_gender():
    prompt = "Why are women so emotional about their jobs?"
    flags = analyze_prompt_for_bias(prompt)
    assert "gender" in flags

def test_analyze_prompt_for_bias_race():
    prompt = "Are asian people naturally better at intelligence tests?"
    flags = analyze_prompt_for_bias(prompt)
    assert "race" in flags

def test_analyze_prompt_for_bias_religion():
    prompt = "Is a muslim always a terrorist?"
    flags = analyze_prompt_for_bias(prompt)
    assert "religion" in flags

def test_get_ethics_guidelines():
    guidelines = get_ethics_guidelines()
    assert "Ethical Guidelines" in guidelines
    assert "Fairness" in guidelines
    assert "Neutrality" in guidelines

def test_get_disclaimer():
    disclaimer = get_disclaimer("gender")
    assert "gender-neutral" in disclaimer

    disclaimer = get_disclaimer("race")
    assert "racial equality" in disclaimer

    disclaimer = get_disclaimer("unknown_flag")
    assert disclaimer == ""
