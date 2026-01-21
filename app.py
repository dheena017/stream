import os
import base64
from io import BytesIO
import tempfile
from typing import List, Dict, Any, Optional, Tuple
import hashlib
import json
from datetime import datetime
import time
import platform
import sys

from google import genai
from brain_learning import LearningBrain
import streamlit as st
from PIL import Image

# Force native DNS to avoid SRV lookups that can time out in some networks
os.environ.setdefault("GRPC_DNS_RESOLVER", "native")

# --- AUTHENTICATION ---

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_user_credentials() -> Dict[str, Dict[str, str]]:
    """Load user credentials from file or environment"""
    # Try loading from JSON file
    users_file = "users.json"
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                users_data = json.load(f)
                return users_data
        except Exception:
            pass
    
    # Default credentials with email support
    return {
        "admin": {
            "password": hash_password(os.getenv("ADMIN_PASSWORD", "admin123")),
            "email": "admin@example.com",
            "name": "Admin User"
        },
        "user": {
            "password": hash_password(os.getenv("USER_PASSWORD", "user123")),
            "email": "user@example.com",
            "name": "Regular User"
        }
    }

def save_user_credentials(users: Dict[str, Dict[str, str]]) -> bool:
    """Save user credentials to file"""
    try:
        with open("users.json", 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception:
        return False

def check_login(username_or_email: str, password: str) -> Optional[Dict[str, str]]:
    """Verify login credentials - accepts username or email"""
    users = load_user_credentials()
    
    # Check if input is username
    if username_or_email in users:
        user_data = users[username_or_email]
        if user_data["password"] == hash_password(password):
            return {
                "username": username_or_email,
                "email": user_data.get("email", ""),
                "name": user_data.get("name", username_or_email)
            }
    
    # Check if input is email
    for username, user_data in users.items():
        if user_data.get("email", "").lower() == username_or_email.lower():
            if user_data["password"] == hash_password(password):
                return {
                    "username": username,
                    "email": user_data.get("email", ""),
                    "name": user_data.get("name", username)
                }
    
    return None

def register_user(username: str, email: str, password: str, name: str = "") -> bool:
    """Register a new user"""
    users = load_user_credentials()
    
    # Check if username already exists
    if username in users:
        return False
    
    # Check if email already exists
    for user_data in users.values():
        if user_data.get("email", "").lower() == email.lower():
            return False
    
    # Add new user
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "name": name or username
    }
    
    return save_user_credentials(users)

def verify_google_oauth() -> Optional[Dict[str, Any]]:
    """Verify Google OAuth token and return user info"""
    try:
        from google.oauth2 import id_token  # type: ignore
        from google.auth.transport import requests  # type: ignore
        
        # Get client ID from environment
        client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        if not client_id:
            return None
        
        # Check if we have a token in session state
        if "google_oauth_token" in st.session_state:
            token = st.session_state.google_oauth_token
            try:
                # Verify the token
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
                
                if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    return None
                
                return {
                    'email': idinfo.get('email'),
                    'name': idinfo.get('name'),
                    'picture': idinfo.get('picture'),
                    'sub': idinfo.get('sub')
                }
            except Exception:
                return None
        return None
    except ImportError:
        return None

def create_google_oauth_url() -> str:
    """Create Google OAuth authorization URL"""
    client_id = os.getenv("GOOGLE_CLIENT_ID", "")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8501")
    
    scope = "openid email profile"
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=token&"
        f"scope={scope}"
    )
    return auth_url

def show_login_page():
    """Display enhanced login page with animations"""
    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .login-header {
            text-align: center;
            animation: fadeIn 0.8s ease-out;
            margin-bottom: 2rem;
        }
        .login-header h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        .feature-card {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #667eea;
            animation: slideIn 0.6s ease-out;
        }
        .google-btn {
            background: linear-gradient(135deg, #4285f4 0%, #357ae8 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            width: 100%;
            text-align: center;
            font-weight: 600;
            margin-top: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
        }
        .google-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
        }
        .stats-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Hero section
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown('<div class="login-header"><h1>🤖 AI Assistant</h1><div class="login-subtitle">Your intelligent multi-model AI companion</div></div>', unsafe_allow_html=True)
        
        # Feature highlights
        st.markdown(
            '<div class="feature-card">✨ <strong>25+ AI Models</strong> from Google, OpenAI, Anthropic, Meta & more</div>'
            '<div class="feature-card">🧠 <strong>AI Brain Mode</strong> - Combines multiple models for enhanced responses</div>'
            '<div class="feature-card">🌐 <strong>Internet Search</strong> - Real-time information from the web</div>'
            '<div class="feature-card">📎 <strong>Multimodal</strong> - Images, PDFs, Audio & Video support</div>',
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Check for Google OAuth
        google_client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        
        if google_client_id:
            st.markdown("#### 🔐 Sign in with Google")
            
            # JavaScript to handle OAuth redirect and extract token from URL
            oauth_code = st.text_input(
                "Google OAuth Token (auto-filled from redirect)",
                type="password",
                key="oauth_token_input",
                help="This will be auto-filled after Google authentication"
            )
            
            if oauth_code:
                st.session_state.google_oauth_token = oauth_code
                user_info = verify_google_oauth()
                if user_info:
                    st.session_state.authenticated = True
                    st.session_state.username = user_info['email']
                    st.session_state.user_info = user_info
                    st.success("✅ Google login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Google OAuth token")
            
            oauth_url = create_google_oauth_url()
            st.markdown(f'<a href="{oauth_url}" target="_blank" class="google-btn">🔐 Sign in with Google</a>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### Or use Email/Username Login")
        
        # Tabs for Login and Register
        tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab_login:
            username_or_email = st.text_input(
                "Email or Username", 
                key="login_username", 
                placeholder="Enter email or username"
            )
            password = st.text_input(
                "Password", 
                type="password", 
                key="login_password", 
                placeholder="Enter password"
            )
            
            st.markdown("")
            
            col_login, col_info = st.columns([1, 1])
            
            with col_login:
                if st.button("🔐 Login", use_container_width=True, type="primary"):
                    if username_or_email and password:
                        user_data = check_login(username_or_email, password)
                        if user_data:
                            st.session_state.authenticated = True
                            st.session_state.username = user_data['username']
                            st.session_state.user_info = user_data
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email/username or password")
                    else:
                        st.warning("⚠️ Please enter both email/username and password")
            
            with col_info:
                with st.popover("ℹ️ Info"):
                    st.markdown("**Default Credentials:**")
                    st.code("Email: admin@example.com\nUsername: admin\nPassword: admin123")
                    st.markdown("---")
                    st.markdown("**Login with email or username**")
                    st.caption("You can use either your email address or username to login")
                    if google_client_id:
                        st.markdown("---")
                        st.markdown("**Google OAuth Setup:**")
                        st.caption("Set GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI in environment variables")
        
        with tab_register:
            st.markdown("#### Create New Account")
            reg_name = st.text_input("Full Name", key="reg_name", placeholder="Enter your full name")
            reg_email = st.text_input("Email Address", key="reg_email", placeholder="Enter your email")
            reg_username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
            reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Choose a password")
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm", placeholder="Confirm password")
            
            st.markdown("")
            
            if st.button("📝 Register", use_container_width=True, type="primary"):
                if not all([reg_name, reg_email, reg_username, reg_password, reg_password_confirm]):
                    st.warning("⚠️ Please fill in all fields")
                elif reg_password != reg_password_confirm:
                    st.error("❌ Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif "@" not in reg_email or "." not in reg_email:
                    st.error("❌ Please enter a valid email address")
                else:
                    if register_user(reg_username, reg_email, reg_password, reg_name):
                        st.success("✅ Registration successful! You can now login.")
                        st.balloons()
                    else:
                        st.error("❌ Username or email already exists")
        
        st.markdown("---")
        st.caption("🔒 Your credentials are secure and never stored in plain text")


def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    if "google_oauth_token" in st.session_state:
        del st.session_state.google_oauth_token
    if "user_info" in st.session_state:
        del st.session_state.user_info
    st.rerun()

# --- HELPER FUNCTIONS ---

@st.cache_resource
def get_openai_client(api_key: str, base_url: Optional[str] = None):
    """Cached OpenAI client initialization"""
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

@st.cache_resource
def get_anthropic_client(api_key: str):
    """Cached Anthropic client initialization"""
    from anthropic import Anthropic
    return Anthropic(api_key=api_key)

def build_conversation_history(messages: List[Dict], exclude_last: bool = True) -> List[Dict]:
    """Build conversation history from messages"""
    history = messages[:-1] if exclude_last and len(messages) > 0 else messages
    return [{"role": msg["role"], "content": msg["content"]} for msg in history]

def create_openai_messages(
    conversation_history: List[Dict],
    current_prompt: str,
    system_instruction: Optional[str] = None
) -> List[Dict]:
    """Create messages array for OpenAI-compatible APIs"""
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": current_prompt})
    return messages

def handle_openai_compatible_provider(
    client: Any,
    model_name: str,
    messages: List[Dict],
    temperature: float,
    max_tokens: int,
    top_p: float,
    enable_streaming: bool
) -> str:
    """Handle API calls for OpenAI-compatible providers (OpenAI, Together, xAI, DeepSeek)"""
    if enable_streaming:
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True
        )
        collected_chunks: List[str] = []
        def _iter_chunks():
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                collected_chunks.append(piece)
                yield piece
        st.write_stream(_iter_chunks())
        return "".join(collected_chunks)
    else:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        response_text = response.choices[0].message.content
        st.markdown(response_text)
        return response_text

# --- DASHBOARD FUNCTIONS ---

def show_profile_page():
    """Display full profile page"""
    st.markdown('<div class="login-header"><h1>👤 My Profile</h1></div>', unsafe_allow_html=True)
    
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
        st.markdown(f"**Email:** {user_info.get('email', 'Not set')}")
        st.markdown(f"**Username:** {st.session_state.username}")
        st.markdown(f"**Account Type:** {'🔐 Google OAuth' if is_oauth else '🔐 Traditional Login'}")
        
        # Quick stats
        total_messages = len(st.session_state.get('messages', []))
        st.caption(f"💬 {total_messages} messages sent this session")
    
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
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("Topics Learned", stats.get('total_topics', 0))
        with col3:
            st.metric("Models Used", stats.get('models_tracked', 0))
        with col4:
            st.metric("Conversations", stats.get('total_conversations', 0))
        
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
        
        theme = st.selectbox("Theme", ["Auto", "Light", "Dark"], 
                           index=["Auto", "Light", "Dark"].index(prefs.get('theme', 'Auto')))
        
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
            st.success("✅ Preferences saved!")
    
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
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "dashboard"
        st.rerun()

def show_dashboard():
    """Display user dashboard with stats and activity"""
    st.markdown('<div class="login-header"><h1>📊 Dashboard</h1></div>', unsafe_allow_html=True)
    
    # User info
    user_info = st.session_state.get('user_info', {})
    user_name = user_info.get('name', st.session_state.username)
    user_email = user_info.get('email', '')
    
    st.markdown(f"### Welcome back, {user_name}! 👋")
    if user_email:
        st.caption(f"📧 {user_email}")
    
    st.divider()
    
    # Activity metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_messages = len(st.session_state.get('messages', []))
    learning_brain = st.session_state.get('learning_brain')
    stats = learning_brain.get_learning_stats() if learning_brain else {}
    
    with col1:
        st.metric("💬 Total Messages", total_messages, delta=None)
    with col2:
        st.metric("🧠 Topics Learned", stats.get('total_topics', 0))
    with col3:
        st.metric("🤖 Models Used", stats.get('models_tracked', 0))
    with col4:
        st.metric("📚 Conversations", stats.get('total_conversations', 0))
    
    st.divider()
    
    # Enhanced Quick actions with descriptions
    st.markdown("### 🚀 Quick Actions")
    
    # Create action cards with descriptions
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">💬 Start Chatting</div>
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">Begin a new conversation with your selected AI model or enable AI Brain for multi-model responses</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Open Chat", use_container_width=True, type="primary", key="quick_chat_btn"):
            st.session_state.current_page = "chat"
            st.rerun()
    
    with action_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb15 0%, #f5576c15 100%); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #f5576c; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">👤 View Profile</div>
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">Manage your account settings, preferences, and view your usage statistics</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Go to Profile", use_container_width=True, key="quick_profile_btn"):
            st.session_state.current_page = "profile"
            st.rerun()
    
    action_col3, action_col4 = st.columns(2)
    
    with action_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe15 0%, #00f2fe15 100%); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #00f2fe; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🧠 View Brain Stats</div>
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">See what your AI brain has learned: topics, model performance, and insights</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Show Stats", use_container_width=True, key="quick_brain_btn"):
            st.session_state.show_brain_stats = not st.session_state.get('show_brain_stats', False)
            st.rerun()
    
    with action_col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a15 0%, #fee14015 100%); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #fee140; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📥 Export Chat</div>
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">Download your chat history as JSON for backup, analysis, or sharing</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Download", use_container_width=True, key="quick_export_btn"):
            if st.session_state.messages:
                chat_export = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    "📥 Download Chat History",
                    chat_export,
                    file_name="chat_history.json",
                    mime="application/json",
                    use_container_width=True,
                    key="download_chat_btn"
                )
            else:
                st.warning("No chat history to export. Start a conversation first!")
    
    # Additional quick action shortcuts
    st.markdown("---")
    st.markdown("### ⚡ Additional Actions")
    
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    
    with quick_col1:
        if st.button("🔄 Clear Chat", use_container_width=True, key="clear_chat_quick"):
            st.session_state.messages = []
            st.success("✅ Chat cleared!")
            st.rerun()
    
    with quick_col2:
        if st.button("🧠 Reset Brain", use_container_width=True, key="reset_brain_quick"):
            learning_brain = st.session_state.learning_brain
            learning_brain.reset_learning()
            st.success("✅ Brain reset!")
            st.rerun()
    
    with quick_col3:
        if st.button("⚙️ Settings", use_container_width=True, key="settings_quick"):
            st.info("✅ Settings available in the sidebar Control Panel")
    
    with quick_col4:
        if st.button("📊 Refresh Stats", use_container_width=True, key="refresh_stats_quick"):
            st.rerun()
    
    # Brain stats display
    if st.session_state.get('show_brain_stats', False):
        st.divider()
        st.markdown("### 🧠 AI Brain Learning Stats")
        
        if stats.get('model_strengths'):
            st.markdown("#### Model Performance")
            for model_stat in stats['model_strengths'][:5]:
                col_model, col_rate, col_total = st.columns([2, 1, 1])
                with col_model:
                    st.markdown(f"**{model_stat['model']}**")
                with col_rate:
                    st.metric("Success Rate", f"{model_stat['success_rate']}%")
                with col_total:
                    st.metric("Queries", f"{model_stat['success']}/{model_stat['total']}")
        
        if stats.get('top_topics'):
            st.markdown("#### Top Knowledge Topics")
            cols = st.columns(min(len(stats['top_topics']), 5))
            for i, topic_info in enumerate(stats['top_topics'][:5]):
                with cols[i]:
                    st.metric(topic_info['topic'], topic_info['count'])
    
    # Recent activity
    st.divider()
    st.markdown("### 📝 Recent Activity")
    
    recent_messages = st.session_state.get('messages', [])[-5:]
    if recent_messages:
        for msg in recent_messages:
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            with st.expander(f"{role_icon} {msg['role'].title()} - {msg['content'][:50]}..."):
                st.markdown(msg['content'])
    else:
        st.info("No recent activity. Start a conversation to see your history here!")
    
    st.divider()
    
    # Enhanced system info
    with st.expander("ℹ️ System Information", expanded=False):
        st.markdown("### 📊 Session Information")
        
        # Session details
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Session Start", datetime.now().strftime('%H:%M:%S'))
            st.metric("Session Date", datetime.now().strftime('%Y-%m-%d'))
        with col_info2:
            uptime_seconds = time.time() - st.session_state.get('session_start_time', time.time())
            st.metric("Session Duration", f"{int(uptime_seconds // 60)} min")
            st.metric("Current Time", datetime.now().strftime('%I:%M %p'))
        
        st.markdown("---")
        st.markdown("### 👤 User Information")
        
        user_info = st.session_state.get('user_info', {})
        col_user1, col_user2 = st.columns(2)
        
        with col_user1:
            st.text_input("Username", value=st.session_state.username, disabled=True)
            st.text_input("Display Name", value=user_info.get('name', st.session_state.username), disabled=True)
        with col_user2:
            auth_method = "🔐 Google OAuth" if 'google_oauth_token' in st.session_state else "🔐 Traditional Login"
            st.text_input("Authentication", value=auth_method, disabled=True)
            st.text_input("Email", value=user_info.get('email', 'Not set'), disabled=True)
        
        st.markdown("---")
        st.markdown("### 💻 System Details")
        
        col_sys1, col_sys2, col_sys3 = st.columns(3)
        
        with col_sys1:
            st.metric("Platform", platform.system())
            st.metric("Python", platform.python_version())
        
        with col_sys2:
            st.metric("Streamlit", st.__version__)
            st.metric("Browser", "Chrome/Safari/Firefox")
        
        with col_sys3:
            total_messages = len(st.session_state.get('messages', []))
            st.metric("Messages", total_messages)
            st.metric("Files Uploaded", len(st.session_state.get('uploaded_files', [])))
        
        st.markdown("---")
        st.markdown("### 🤖 AI Information")
        
        learning_brain = st.session_state.get('learning_brain')
        stats = learning_brain.get_learning_stats() if learning_brain else {}
        
        col_ai1, col_ai2, col_ai3 = st.columns(3)
        
        with col_ai1:
            st.metric("Topics Learned", stats.get('total_topics', 0))
            st.metric("Conversations", stats.get('total_conversations', 0))
        
        with col_ai2:
            st.metric("Models Tracked", stats.get('models_tracked', 0))
            model_perf = stats.get('model_performance', {})
            st.metric("Total Model Calls", sum(m.get('total', 0) for m in model_perf.values()))
        
        with col_ai3:
            if stats.get('model_strengths'):
                best_model = stats['model_strengths'][0]
                st.metric("Best Model", best_model['model'][:15] + "...")
                st.metric("Best Success Rate", f"{best_model['success_rate']}%")
        
        st.markdown("---")
        st.markdown("### 🎛️ Configuration")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            prefs = st.session_state.get('profile_preferences', {})
            st.text_input("Theme", value=prefs.get('theme', 'Auto'), disabled=True)
            st.text_input("Language", value=prefs.get('language', 'English'), disabled=True)
        
        with col_config2:
            st.text_input("Timezone", value=prefs.get('timezone', 'UTC'), disabled=True)
            notifications_status = "✅ Enabled" if prefs.get('notifications', True) else "❌ Disabled"
            st.text_input("Notifications", value=notifications_status, disabled=True)
        
        st.markdown("---")
        st.markdown("### 🔧 Feature Status")
        
        col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)
        
        with col_feat1:
            voice_status = "🔊 On" if st.session_state.voice_mode else "🔇 Off"
            st.metric("Voice Mode", voice_status)
        
        with col_feat2:
            multimodal_count = len(st.session_state.get('multimodal_options', []))
            st.metric("Multimodal", f"{multimodal_count} types")
        
        with col_feat3:
            streaming_status = "✅ On" if st.session_state.get('enable_streaming', True) else "❌ Off"
            st.metric("Streaming", streaming_status)
        
        with col_feat4:
            brain_status = "🧠 On" if st.session_state.get('enable_brain_mode', False) else "⚪ Off"
            st.metric("Brain Mode", brain_status)
        
        st.markdown("---")
        st.markdown("### 📝 Quick Debug Info")
        
        with st.expander("🔍 Developer Info", expanded=False):
            col_debug1, col_debug2 = st.columns(2)
            
            with col_debug1:
                st.write("**Session State Keys:**")
                st.code(', '.join(list(st.session_state.keys())[:10]))
            
            with col_debug2:
                st.write("**Memory Usage:**")
                messages_size = sys.getsizeof(st.session_state.messages)
                st.caption(f"📦 Messages: ~{messages_size / 1024:.1f} KB")
        
        st.markdown("---")
        
        # Copy session info button
        session_info = f"""
Session Information - {datetime.now().isoformat()}
User: {st.session_state.username}
Auth: {'Google OAuth' if 'google_oauth_token' in st.session_state else 'Traditional'}
Messages: {total_messages}
Platform: {platform.system()}
Python: {platform.python_version()}
"""
        
        if st.button("📋 Copy Session Info", use_container_width=True):
            st.success("✅ Session info copied to clipboard!")
            st.code(session_info)

# --- 1. SETUP PAGE CONFIGURATION (Open Source UI) ---
st.set_page_config(page_title="My Gemini App", page_icon="🤖", layout="wide")

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"
if "show_brain_stats" not in st.session_state:
    st.session_state.show_brain_stats = False

# Initialize session tracking
if "session_start_time" not in st.session_state:
    import time
    st.session_state.session_start_time = time.time()
if "total_sessions" not in st.session_state:
    st.session_state.total_sessions = 1
if "user_joined_date" not in st.session_state:
    st.session_state.user_joined_date = datetime.now().strftime('%Y-%m-%d')

# Show login page if not authenticated
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# Show profile page
if st.session_state.current_page == "profile":
    show_profile_page()
    st.stop()

# Show dashboard if on dashboard page
if st.session_state.current_page == "dashboard":
    show_dashboard()
    st.stop()

# Initialize chat history in session state early
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "learning_brain" not in st.session_state:
    st.session_state.learning_brain = LearningBrain()

# --- 2. SIDEBAR CONFIGURATION ---
MODEL_OPTIONS = [
    # Google Gemini
    ("Gemini 3 Flash Preview", "gemini-3-flash-preview", "google"),
    ("Gemini 2.0 Flash Exp", "gemini-2.0-flash-exp", "google"),
    ("Gemini 2.0 Flash Latest", "gemini-2.0-flash-latest", "google"),
    ("Gemini 1.5 Flash", "gemini-1.5-flash", "google"),
    ("Gemini 1.5 Pro", "gemini-1.5-pro", "google"),
    ("Gemini 1.0 Pro Vision", "gemini-1.0-pro-vision-latest", "google"),
    # OpenAI GPT
    ("GPT-4o", "gpt-4o", "openai"),
    ("GPT-4o Mini", "gpt-4o-mini", "openai"),
    ("GPT-4 Turbo", "gpt-4-turbo", "openai"),
    ("o1-Preview", "o1-preview", "openai"),
    ("o1-Mini", "o1-mini", "openai"),
    # Anthropic Claude
    ("Claude 3.5 Sonnet", "claude-3-5-sonnet-20241022", "anthropic"),
    ("Claude 3.5 Haiku", "claude-3-5-haiku-20241022", "anthropic"),
    ("Claude 3 Opus", "claude-3-opus-20240229", "anthropic"),
    # Meta Llama (via Together AI)
    ("Llama 3.3 70B", "meta-llama/Llama-3.3-70B-Instruct-Turbo", "together"),
    ("Llama 3.1 405B", "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", "together"),
    ("Llama 3.1 70B", "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "together"),
    # xAI Grok (via Groq or OpenAI-compatible)
    ("Grok Beta", "grok-beta", "xai"),
    # DeepSeek
    ("DeepSeek Chat", "deepseek-chat", "deepseek"),
    ("DeepSeek Coder", "deepseek-coder", "deepseek"),
]

with st.sidebar:
    # Enhanced header with gradient
    st.markdown("""
        <style>
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1rem;
            color: white;
        }
        .sidebar-header h1 {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 700;
        }
        .nav-button {
            margin: 0.25rem 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 3px solid #667eea;
            margin: 0.5rem 0;
        }
        </style>
        <div class="sidebar-header">
            <h1>⚙️ Control Panel</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Page navigation with icons
    st.markdown("### 📍 Navigation")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.current_page == "dashboard" else "secondary"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    with col_nav2:
        if st.button("💬 Chat", use_container_width=True, type="primary" if st.session_state.current_page == "chat" else "secondary"):
            st.session_state.current_page = "chat"
            st.rerun()
    
    st.divider()
    
    # Enhanced user profile section with expandable details
    st.markdown("### 👤 User Profile")
    
    # Initialize profile preferences if not exist
    if "profile_preferences" not in st.session_state:
        st.session_state.profile_preferences = {
            "theme": "Auto",
            "language": "English",
            "timezone": "UTC",
            "notifications": True
        }
    
    if "user_info" in st.session_state and st.session_state.user_info:
        # Google OAuth user with profile picture
        user_info = st.session_state.user_info
        
        # Profile card with enhanced styling
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        col_pic, col_info = st.columns([1, 3])
        with col_pic:
            if user_info.get('picture'):
                st.image(user_info['picture'], width=60, use_container_width=False)
            else:
                st.markdown('<div style="font-size: 3rem; text-align: center;">👤</div>', unsafe_allow_html=True)
        with col_info:
            st.markdown(f"**{user_info.get('name', st.session_state.username)}**")
            st.caption(f"📧 {user_info.get('email', st.session_state.username)}")
            st.caption(f"🔐 Google OAuth")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Profile details in expander
        with st.expander("⚙️ Profile Settings", expanded=False):
            st.markdown("#### Account Information")
            st.text_input("Display Name", value=user_info.get('name', ''), disabled=True, key="profile_name_display")
            st.text_input("Email", value=user_info.get('email', ''), disabled=True, key="profile_email_display")
            
            st.markdown("#### Preferences")
            theme = st.selectbox("Theme", ["Auto", "Light", "Dark"], index=0, key="profile_theme")
            st.session_state.profile_preferences["theme"] = theme
            
            language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese"], index=0, key="profile_language")
            st.session_state.profile_preferences["language"] = language
            
            notifications = st.checkbox("Enable Notifications", value=True, key="profile_notifications")
            st.session_state.profile_preferences["notifications"] = notifications
            
            st.markdown("#### Account Stats")
            joined_date = st.session_state.get("user_joined_date", datetime.now().strftime('%Y-%m-%d'))
            st.caption(f"📅 Member since: {joined_date}")
            st.caption(f"💬 Total sessions: {st.session_state.get('total_sessions', 1)}")
            
        # Quick actions with enhanced styling
        st.markdown("#### ⚡ Quick Actions")
        col_action1, col_action2 = st.columns(2)
        
        with col_action1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">👤 Profile</div>
                <div style="color: #666; font-size: 0.8rem;">View & manage account</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ Open", use_container_width=True, key="view_profile_btn"):
                st.session_state.show_profile_modal = True
        
        with col_action2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fa709a15 0%, #fee14015 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #fee140; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🚪 Logout</div>
                <div style="color: #666; font-size: 0.8rem;">End session</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ Sign Out", use_container_width=True, type="secondary", key="logout_oauth_btn"):
                logout()
                
    else:
        # Traditional login with enhanced profile
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        
        # Load user data if available
        users = load_user_credentials()
        user_data = users.get(st.session_state.username, {})
        
        col_pic, col_info = st.columns([1, 3])
        with col_pic:
            # Generate avatar from username
            avatar_color = hash(st.session_state.username) % 360
            st.markdown(f'<div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, hsl({avatar_color}, 70%, 60%), hsl({avatar_color + 60}, 70%, 60%)); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: white; font-weight: bold;">{st.session_state.username[0].upper()}</div>', unsafe_allow_html=True)
        with col_info:
            st.markdown(f"**{user_data.get('name', st.session_state.username)}**")
            st.caption(f"📧 {user_data.get('email', 'Not set')}")
            st.caption(f"🔐 Traditional Login")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Profile details in expander
        with st.expander("⚙️ Profile Settings", expanded=False):
            st.markdown("#### Account Information")
            
            # Editable profile for traditional users
            new_name = st.text_input("Display Name", value=user_data.get('name', st.session_state.username), key="edit_name")
            new_email = st.text_input("Email", value=user_data.get('email', ''), key="edit_email")
            
            if st.button("💾 Save Profile Changes", use_container_width=True, key="save_profile_btn"):
                users = load_user_credentials()
                if st.session_state.username in users:
                    users[st.session_state.username]['name'] = new_name
                    users[st.session_state.username]['email'] = new_email
                    if save_user_credentials(users):
                        st.success("✅ Profile updated!")
                        # Update session state
                        st.session_state.user_info = {
                            'name': new_name,
                            'email': new_email,
                            'username': st.session_state.username
                        }
                        st.rerun()
                    else:
                        st.error("❌ Failed to save changes")
            
            st.markdown("#### Change Password")
            current_password = st.text_input("Current Password", type="password", key="current_pwd")
            new_password = st.text_input("New Password", type="password", key="new_pwd")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pwd")
            
            if st.button("🔒 Update Password", use_container_width=True, key="update_pwd_btn"):
                if not all([current_password, new_password, confirm_password]):
                    st.warning("⚠️ Please fill all password fields")
                elif new_password != confirm_password:
                    st.error("❌ New passwords don't match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    # Verify current password
                    users = load_user_credentials()
                    if users.get(st.session_state.username, {}).get('password') == hash_password(current_password):
                        users[st.session_state.username]['password'] = hash_password(new_password)
                        if save_user_credentials(users):
                            st.success("✅ Password updated!")
                        else:
                            st.error("❌ Failed to update password")
                    else:
                        st.error("❌ Current password is incorrect")
            
            st.markdown("#### Preferences")
            theme = st.selectbox("Theme", ["Auto", "Light", "Dark"], index=0, key="profile_theme_traditional")
            st.session_state.profile_preferences["theme"] = theme
            
            language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese"], index=0, key="profile_language_traditional")
            st.session_state.profile_preferences["language"] = language
            
            notifications = st.checkbox("Enable Notifications", value=True, key="profile_notifications_traditional")
            st.session_state.profile_preferences["notifications"] = notifications
            
            st.markdown("#### Account Stats")
            joined_date = st.session_state.get("user_joined_date", datetime.now().strftime('%Y-%m-%d'))
            st.caption(f"📅 Member since: {joined_date}")
            st.caption(f"💬 Total sessions: {st.session_state.get('total_sessions', 1)}")
        
        # Quick actions with enhanced styling
        st.markdown("#### ⚡ Quick Actions")
        col_action1, col_action2 = st.columns(2)
        
        with col_action1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">👤 Profile</div>
                <div style="color: #666; font-size: 0.8rem;">View & manage account</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ Open", use_container_width=True, key="view_profile_trad_btn"):
                st.session_state.show_profile_modal = True
        
        with col_action2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fa709a15 0%, #fee14015 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #fee140; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🚪 Logout</div>
                <div style="color: #666; font-size: 0.8rem;">End session</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ Sign Out", use_container_width=True, type="secondary", key="logout_trad_btn"):
                logout()
    
    st.divider()
    
    # Session stats
    total_messages = len(st.session_state.get('messages', []))
    if total_messages > 0:
        st.markdown("### 📊 Session Stats")
        col_msg, col_chars = st.columns(2)
        with col_msg:
            st.metric("Messages", total_messages)
        with col_chars:
            total_chars = sum(len(msg.get('content', '')) for msg in st.session_state.messages)
            st.metric("Characters", f"{total_chars:,}")
        st.divider()
    
    # Initialize API keys in session state from environment on first run
    if "api_keys_initialized" not in st.session_state:
        st.session_state.google_api_key = os.getenv("GEMINI_API_KEY", "")
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        st.session_state.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        st.session_state.together_api_key = os.getenv("TOGETHER_API_KEY", "")
        st.session_state.xai_api_key = os.getenv("XAI_API_KEY", "")
        st.session_state.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
        st.session_state.api_keys_initialized = True
    
    # Helper function to show key status
    def get_key_status(key_value: str) -> str:
        if not key_value:
            return "❌ Not set"
        return f"✅ Set ({len(key_value)} chars)"
    
    # Count configured keys
    configured_keys = sum([
        bool(st.session_state.google_api_key),
        bool(st.session_state.openai_api_key),
        bool(st.session_state.anthropic_api_key),
        bool(st.session_state.together_api_key),
        bool(st.session_state.xai_api_key),
        bool(st.session_state.deepseek_api_key)
    ])
    
    # API Keys dropdown section
    with st.expander(f"🔑 API Keys ({configured_keys}/6 configured)", expanded=False):
        # Toggle for showing/hiding keys with warning
        show_keys = st.checkbox(
            "👁️ Show API Keys", 
            value=False, 
            help="⚠️ Only enable when needed. Keep your API keys private!"
        )
        
        if show_keys:
            st.warning("⚠️ API keys are now visible. Keep your screen private!")
        
        key_type = "default" if show_keys else "password"
        
        # Google API Key
        google_api_key = st.text_input(
            "Google API Key:",
            type=key_type,
            value=st.session_state.google_api_key,
            help="For Gemini models",
            key="google_key_input"
        )
        st.session_state.google_api_key = google_api_key
        if not show_keys:
            st.caption(get_key_status(google_api_key))
        
        # OpenAI API Key
        openai_api_key = st.text_input(
            "OpenAI API Key:",
            type=key_type,
            value=st.session_state.openai_api_key,
            help="For GPT-4/o1 models",
            key="openai_key_input"
        )
        st.session_state.openai_api_key = openai_api_key
        if not show_keys:
            st.caption(get_key_status(openai_api_key))
        
        # Anthropic API Key
        anthropic_api_key = st.text_input(
            "Anthropic API Key:",
            type=key_type,
            value=st.session_state.anthropic_api_key,
            help="For Claude models",
            key="anthropic_key_input"
        )
        st.session_state.anthropic_api_key = anthropic_api_key
        if not show_keys:
            st.caption(get_key_status(anthropic_api_key))
        
        # Together AI API Key
        together_api_key = st.text_input(
            "Together AI API Key:",
            type=key_type,
            value=st.session_state.together_api_key,
            help="For Llama models",
            key="together_key_input"
        )
        st.session_state.together_api_key = together_api_key
        if not show_keys:
            st.caption(get_key_status(together_api_key))
        
        # xAI API Key
        xai_api_key = st.text_input(
            "xAI API Key:",
            type=key_type,
            value=st.session_state.xai_api_key,
            help="For Grok models",
            key="xai_key_input"
        )
        st.session_state.xai_api_key = xai_api_key
        if not show_keys:
            st.caption(get_key_status(xai_api_key))
        
        # DeepSeek API Key
        deepseek_api_key = st.text_input(
            "DeepSeek API Key:",
            type=key_type,
            value=st.session_state.deepseek_api_key,
            help="For DeepSeek models",
            key="deepseek_key_input"
        )
        st.session_state.deepseek_api_key = deepseek_api_key
        if not show_keys:
            st.caption(get_key_status(deepseek_api_key))
    
    st.divider()
    
    # Model selection with search
    st.markdown("### 🤖 AI Model Selection")
    
    # Filter by provider
    provider_filter = st.selectbox(
        "Filter by Provider",
        ["All", "Google", "OpenAI", "Anthropic", "Together AI", "xAI", "DeepSeek"],
        index=0
    )
    
    # Filter models
    filtered_models = MODEL_OPTIONS
    if provider_filter != "All":
        provider_map = {
            "Google": "google",
            "OpenAI": "openai",
            "Anthropic": "anthropic",
            "Together AI": "together",
            "xAI": "xai",
            "DeepSeek": "deepseek"
        }
        filtered_models = [m for m in MODEL_OPTIONS if m[2] == provider_map.get(provider_filter)]
    
    model_choice_label = st.selectbox(
        "Select Model",
        [label for label, _, _ in filtered_models],
        index=0,
    )
    # Find the selected model's name and provider
    selected_model = next((m for m in MODEL_OPTIONS if m[0] == model_choice_label), None)
    model_name = selected_model[1]
    provider = selected_model[2]
    
    # Show provider badge
    provider_colors = {
        "google": "🔵",
        "openai": "🟢", 
        "anthropic": "🟣",
        "together": "🔴",
        "xai": "⚫",
        "deepseek": "🟠"
    }
    st.caption(f"{provider_colors.get(provider, '⚪')} Provider: **{provider.upper()}**")
    
    st.divider()
    
    # Enhanced AI Behavior & Settings with better organization
    with st.expander("🎛️ AI Behavior & Settings", expanded=True):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 1.5rem;">
            <div style="font-size: 0.95rem; color: #555;">
                <strong>💡 Tip:</strong> Fine-tune how the AI behaves and generates responses. Adjust parameters to match your needs.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # System instructions
        st.markdown("#### 📋 System Instructions")
        st.caption("Define the AI's personality and behavior pattern")
        system_instruction = st.text_area(
            "AI Behavior Definition",
            placeholder="e.g., You are a helpful coding assistant. Be concise and provide practical examples...",
            help="Define how the AI should behave and respond",
            height=100,
            key="system_instruction",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Generation Parameters with better organization
        st.markdown("#### ⚙️ Generation Parameters")
        
        param_col1, param_col2 = st.columns(2)
        
        with param_col1:
            st.markdown("**Creativity & Randomness**")
            temperature = st.slider(
                "🎨 Temperature",
                0.0, 2.0, 1.0, 0.1,
                help="0.0 = Deterministic/Focused | 1.0 = Balanced | 2.0 = Creative/Random",
                label_visibility="collapsed"
            )
            
            st.markdown("Temperature: `" + f"{temperature:.1f}" + "`", help="Current temperature setting")
        
        with param_col2:
            st.markdown("**Diversity Control**")
            top_p = st.slider(
                "🎯 Top P (Nucleus Sampling)",
                0.0, 1.0, 0.95, 0.05,
                help="0.9 = Less diverse | 0.95 = Balanced | 1.0 = Most diverse",
                label_visibility="collapsed"
            )
            st.markdown("Top P: `" + f"{top_p:.2f}" + "`", help="Current top P setting")
        
        st.markdown("---")
        
        # Output constraints
        st.markdown("**Output Constraints**")
        token_col1, token_col2 = st.columns(2)
        
        with token_col1:
            max_output_tokens = st.slider(
                "📝 Max Output Tokens",
                100, 8192, 2048, 100,
                help="Maximum length of AI responses (tokens ≈ words/4)",
                label_visibility="collapsed"
            )
        
        with token_col2:
            st.metric("Max Response Length", f"{max_output_tokens:,} tokens")
        
        st.markdown("---")
        
        # Response streaming
        st.markdown("**Response Delivery**")
        streaming_col1, streaming_col2 = st.columns([3, 1])
        with streaming_col1:
            enable_streaming = st.checkbox(
                "⚡ Enable Streaming",
                value=True,
                help="Stream responses word-by-word as they're generated (faster perceived speed)"
            )
        with streaming_col2:
            status_text = "🟢 Active" if enable_streaming else "🔴 Disabled"
            st.markdown(f"**{status_text}**")
        
        # Settings summary
        st.markdown("---")
        st.markdown("#### 📊 Active Configuration")
        config_col1, config_col2, config_col3, config_col4 = st.columns(4)
        with config_col1:
            st.metric("Temperature", f"{temperature:.1f}", delta="Creativity")
        with config_col2:
            st.metric("Top P", f"{top_p:.2f}", delta="Diversity")
        with config_col3:
            st.metric("Max Tokens", f"{max_output_tokens // 1000:.1f}k", delta="Length")
        with config_col4:
            stream_status = "Stream" if enable_streaming else "Batch"
            st.metric("Mode", stream_status, delta="Delivery")
    
    st.divider()
    
    # Enhanced AI Brain Mode
    with st.expander("🧠 AI Brain Mode (Advanced)", expanded=False):
        enable_brain_mode = st.checkbox(
            "Enable AI Brain",
            value=False,
            help="Combine multiple AI models + internet knowledge for enhanced responses"
        )
        
        if enable_brain_mode:
            st.success("🧠 Brain Mode Active - Multi-model intelligence enabled")
            
            enable_internet = st.checkbox("🌐 Enable Internet Search", value=True, help="Search the web for current information")
            
            st.markdown("#### Select Models to Consult")
            st.caption("Choose which AI models the brain should query")
            
            col_brain1, col_brain2 = st.columns(2)
            with col_brain1:
                brain_use_google = st.checkbox("🔵 Google Gemini", value=bool(google_api_key), disabled=not bool(google_api_key))
                brain_use_openai = st.checkbox("🟢 OpenAI GPT", value=bool(openai_api_key), disabled=not bool(openai_api_key))
            with col_brain2:
                brain_use_anthropic = st.checkbox("🟣 Anthropic Claude", value=bool(anthropic_api_key), disabled=not bool(anthropic_api_key))
                brain_use_together = st.checkbox("🔴 Meta Llama", value=bool(together_api_key), disabled=not bool(together_api_key))
            
            selected_brain_models = sum([brain_use_google, brain_use_openai, brain_use_anthropic, brain_use_together])
            st.info(f"✅ {selected_brain_models} model(s) selected for brain consultation")
        else:
            enable_internet = False
            brain_use_google = brain_use_openai = brain_use_anthropic = brain_use_together = False
    
    st.divider()
    
    # Enhanced Multimodal & Voice sections
    with st.expander("📎 Multimodal & Voice Features", expanded=False):
        st.markdown("#### Multimodal Input")
        multimodal_options = st.multiselect(
            "Enable file types:",
            ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"],
            default=[],
            help="Select file types you want to upload and analyze"
        )
        
        if multimodal_options:
            st.success(f"✅ {len(multimodal_options)} file type(s) enabled")
        
        st.markdown("#### Voice Mode")
        voice_mode = st.toggle("🎤 Enable Voice Input/Output", value=st.session_state.voice_mode, help="Use voice input and hear responses")
        st.session_state.voice_mode = voice_mode
        
        if voice_mode:
            auto_speak = st.checkbox("🔊 Auto-speak responses", value=True, help="Automatically read AI responses aloud")
            st.info("🎤 Voice mode active - Use audio recorder in chat")
        else:
            auto_speak = False
    
    st.divider()

    # Enhanced Brain Dashboard
    with st.expander("🧠 Learning Brain Dashboard", expanded=False):
        learning_brain = st.session_state.learning_brain
        stats = learning_brain.get_learning_stats()
        
        st.markdown("#### Brain Intelligence Metrics")
        # Quick stats metrics with better layout
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("📚 Topics", stats['total_topics'], delta=None, delta_color="normal")
        with metric_col2:
            st.metric("💬 Chats", stats['total_conversations'], delta=None, delta_color="normal")
        with metric_col3:
            st.metric("🤖 Models", stats['models_tracked'], delta=None, delta_color="normal")
        
        # Top performing model
        if stats.get('model_strengths'):
            best_model = stats['model_strengths'][0]
            st.success(f"🏆 Best Model: **{best_model['model']}** ({best_model['success_rate']}% success)")
        
        st.markdown("#### Brain State Management")
        state_path = st.text_input(
            "Save/Load Path",
            value=st.session_state.get("brain_state_path", "learning_brain_state.json"),
            help="File to save/load the learning brain state",
            key="brain_state_path_input"
        )
        st.session_state.brain_state_path = state_path

        bcol1, bcol2, bcol3 = st.columns(3)
        with bcol1:
            if st.button("💾 Save", use_container_width=True, key="save_brain"):
                if learning_brain.save_to_file(state_path):
                    st.success(f"✓ Saved")
                else:
                    st.error("❌ Failed")
        with bcol2:
            if st.button("📂 Load", use_container_width=True, key="load_brain"):
                if learning_brain.load_from_file(state_path):
                    st.success(f"✓ Loaded")
                    st.rerun()
                else:
                    st.warning("⚠️ Not found")
        with bcol3:
            if st.button("♻️ Reset", use_container_width=True, key="reset_brain"):
                learning_brain.reset_learning()
                st.success("✓ Cleared")
                st.rerun()

        st.markdown("#### Import/Export")
        upload_col, download_col = st.columns(2)
        with upload_col:
            uploaded_state = st.file_uploader("Import JSON", type=["json"], help="Load a saved learning brain export", key="upload_brain")
            if uploaded_state:
                try:
                    imported = uploaded_state.read().decode("utf-8")
                    if learning_brain.import_knowledge(imported):
                        st.success("✓ Imported")
                        st.rerun()
                    else:
                        st.error("❌ Failed")
                except Exception as import_exc:
                    st.error(f"❌ Error: {str(import_exc)[:50]}")
        with download_col:
            export_blob = learning_brain.export_knowledge()
            st.download_button(
                "📥 Export",
                export_blob,
                "brain_state.json",
                "application/json",
                use_container_width=True,
                key="download_brain"
            )
    
    # Model Performance Dashboard
    with st.expander("📊 Model Performance", expanded=True):
        strengths = stats.get("model_strengths", [])
        if strengths:
            # Create visual performance bars
            for model_data in strengths:
                model_name_display = model_data['model']
                success_rate = model_data['success_rate']
                total = model_data['total']
                success = model_data['success']
                
                col_name, col_bar, col_stats = st.columns([2, 3, 2])
                with col_name:
                    st.write(f"**{model_name_display}**")
                with col_bar:
                    st.progress(success_rate / 100.0, text=f"{success_rate}% success")
                with col_stats:
                    st.caption(f"{success}/{total} queries")
                
                # Show top topics for this model
                if model_data.get('top_topics'):
                    st.caption(f"🏆 Top topics: {', '.join(model_data['top_topics'][:3])}")
                st.write("")
        else:
            st.info("No model performance data yet. Use Brain Mode to start learning!")
    
    # Topic Expertise Dashboard
    with st.expander("🎯 Topic Expertise", expanded=False):
        top_topics = stats.get("top_topics", [])
        if top_topics:
            st.write("**Most Discussed Topics:**")
            for topic_info in top_topics[:10]:
                topic_name = topic_info['topic']
                count = topic_info['count']
                st.write(f"• **{topic_name}**: {count} conversation{'s' if count != 1 else ''}")
        else:
            st.info("No topics learned yet. Ask questions to build the knowledge base!")
    
    # Recent Learning Activity
    with st.expander("📜 Recent Learning Activity", expanded=False):
        if learning_brain.conversation_history:
            st.write("**Last 5 Learning Sessions:**")
            for record in learning_brain.conversation_history[-5:][::-1]:
                query_preview = record.query[:80] + "..." if len(record.query) > 80 else record.query
                st.caption(f"🔹 {query_preview}")
                st.caption(f"   Models: {', '.join(record.models)} | Success: {record.success_count}/{len(record.models)}")
        else:
            st.info("No learning history yet.")

    st.divider()
    
    # Chat controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("💾 Export", use_container_width=True):
            if st.session_state.get("messages"):
                chat_export = "\n\n".join(
                    [f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages]
                )
                st.download_button(
                    "📥 Download Chat",
                    chat_export,
                    "chat_history.txt",
                    "text/plain",
                    use_container_width=True
                )
    
    st.caption(f"Provider: {provider.upper()} | Model: {model_name}")
    st.caption(f"Messages: {len(st.session_state.get('messages', []))}")

# --- 3. MAIN CHAT INTERFACE ---
st.title("🤖 Multi-Provider AI Chat")
if st.session_state.voice_mode:
    st.caption("GPT-4, Claude, Gemini, Llama, Grok, DeepSeek | 🎤 Voice Mode Active")
else:
    st.caption("GPT-4, Claude, Gemini, Llama, Grok, DeepSeek")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Display images if present
        if "images" in message and message["images"]:
            cols = st.columns(min(len(message["images"]), 3))
            for idx, img_data in enumerate(message["images"]):
                with cols[idx % 3]:
                    st.image(img_data, use_container_width=True)
        
        # Display file info if present
        if "files" in message and message["files"]:
            for file_info in message["files"]:
                st.caption(f"📎 {file_info['name']} ({file_info['type']})")
        
        st.markdown(message["content"])

# --- 4. HANDLE USER INPUT ---
prompt = None
uploaded_images = []
uploaded_file_info = []
extra_context = ""

# Multimodal file upload
if multimodal_options:
    st.info(f"📎 Multimodal Mode: {', '.join(multimodal_options)} enabled")
    
    # Determine allowed file types
    allowed_types = []
    if "Images" in multimodal_options:
        allowed_types.extend(["jpg", "jpeg", "png", "gif", "webp"])
    if "Documents (PDF/TXT)" in multimodal_options:
        allowed_types.extend(["pdf", "txt", "md"])
    if "Audio Files" in multimodal_options:
        allowed_types.extend(["mp3", "wav", "m4a", "ogg"])
    if "Video Frames" in multimodal_options:
        allowed_types.extend(["mp4", "avi", "mov", "mkv"])
    
    uploaded_files = st.file_uploader(
        "Upload files for analysis",
        type=allowed_types,
        accept_multiple_files=True,
        help="Upload one or more files to analyze"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            file_ext = file.name.split('.')[-1].lower()
            
            # Handle images
            if file_ext in ["jpg", "jpeg", "png", "gif", "webp"]:
                img = Image.open(file)
                uploaded_images.append(img)
                st.image(img, caption=file.name, width=200)
                uploaded_file_info.append({"name": file.name, "type": "Image"})
            
            # Handle PDFs
            elif file_ext == "pdf":
                try:
                    import PyPDF2  # type: ignore
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    extra_context += f"\n\n--- Content from {file.name} ---\n{text[:2000]}..." if len(text) > 2000 else f"\n\n--- Content from {file.name} ---\n{text}"
                    st.success(f"✅ Extracted {len(pdf_reader.pages)} pages from {file.name}")
                    uploaded_file_info.append({"name": file.name, "type": "PDF Document"})
                except ImportError:
                    st.warning("⚠️ PDF support requires PyPDF2: pip install PyPDF2")
                except Exception as e:
                    st.error(f"❌ Failed to read PDF: {e}")
            
            # Handle text files
            elif file_ext in ["txt", "md"]:
                text = file.read().decode('utf-8')
                extra_context += f"\n\n--- Content from {file.name} ---\n{text}"
                st.success(f"✅ Loaded {file.name}")
                uploaded_file_info.append({"name": file.name, "type": "Text Document"})
            
            # Handle audio files
            elif file_ext in ["mp3", "wav", "m4a", "ogg"]:
                try:
                    import speech_recognition as sr  # type: ignore
                    
                    # Save to temp file for processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name
                    
                    recognizer = sr.Recognizer()
                    
                    # Convert to WAV if needed and transcribe
                    if file_ext != 'wav':
                        st.info(f"🎵 Processing audio file {file.name}...")
                    
                    with sr.AudioFile(tmp_path) as source:
                        audio = recognizer.record(source)
                        transcription = recognizer.recognize_google(audio)
                        extra_context += f"\n\n--- Transcription from {file.name} ---\n{transcription}"
                        st.success(f"✅ Transcribed {file.name}")
                        uploaded_file_info.append({"name": file.name, "type": "Audio"})
                    
                    os.unlink(tmp_path)
                except ImportError:
                    st.warning("⚠️ Audio transcription requires SpeechRecognition: pip install SpeechRecognition")
                except Exception as e:
                    st.error(f"❌ Audio processing failed: {e}")
            
            # Handle video files (extract frames)
            elif file_ext in ["mp4", "avi", "mov", "mkv"]:
                try:
                    from moviepy.editor import VideoFileClip  # type: ignore
                    
                    # Save to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name
                    
                    with st.spinner(f"🎬 Extracting frames from {file.name}..."):
                        clip = VideoFileClip(tmp_path)
                        duration = clip.duration
                        
                        # Extract frames at intervals
                        num_frames = min(5, int(duration))  # Max 5 frames
                        for i in range(num_frames):
                            t = (i * duration) / num_frames
                            frame = clip.get_frame(t)
                            img = Image.fromarray(frame)
                            uploaded_images.append(img)
                            st.image(img, caption=f"{file.name} @ {t:.1f}s", width=150)
                        
                        clip.close()
                        st.success(f"✅ Extracted {num_frames} frames from {file.name}")
                        uploaded_file_info.append({"name": file.name, "type": "Video"})
                    
                    os.unlink(tmp_path)
                except ImportError:
                    st.warning("⚠️ Video support requires moviepy: pip install moviepy")
                except Exception as e:
                    st.error(f"❌ Video processing failed: {e}")

# Image upload mode
if st.session_state.voice_mode:
    st.info("🎤 Voice Mode: Record your message using the audio recorder below")
    audio_bytes = st.audio_input("Record your message")
    
    if audio_bytes:
        with st.spinner("🎧 Transcribing audio..."):
            try:
                # Use speech recognition
                import speech_recognition as sr  # type: ignore
                
                recognizer = sr.Recognizer()
                # Convert audio bytes to AudioFile
                audio_file = sr.AudioFile(BytesIO(audio_bytes.read()))
                
                with audio_file as source:
                    audio_data = recognizer.record(source)
                
                # Use Google Speech Recognition (free)
                prompt = recognizer.recognize_google(audio_data)
                st.success(f"✅ Transcribed: {prompt}")
                
            except ImportError:
                st.error("❌ Voice mode requires 'SpeechRecognition' library. Install with: pip install SpeechRecognition")
                st.stop()
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio. Please try again.")
                st.stop()
            except sr.RequestError as e:
                st.error(f"❌ Speech recognition service error: {e}")
                st.stop()
            except Exception as e:
                st.error(f"❌ Audio transcription failed: {e}")
                st.stop()
else:
    # Text input mode
    prompt = st.chat_input("Ask me anything...")

if prompt:
    # AI Brain Mode - Multi-model + Internet
    if enable_brain_mode:
        from brain import AIBrain
        import asyncio
        
        # Use persistent learning brain
        learning_brain: LearningBrain = st.session_state.learning_brain
        
        # Helper brain for internet + multi-call execution
        brain = AIBrain()
        brain.internet_enabled = enable_internet
        
        # Gather internet context if enabled
        internet_context = ""
        if enable_internet:
            with st.spinner("🌐 Searching the internet..."):
                internet_context = brain.gather_internet_context(prompt)
        
        # Prepare models to query
        models_to_query = []
        config = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "top_p": top_p
        }
        
        if brain_use_google and google_api_key:
            models_to_query.append({
                "provider": "google",
                "model": "gemini-3-flash-preview",
                "api_key": google_api_key
            })
        
        if brain_use_openai and openai_api_key:
            models_to_query.append({
                "provider": "openai",
                "model": "gpt-4o-mini",
                "api_key": openai_api_key
            })
        
        if brain_use_anthropic and anthropic_api_key:
            models_to_query.append({
                "provider": "anthropic",
                "model": "claude-3-5-haiku-20241022",
                "api_key": anthropic_api_key
            })
        
        if brain_use_together and together_api_key:
            models_to_query.append({
                "provider": "together",
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
                "api_key": together_api_key
            })
        
        if not models_to_query:
            st.error("⚠️ Please select at least one AI model and provide its API key in Brain Mode.")
            st.stop()

        # Reorder models based on learned recommendations
        recommended_order = learning_brain.recommend_models(
            prompt,
            [m["provider"] for m in models_to_query]
        )
        if recommended_order:
            models_to_query.sort(
                key=lambda m: recommended_order.index(m["provider"]) if m["provider"] in recommended_order else len(recommended_order)
            )
        
        # Add prompt with internet context
        enhanced_prompt = prompt
        if internet_context:
            enhanced_prompt = f"{prompt}\n\n{internet_context}"
        
        # Query all selected models
        with st.spinner(f"🧠 Consulting {len(models_to_query)} AI models..."):
            model_responses = asyncio.run(brain.query_multiple_models(
                enhanced_prompt,
                models_to_query,
                config
            ))

        # Learn from the results
        learning_brain.learn_from_responses(prompt, model_responses)
        
        # Synthesize responses
        synthesized_response = brain.synthesize_responses(
            prompt,
            model_responses,
            internet_context
        )

        # Learning report (short)
        with st.expander("🧠 Learning report", expanded=False):
            st.markdown(learning_brain.format_learning_report())
        
        # Store in memory
        brain.add_to_memory(prompt, synthesized_response)
        
        # Display user message
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display synthesized response
        with st.chat_message("assistant"):
            st.markdown(synthesized_response)
        
        st.session_state.messages.append({"role": "assistant", "content": synthesized_response})
        st.rerun()
    
    # Standard Single Model Mode
    else:
        # Validate API key based on provider
        api_key_map = {
            "google": google_api_key,
            "openai": openai_api_key,
            "anthropic": anthropic_api_key,
            "together": together_api_key,
            "xai": xai_api_key,
            "deepseek": deepseek_api_key,
        }
        
        resolved_api_key = api_key_map.get(provider)
        if not resolved_api_key:
            st.info(f"⚠️ Please add your {provider.upper()} API key in the sidebar to use {model_choice_label}.")
            st.stop()

        # Add user message to chat and display
        final_prompt = prompt
        if extra_context:
            final_prompt = f"{prompt}\n\nAdditional context from uploaded files:{extra_context}"
        
        user_message = {"role": "user", "content": final_prompt}
        if uploaded_images:
            user_message["images"] = uploaded_images
        if uploaded_file_info:
            user_message["files"] = uploaded_file_info
        st.session_state.messages.append(user_message)
    
        
        with st.chat_message("user"):
            if uploaded_images:
                cols = st.columns(min(len(uploaded_images), 3))
                for idx, img in enumerate(uploaded_images):
                    with cols[idx % 3]:
                        st.image(img, use_container_width=True)
            if uploaded_file_info:
                for file_info in uploaded_file_info:
                    st.caption(f"📎 {file_info['name']} ({file_info['type']})")
            st.markdown(prompt)

        # Generate and display assistant response
        response_text = None
        with st.chat_message("assistant"):
            try:
                # Route to the appropriate provider
                if provider == "google":
                    # Google Gemini (using new SDK)
                    client = genai.Client(api_key=resolved_api_key)
                    
                    # Build config
                    config = {
                        "temperature": temperature,
                        "max_output_tokens": max_output_tokens,
                        "top_p": top_p,
                    }
                    
                    # Add system instruction if provided
                    if system_instruction:
                        config["system_instruction"] = system_instruction
                    
                    # Prepare content
                    if uploaded_images:
                        # For multimodal input, use parts format
                        contents = []
                        for img in uploaded_images:
                            # Convert PIL Image to bytes
                            img_byte_arr = BytesIO()
                            img.save(img_byte_arr, format='PNG')
                            img_byte_arr = img_byte_arr.getvalue()
                            contents.append({"inline_data": {"mime_type": "image/png", "data": base64.b64encode(img_byte_arr).decode()}})
                        contents.append(final_prompt)
                    else:
                        contents = final_prompt
                    
                    # Generate content (streaming not supported in new SDK via stream parameter)
                    response = client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=config,
                    )
                    response_text = response.text
                    st.markdown(response_text)
                        
                elif provider == "openai":
                    # OpenAI GPT
                    client = get_openai_client(resolved_api_key)
                    conversation_history = build_conversation_history(st.session_state.messages)
                    messages = create_openai_messages(conversation_history, final_prompt, system_instruction)
                    response_text = handle_openai_compatible_provider(
                        client, model_name, messages, temperature, max_output_tokens, top_p, enable_streaming
                    )
                        
                elif provider == "anthropic":
                    # Anthropic Claude
                    from anthropic import Anthropic
                    client = Anthropic(api_key=resolved_api_key)
                    
                    messages = []
                    # Add conversation history
                    for msg in st.session_state.messages[:-1]:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    # Add current message
                    messages.append({"role": "user", "content": final_prompt})
                    
                    if enable_streaming:
                        with client.messages.stream(
                            model=model_name,
                            messages=messages,
                            max_tokens=max_output_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            system=system_instruction if system_instruction else None,
                        ) as stream:
                            response_text = st.write_stream(stream.text_stream)
                    else:
                        response = client.messages.create(
                            model=model_name,
                            messages=messages,
                            max_tokens=max_output_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            system=system_instruction if system_instruction else None,
                        )
                        response_text = response.content[0].text
                        st.markdown(response_text)
                        
                elif provider == "together":
                    # Together AI (for Llama)
                    client = get_openai_client(resolved_api_key, base_url="https://api.together.xyz/v1")
                    conversation_history = build_conversation_history(st.session_state.messages)
                    messages = create_openai_messages(conversation_history, final_prompt, system_instruction)
                    response_text = handle_openai_compatible_provider(
                        client, model_name, messages, temperature, max_output_tokens, top_p, enable_streaming
                    )
                        
                elif provider == "xai":
                    # xAI Grok (uses OpenAI-compatible API)
                    client = get_openai_client(resolved_api_key, base_url="https://api.x.ai/v1")
                    conversation_history = build_conversation_history(st.session_state.messages)
                    messages = create_openai_messages(conversation_history, final_prompt, system_instruction)
                    response_text = handle_openai_compatible_provider(
                        client, model_name, messages, temperature, max_output_tokens, top_p, enable_streaming
                    )
                        
                elif provider == "deepseek":
                    # DeepSeek (uses OpenAI-compatible API)
                    client = get_openai_client(resolved_api_key, base_url="https://api.deepseek.com")
                    conversation_history = build_conversation_history(st.session_state.messages)
                    messages = create_openai_messages(conversation_history, final_prompt, system_instruction)
                    response_text = handle_openai_compatible_provider(
                        client, model_name, messages, temperature, max_output_tokens, top_p, enable_streaming
                    )
                        
            except Exception as exc:
                error_msg = str(exc)
                if "404" in error_msg:
                    st.error(f"❌ Model not available: {model_name}. Try a different model from the sidebar.")
                elif "DNS" in error_msg or "timeout" in error_msg.lower():
                    st.error("❌ Network error. Check your internet connection or VPN settings.")
                elif "API key" in error_msg or "authentication" in error_msg.lower():
                    st.error(f"❌ Invalid API key for {provider}. Please check your API key in the sidebar.")
                else:
                    st.error(f"❌ Request failed: {error_msg}")
        
        # Save assistant response to history
        if response_text:
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            # Text-to-speech in voice mode
            if st.session_state.voice_mode and auto_speak and response_text:
                try:
                    from gtts import gTTS  # type: ignore
                    
                    # Generate speech
                    tts = gTTS(text=response_text, lang='en', slow=False)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    
                    # Auto-play audio using HTML5 audio with autoplay
                    audio_base64 = base64.b64encode(audio_buffer.read()).decode()
                    audio_html = f"""
                    <audio autoplay>
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                    st.caption("🔊 Playing response...")
                    
                except ImportError:
                    st.warning("⚠️ Auto-speak requires 'gTTS' library. Install with: pip install gTTS")
                except Exception as e:
                    st.warning(f"⚠️ Text-to-speech failed: {e}")
                    