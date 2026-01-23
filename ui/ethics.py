import re
from typing import List, Dict

# Regex patterns for sensitive topics and potential bias triggers
# These are simplified examples for demonstration purposes.
SENSITIVE_TOPICS = {
    "gender": [
        (r"\b(man|woman|boy|girl|male|female|men|women)\b", r"\b(jobs|roles|capability|emotion|emotional)\b")
    ],
    "race": [
        (r"\b(white|black|asian|hispanic|latino|native)\b", r"\b(crime|intelligence|lazy|hardworking)\b")
    ],
    "religion": [
        (r"\b(christian|muslim|jewish|hindu|atheist)\b", r"\b(terrorist|violence|extremist|peaceful)\b")
    ]
}

def analyze_prompt_for_bias(text: str) -> List[str]:
    """
    Analyzes the input text for potential bias triggers.
    Returns a list of flags indicating the type of potential bias detected.
    """
    flags = []
    text_lower = text.lower()

    for category, patterns in SENSITIVE_TOPICS.items():
        for group_pattern, context_pattern in patterns:
            # Check if both the group identifier and the context keyword appear in the text
            if re.search(group_pattern, text_lower) and re.search(context_pattern, text_lower):
                flags.append(category)
                break # Avoid duplicate flags for the same category

    return flags

def get_ethics_guidelines() -> str:
    """
    Returns the ethical guidelines to be added to the system prompt.
    """
    return (
        "### Ethical Guidelines\n"
        "You are an AI assistant committed to ethical, fair, and unbiased interactions. "
        "Adhere to the following principles:\n"
        "1. **Fairness**: Avoid stereotypes based on race, gender, religion, sexual orientation, or background.\n"
        "2. **Neutrality**: Provide neutral, fact-based responses. Avoid taking sides in subjective debates unless grounded in universal human rights.\n"
        "3. **Inclusivity**: Use inclusive language. If asked about sensitive topics, present multiple viewpoints objectively.\n"
        "4. **Safety**: Do not generate hate speech, harmful content, or encourage illegal acts.\n"
        "### End of Guidelines\n"
    )

def get_disclaimer(flag: str) -> str:
    """
    Returns a disclaimer string based on the detected bias flag.
    """
    disclaimers = {
        "gender": "\n\n[Note: This response aims to be gender-neutral and avoid stereotypes associated with gender roles.]",
        "race": "\n\n[Note: This response is generated with a commitment to racial equality and avoidance of harmful stereotypes.]",
        "religion": "\n\n[Note: This response strives for religious neutrality and respect for diverse beliefs.]"
    }
    return disclaimers.get(flag, "")
