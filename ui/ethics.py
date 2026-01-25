<<<<<<< HEAD
<<<<<<< HEAD
"""
Ethics Guardian Module
Handles detection and mitigation of bias, harmful stereotypes, and unfair responses.
"""
from typing import Tuple, Optional, List

class EthicsGuardian:
    """
    Guardian class to check prompts and responses for ethical concerns.
    """

    def __init__(self):
        # Basic keyword lists for demonstration of bias detection
        # In a real system, this would use more advanced NLP or a dedicated safety model.
        self.sensitive_keywords = [
            "stereotype", "bias", "discrimination", "racist", "sexist",
            "prejudice", "hate speech", "slur", "supremacy"
        ]

        self.controversial_topics = [
            "political extremist", "hate group", "discrimination against"
        ]

    def check_safety(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Check if the text contains potentially unsafe or sensitive content.
        Returns (is_safe, issue_type).
        """
        if not text:
            return True, None

        text_lower = text.lower()

        for keyword in self.sensitive_keywords:
            if keyword in text_lower:
                return False, "sensitive_content"

        for topic in self.controversial_topics:
            if topic in text_lower:
                return False, "controversial_topic"

        return True, None

    def get_disclaimer(self, issue_type: str) -> str:
        """
        Get the appropriate disclaimer for the detected issue.
        """
        if issue_type == "sensitive_content":
            return "\n\n*Note: This content triggers sensitive topic filters. AI responses may reflect historical biases. Please verify important information.*"
        elif issue_type == "controversial_topic":
            return "\n\n*Note: This topic involves controversial subjects. The AI aims to be neutral but may lack nuance.*"
        else:
            return "\n\n*Note: Please verify AI generated content.*"

    def augment_system_instruction(self, original_instruction: str, issue_type: str) -> str:
        """
        Add ethical guidelines to system instructions based on detection.
        """
        guideline = " You must answer neutrally, avoiding stereotypes and bias. Present multiple viewpoints if applicable."

        if not original_instruction:
            return guideline.strip()

        return f"{original_instruction} {guideline}"
=======
import re
from typing import Optional, List, Dict

class EthicsEngine:
    """
    Handles ethics checks, bias detection, and mitigation strategies for the AI chat.
    """

    def __init__(self):
        # Regex patterns for potential bias detection
        # These are simple heuristics and not exhaustive
        self.bias_patterns = {
            "gender": r"\b(men|women|boys|girls|he|she)\s+(are|cannot|always|never)\b",
            "race": r"\b(white|black|asian|hispanic|latino|native)\s+(people|are|always|never)\b",
            "religion": r"\b(muslim|christian|jewish|hindu|atheist)\s+(people|are|always|never)\b",
            "general_stereotype": r"\b(all|every)\s+\w+\s+(is|are)\s+(lazy|smart|stupid|criminal|terrorist|greedy)\b"
        }

        self.guidelines = (
            "ETHICAL GUIDELINES:\n"
            "1. Do not generate hate speech, discrimination, or harmful stereotypes.\n"
            "2. Maintain neutrality and fairness when discussing sensitive topics (gender, race, religion, politics).\n"
            "3. If the user prompt implies a harmful stereotype, correct it gently or provide a balanced perspective.\n"
            "4. Prioritize safety and helpfulness.\n"
        )

        self.disclaimer = (
            "⚠️ **Ethics Warning**: This prompt touches on sensitive topics. "
            "The AI has been instructed to prioritize fairness and neutrality."
        )

    def detect_bias(self, text: str) -> Optional[str]:
        """
        Scans the text for potential bias patterns.
        Returns the type of bias detected, or None.
        """
        if not text:
            return None

        lower_text = text.lower()
        for category, pattern in self.bias_patterns.items():
            if re.search(pattern, lower_text):
                return category
        return None

    def get_ethical_guidelines(self) -> str:
        """Returns the ethical guidelines system instruction."""
        return self.guidelines

    def get_disclaimer(self) -> str:
        """Returns the user-facing disclaimer message."""
        return self.disclaimer
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
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
>>>>>>> origin/ethics-bias-fixes-185826756388721926
