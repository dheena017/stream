import streamlit as st
import ui.analytics as analytics
import ui.chat_utils as chat_utils
from ui.chat import render_chat_interface
import ui.styles as styles

# Mock initialization functions for the purpose of the demo
def init_db():
    analytics.log_system_event("db_init")

def initialize_theme():
    styles.load_css()

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
    render_chat_interface()

if __name__ == "__main__":
    main()
