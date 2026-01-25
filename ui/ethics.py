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
