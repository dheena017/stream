import streamlit as st
from ui.database import save_feedback

def render_feedback_form(key_suffix="default"):
    """Render the feedback form."""
    form_key = f"feedback_form_{key_suffix}"
    with st.form(form_key, clear_on_submit=True):
        st.subheader("We value your feedback!")

        category = st.selectbox(
            "Category",
            ["General", "Bug Report", "Feature Request", "Model Performance", "UI/UX"],
            key=f"fb_cat_{key_suffix}"
        )

        rating = st.slider("Rating", 1, 5, 5, key=f"fb_rate_{key_suffix}")

        comment = st.text_area("Comments", placeholder="Tell us what you think...", key=f"fb_comment_{key_suffix}")

        # Anonymity toggle
        is_anonymous = st.checkbox("Submit Anonymously", value=True, key=f"fb_anon_{key_suffix}")

        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if not comment and rating < 3: # Require comment for low ratings
                 st.warning("Please explain why you gave a low rating.")
            else:
                user_id = "Anonymous"
                if not is_anonymous and 'username' in st.session_state:
                    user_id = st.session_state.username

                try:
                    save_feedback(user_id, category, rating, comment)
                    st.success("Thank you for your feedback!")
                except Exception as e:
                    st.error(f"Error saving feedback: {e}")
