import time
import streamlit as st

@st.cache_data
def check_safety(prompt):
    # Simulate ethics check
    time.sleep(0.5)
    return True

def get_google_client():
    return "mock_google_client"

def get_google_genai_client():
    return "mock_google_genai_client"
