import streamlit as st
import sys
import os

# Ensure we can import from ui
sys.path.append(os.getcwd())

from ui.chat_utils import generate_standard_response

st.set_page_config(page_title="Streamlit AI Chat", page_icon="🤖")

st.title("Streamlit AI Chat")

# Sidebar
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Provider", ["google", "openai", "anthropic"])
    api_key = st.text_input("API Key", type="password")

    api_keys = {provider: api_key}

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_standard_response(
            provider=provider,
            model_name="default",
            api_keys=api_keys,
            prompt=prompt,
            chat_history=st.session_state.messages[:-1], # Exclude current prompt
            config={}
        )
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# Resilience metrics
if "failure_metrics" in st.session_state:
    with st.expander("System Health"):
        st.write(st.session_state.failure_metrics)
