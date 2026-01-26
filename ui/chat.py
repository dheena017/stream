import streamlit as st
import time
from ui.engagement import EngagementManager

def render_chat():
    st.title("AI Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Log Engagement
        user_id = st.session_state.get("username", "test_user") or "test_user"
        manager = EngagementManager()
        result = manager.log_activity(user_id, "message_sent")

        if result["level_up"]:
            st.balloons()
            st.toast(f"🎉 Level Up! You are now Level {result['stats']['level']}!")

        for ach in result["new_achievements"]:
            st.toast(f"🏆 Achievement Unlocked: {ach['title']}!")

        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate AI response
            assistant_response = f"I received your message: '{prompt}'. Keep chatting to earn XP!"

            # Simulate typing
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
