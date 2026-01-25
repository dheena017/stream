import streamlit as st
import os
import json
import logging
from cryptography.fernet import Fernet
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

KEY_FILE = "secret.key"

class PrivacyManager:
    _instance = None
    _cipher_suite = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrivacyManager, cls).__new__(cls)
            cls._instance._initialize_cipher()
        return cls._instance

    def _initialize_cipher(self):
        """Initialize the Fernet cipher suite with a key."""
        key = os.getenv("ANTIGRAVITY_KEY")

        if not key:
            if os.path.exists(KEY_FILE):
                try:
                    with open(KEY_FILE, "rb") as key_file:
                        key = key_file.read()
                except Exception as e:
                    logger.error(f"Error reading key file: {e}")

        if not key:
            # Generate and save new key
            key = Fernet.generate_key()
            try:
                with open(KEY_FILE, "wb") as key_file:
                    key_file.write(key)
                logger.info("New encryption key generated and saved.")
            except Exception as e:
                logger.error(f"Error saving key file: {e}")

        try:
            self._cipher_suite = Fernet(key)
        except Exception as e:
            logger.error(f"Error initializing cipher suite: {e}")
            # Fallback to no-op or handle critical error
            self._cipher_suite = None

    def encrypt(self, data: str) -> str:
        """Encrypts a string."""
        if not self._cipher_suite or not data:
            return data
        try:
            if isinstance(data, str):
                encoded_text = data.encode()
            else:
                encoded_text = str(data).encode()
            encrypted_text = self._cipher_suite.encrypt(encoded_text)
            return encrypted_text.decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data

    def decrypt(self, data: str) -> str:
        """Decrypts a string."""
        if not self._cipher_suite or not data:
            return data
        try:
            # Check if it looks like a fernet token (basic check)
            # Fernet tokens are base64 encoded and usually start with gAAAA
            if not data.startswith("gAAAA"):
                return data

            decrypted_text = self._cipher_suite.decrypt(data.encode())
            return decrypted_text.decode()
        except Exception as e:
            # If decryption fails, it might be plain text (migration scenario)
            # logger.debug(f"Decryption failed (returning original): {e}")
            return data

def show_privacy_page():
    """Render the Privacy & Security page."""
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1>🔒 Privacy & Security</h1>
        <p style="color: #9ca3af;">Manage your data, privacy settings, and security preferences.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_policy, tab_data = st.tabs(["📜 Privacy Policy", "💾 Data Control"])

    with tab_policy:
        st.markdown("""
        ### Privacy Policy

        **Effective Date:** Today

        At **Antigravity AI**, we prioritize your privacy and data security. This policy outlines how we handle your data.

        #### 1. Data Collection
        - **Conversations:** We store your chat history locally to provide context for the AI.
        - **Account Info:** We store your username and hashed password if you register.
        - **Usage Data:** We may collect anonymous usage metrics to improve the application.

        #### 2. Data Storage & Security
        - **Encryption:** Your messages are encrypted at rest using industry-standard encryption (Fernet/AES).
        - **Local Storage:** Data is stored in a local SQLite database (`chat_history.db`).
        - **No Third-Party Sharing:** We do not sell your personal data to third parties. AI model providers (Google, OpenAI, etc.) receive your prompts to generate responses, subject to their respective privacy policies.

        #### 3. User Rights
        - **Access:** You can view and export your data at any time.
        - **Deletion:** You can delete your account and all associated data permanently.

        #### 4. Contact
        If you have questions, please contact support.
        """)

    with tab_data:
        st.markdown("### Manage Your Data")

        st.info("You have full control over your data. You can export it for your records or permanently delete it.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📤 Export Data")
            st.markdown("Download a copy of all your conversations and messages.")

            if st.button("Download My Data", type="secondary"):
                from ui.database import get_all_user_data
                user_id = st.session_state.get('username')
                if user_id:
                    data = get_all_user_data(user_id)
                    json_str = json.dumps(data, indent=2, default=str)
                    st.download_button(
                        label="Click to Download JSON",
                        data=json_str,
                        file_name=f"antigravity_export_{user_id}.json",
                        mime="application/json"
                    )
                else:
                    st.error("You must be logged in to export data.")

        with col2:
            st.markdown("#### 🗑️ Delete Account")
            st.markdown("Permanently remove your account and all chat history. **This cannot be undone.**")

            with st.expander("Danger Zone"):
                st.warning("This action is irreversible.")
                confirm_text = st.text_input("Type 'DELETE' to confirm:")

                if st.button("Permanently Delete My Data", type="primary"):
                    if confirm_text == "DELETE":
                        from ui.database import delete_all_user_data
                        from ui.auth import load_user_credentials, save_user_credentials

                        user_id = st.session_state.get('username')
                        if user_id:
                            # 1. Delete DB Data
                            delete_all_user_data(user_id)

                            # 2. Delete Account from users.json
                            users = load_user_credentials()
                            if user_id in users:
                                del users[user_id]
                                save_user_credentials(users)

                            # 3. Log out
                            st.success("Account deleted successfully. Redirecting...")
                            st.session_state.clear()
                            st.rerun()
                        else:
                            st.error("User not found.")
                    else:
                        st.error("Confirmation text does not match.")
