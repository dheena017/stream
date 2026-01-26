import streamlit as st
import ui.analytics as analytics
import ui.chat_utils as chat_utils

# Mock initialization functions for the purpose of the demo
def init_db():
    analytics.log_system_event("db_init")

def initialize_theme():
    pass

def initialize_all_states():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    try:
        analytics.configure_logging()
        analytics.log_system_event("app_startup")
        init_db()
        initialize_theme()
        initialize_all_states()
    except Exception as e:
        analytics.log_error("app_startup", str(e), e)
        st.error("Failed to initialize application.")
        return

    st.title("Streamlit AI Chat Analytics Demo")

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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

if __name__ == "__main__":
    main()
