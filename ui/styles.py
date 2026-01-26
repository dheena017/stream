import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .chat-header-container { padding: 1rem; }
    </style>
    """, unsafe_allow_html=True)
