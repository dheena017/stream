import time
from ui import chat_utils
import streamlit as st

class AIBrain:
    def __init__(self):
        # Simulate heavy initialization (e.g. loading model)
        time.sleep(1.0)

    def process(self, prompt):
        # Check ethics
        if not chat_utils.check_safety(prompt):
            return "I cannot answer that."

        # Simulate processing time
        time.sleep(1.0)
        return f"Echo: {prompt}"

@st.cache_resource
def get_brain():
    return AIBrain()
