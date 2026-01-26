
import streamlit as st
from ui.chat_utils import generate_standard_response, export_chat_to_json

def chat_interface():
    st.title("AI Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("Chat Options")
        if st.session_state.messages:
            json_str = export_chat_to_json(st.session_state.messages)
            st.download_button(
                label="Export Chat to JSON",
                data=json_str,
                file_name="chat_history.json",
                mime="application/json"
            )

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Dummy API keys and config for now. In a real app, these would come from st.secrets or user input.
            api_keys = {"openai": "dummy", "google": "dummy", "anthropic": "dummy"}
            response = generate_standard_response(
                provider="openai", # Default to openai
                model_name="gpt-3.5-turbo",
                api_keys=api_keys,
                prompt=prompt,
                chat_history=st.session_state.messages
            )
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    chat_interface()
