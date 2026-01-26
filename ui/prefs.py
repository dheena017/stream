import streamlit as st
from ui.feedback import render_feedback_form

def render_prefs():
    st.header("Preferences")
    st.write("Manage your application settings here.")

    # ... existing prefs logic would go here ...

    st.markdown("---")
    render_feedback_form()
