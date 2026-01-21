
import streamlit as st
import time
from datetime import datetime
import json
import logging
from ui.common import logout
from ui.auth import load_user_credentials, save_user_credentials, hash_password

def show_profile_page():
    """Display full profile page"""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h1>👤 My Profile</h1>
    </div>""", unsafe_allow_html=True)
    
    # Get user info
    user_info = st.session_state.get('user_info', {})
    is_oauth = 'google_oauth_token' in st.session_state
    
    # Profile header
    col_header1, col_header2 = st.columns([1, 3])
    
    with col_header1:
        if is_oauth and user_info.get('picture'):
            st.image(user_info['picture'], width=150)
        else:
            # Generate gradient avatar
            avatar_color = hash(st.session_state.username) % 360
            st.markdown(f'''
                <div style="width: 150px; height: 150px; border-radius: 50%; 
                background: linear-gradient(135deg, hsl({avatar_color}, 70%, 60%), hsl({avatar_color + 60}, 70%, 60%)); 
                display: flex; align-items: center; justify-content: center; 
                font-size: 4rem; color: white; font-weight: bold; margin: auto;">
                {st.session_state.username[0].upper()}
                </div>
            ''', unsafe_allow_html=True)
    
    with col_header2:
        st.markdown(f"## {user_info.get('name', st.session_state.username)}")
        avatar_url = user_info.get('avatar_url', None)
        if avatar_url:
            st.image(avatar_url, width=64)
        st.markdown(f"**Email:** {user_info.get('email', 'Not set')}")
        st.markdown(f"**Username:** {st.session_state.username}")
        st.markdown(f"**Account Type:** {'🔐 Google OAuth' if is_oauth else '🔐 Traditional Login'}")
        if st.button("Edit Profile", key="edit_profile_btn", help="Edit your profile information and preferences."):
            with st.popover("Edit Profile", use_container_width=True):
                new_name = st.text_input("Name", value=user_info.get('name', ''), key="edit_name")
                new_avatar = st.text_input("Avatar URL", value=user_info.get('avatar_url', ''), key="edit_avatar")
                if st.button("Save Changes", key="save_profile_btn"):
                    st.session_state.user_info['name'] = new_name
                    st.session_state.user_info['avatar_url'] = new_avatar
                    st.success("Profile updated!")
        # Quick stats
        total_messages = len(st.session_state.get('messages', []))
        st.caption(f"💬 {total_messages} messages sent this session")
        # Download chat/session history
        if st.session_state.get('messages'):
            if st.download_button("Download Chat History", data='\n'.join([m['content'] for m in st.session_state['messages']]), file_name="chat_history.txt", mime="text/plain", help="Download your chat history as a text file."):
                st.info("Chat history downloaded.")
        # Feedback form
        with st.expander("💡 Feedback / Suggestion"):
            feedback = st.text_area("Your feedback or suggestion:", key="feedback_text")
            if st.button("Submit Feedback", key="submit_feedback_btn"):
                logging.info(f"User feedback: {feedback}")
                st.success("Thank you for your feedback!")
    
    st.divider()
    
    # Tabbed interface
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics", "⚙️ Settings", "🎨 Preferences", "🔒 Security"])
    
    with tab1:
        st.markdown("### 📊 Usage Statistics")
        
        # Activity metrics
        col1, col2, col3, col4 = st.columns(4)
        learning_brain = st.session_state.get('learning_brain')
        stats = learning_brain.get_learning_stats() if learning_brain else {}
        
        with col1:
            st.metric("Total Messages", total_messages, help="Total number of messages exchanged in this session.")
        with col2:
            st.metric("Topics Learned", stats.get('total_topics', 0), help="Unique topics learned by the AI in this session.")
        with col3:
            st.metric("Models Used", stats.get('models_tracked', 0), help="Number of different AI models used.")
        with col4:
            st.metric("Conversations", stats.get('total_conversations', 0), help="Total separate conversations in this session.")
        
        st.markdown("### 🏆 Top Models Used")
        if stats.get('model_strengths'):
            for i, model_stat in enumerate(stats['model_strengths'][:5], 1):
                col_rank, col_model, col_stats = st.columns([0.5, 2, 2])
                with col_rank:
                    medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
                    st.markdown(f"### {medal}")
                with col_model:
                    st.markdown(f"**{model_stat['model']}**")
                    topics = ', '.join(model_stat.get('top_topics', [])[:3])
                    st.caption(f"Topics: {topics if topics else 'N/A'}")
                with col_stats:
                    st.progress(model_stat['success_rate'] / 100)
                    st.caption(f"Success: {model_stat['success_rate']}% ({model_stat['success']}/{model_stat['total']})")
        
        st.markdown("### 📈 Activity Timeline")
        joined_date = st.session_state.get("user_joined_date", datetime.now().strftime('%Y-%m-%d'))
        st.info(f"📅 Member since: {joined_date}")
        st.info(f"🔄 Total sessions: {st.session_state.get('total_sessions', 1)}")
    
    with tab2:
        st.markdown("### ⚙️ Account Settings")
        
        if not is_oauth:
            # Editable fields for traditional users
            users = load_user_credentials()
            user_data = users.get(st.session_state.username, {})
            
            st.markdown("#### Personal Information")
            new_name = st.text_input("Display Name", value=user_data.get('name', st.session_state.username))
            new_email = st.text_input("Email Address", value=user_data.get('email', ''))
            
            if st.button("💾 Save Changes", type="primary"):
                users[st.session_state.username]['name'] = new_name
                users[st.session_state.username]['email'] = new_email
                if save_user_credentials(users):
                    st.success("✅ Profile updated successfully!")
                    st.session_state.user_info = {
                        'name': new_name,
                        'email': new_email,
                        'username': st.session_state.username
                    }
                    st.rerun()
                else:
                    st.error("❌ Failed to save changes")
        else:
            st.info("🔒 Profile information is managed by Google OAuth and cannot be edited here.")
            st.markdown("**Current Information:**")
            st.text_input("Name", value=user_info.get('name', ''), disabled=True)
            st.text_input("Email", value=user_info.get('email', ''), disabled=True)
        
        st.markdown("#### Export Data")
        if st.button("📥 Download My Data"):
            user_data = {
                'profile': user_info,
                'messages': st.session_state.get('messages', []),
                'stats': stats,
                'preferences': st.session_state.get('profile_preferences', {})
            }
            st.download_button(
                "Download JSON",
                json.dumps(user_data, indent=2),
                file_name=f"{st.session_state.username}_data.json",
                mime="application/json"
            )
    
    with tab3:
        st.markdown("### 🎨 Preferences")
        
        prefs = st.session_state.get('profile_preferences', {})
        
        theme = st.selectbox("Theme", ["Dark"], index=0, help="Dark mode is now enforced.")
        
        language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese"],
                               index=["English", "Spanish", "French", "German", "Chinese"].index(prefs.get('language', 'English')))
        
        timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT", "IST"],
                               index=0)
        
        notifications = st.checkbox("Enable Notifications", value=prefs.get('notifications', True))
        
        auto_save = st.checkbox("Auto-save Chat History", value=True)
        
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.profile_preferences = {
                'theme': theme,
                'language': language,
                'timezone': timezone,
                'notifications': notifications,
                'auto_save': auto_save
            }
            
            # Apply Theme Change
            # Apply Theme Change
            st.session_state["dark_mode"] = True
            
            st.success("✅ Preferences saved! reloading...")
            time.sleep(0.5)
            st.rerun()
    
    with tab4:
        st.markdown("### 🔒 Security")
        
        if not is_oauth:
            st.markdown("#### Change Password")
            
            with st.form("change_password_form"):
                current_pwd = st.text_input("Current Password", type="password")
                new_pwd = st.text_input("New Password", type="password")
                confirm_pwd = st.text_input("Confirm New Password", type="password")
                
                submit = st.form_submit_button("🔒 Update Password", type="primary")
                
                if submit:
                    if not all([current_pwd, new_pwd, confirm_pwd]):
                        st.error("❌ Please fill all fields")
                    elif new_pwd != confirm_pwd:
                        st.error("❌ Passwords don't match")
                    elif len(new_pwd) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        users = load_user_credentials()
                        if users.get(st.session_state.username, {}).get('password') == hash_password(current_pwd):
                            users[st.session_state.username]['password'] = hash_password(new_pwd)
                            if save_user_credentials(users):
                                st.success("✅ Password updated successfully!")
                            else:
                                st.error("❌ Failed to update password")
                        else:
                            st.error("❌ Current password is incorrect")
        else:
            st.info("🔒 Password is managed by Google OAuth")
        
        st.markdown("#### Active Sessions")
        st.info(f"🟢 Current session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("#### Danger Zone")
        with st.expander("⚠️ Delete Account", expanded=False):
            st.warning("This action cannot be undone!")
            if st.button("🗑️ Delete My Account", type="secondary"):
                st.error("Account deletion is not implemented in this demo")
    
    st.divider()
    
    # Back button
    if st.button("← Back to Dashboard", width="stretch"):
        st.session_state.current_page = "dashboard"
        st.rerun()
