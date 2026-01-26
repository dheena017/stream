import streamlit as st
import ui.chat_utils as chat_utils
import ui.analytics as analytics

def render_chat_interface():
    """
    Renders the main chat interface.
    """
    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input and response generation
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Simulate a provider call which will trigger logging in chat_utils
            response = chat_utils.generate_response("mock_provider", "mock_model", st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Check if response was an error (standardized error handling)
            if response.startswith("Error:"):
                 analytics.log_error("chat_interface", response)
