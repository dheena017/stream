import streamlit as st
from ui.database import save_feedback

def render_feedback_form():
    st.subheader("We value your feedback!")

    with st.form("feedback_form"):
        rating = st.slider("How would you rate your experience?", 1, 5, 5)
        comment = st.text_area("Please share your thoughts or report issues:")
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            # In a real app, user_id would come from session_state or auth
            user_id = st.session_state.get("username", "anonymous")
            save_feedback(user_id, rating, comment)
            st.success("Thank you for your feedback!")
