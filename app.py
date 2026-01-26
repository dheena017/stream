import streamlit as st
import ui.chat

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if __name__ == "__main__":
    # Launch the chat interface
    ui.chat.main()
