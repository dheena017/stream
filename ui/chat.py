import streamlit as st
import time
from ui.styles import get_css
from ui.chat_utils import generate_standard_response

def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def chat_interface():
    st.markdown(get_css(), unsafe_allow_html=True)
    init_chat_state()

    # Header with responsive design classes
    with st.container():
        st.markdown(
            """
            <div class="chat-header-container">
                <h1 class="main-header">AI Chat Assistant</h1>
                <div class="chat-status-container">
                    <span class="status-badge">🟢 Online</span>
                    <span class="status-badge">v2.0</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Chat History
    # We use a container for messages to ensure proper scrolling if needed (Streamlit handles this mostly)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        with st.chat_message("assistant"):
            # UI Improvement: Spinner
            with st.spinner("Analyzing request..."):
                try:
                    # Mock backend call
                    response = generate_standard_response(prompt, st.session_state.messages)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    # UI Improvement: Error Message
                    st.error(f"Unable to generate response. Error: {str(e)}")

def main():
    chat_interface()

if __name__ == "__main__":
    main()
