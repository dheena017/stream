import streamlit as st
import sys
import os

# Ensure we can import from ui
sys.path.append(os.getcwd())

from ui.database import init_db
from ui.prefs import render_prefs
from ui.dashboard import render_dashboard

# Initialize DB on startup
init_db()

st.set_page_config(page_title="AI Chat Feedback", layout="wide")

st.title("AI Chat App Integration Test")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Chat (Mock)", "Preferences", "Dashboard"])

if page == "Chat (Mock)":
    st.write("This is a mock chat interface.")
    st.info("Go to Preferences to leave feedback.")
elif page == "Preferences":
    render_prefs()
elif page == "Dashboard":
    render_dashboard()
