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
