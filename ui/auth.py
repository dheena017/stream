
import streamlit as st
import os
import hashlib
import json
import logging
from typing import Dict, Optional, Any
from google.oauth2 import id_token
from google.auth.transport import requests

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
    logging.info("User credentials updated.")
    try:
        with open("users.json", 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception:
        return False

def check_login(username_or_email: str, password: str) -> Optional[Dict[str, str]]:
    """Verify login credentials - accepts username or email"""
    logging.info(f"Login attempt for: {username_or_email}")
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
    # Dark mode preference
    dark_mode = st.session_state.get('dark_mode', False)

    # CSS for light and dark modes
    if dark_mode:
        st.markdown(
            """
            <style>
            :root {
                --bg: #0b1220;
                --card: #0f1724;
                --muted: #9ca3af;
                --text: #e6eef8;
                --accent-1: #7c3aed;
                --accent-2: #2563eb;
            }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(-20px);} to { opacity: 1; transform: translateY(0);} }
            @keyframes slideIn { from { opacity: 0; transform: translateX(-30px);} to { opacity: 1; transform: translateX(0);} }
            .stApp { background: var(--bg) !important; color: var(--text) !important; }
            .login-header { text-align: center; animation: fadeIn 0.8s ease-out; margin-bottom: 2rem; }
            .login-header h1 { background: linear-gradient(135deg, var(--accent-2), var(--accent-1)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; }
            .login-subtitle { color: var(--muted); font-size: 1.2rem; margin-bottom: 1rem; }
            .feature-card { background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(37,99,235,0.03)); border-radius: 10px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid var(--accent-1); animation: slideIn 0.6s ease-out; color: var(--text); }
            .google-btn { background: linear-gradient(135deg, #1f6feb, #1646b2); color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; display: inline-block; width: 100%; text-align: center; font-weight: 600; margin-top: 10px; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(0,0,0,0.6); }
            .google-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 26px rgba(0,0,0,0.7); }
            .info-card { background: var(--card); padding: 10px; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.6); }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            :root {
                --bg: #f8fafc;
                --card: #ffffff;
                --muted: #666666;
                --text: #0f1724;
                --accent-1: #667eea;
                --accent-2: #357ae8;
            }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(-20px);} to { opacity: 1; transform: translateY(0);} }
            @keyframes slideIn { from { opacity: 0; transform: translateX(-30px);} to { opacity: 1; transform: translateX(0);} }
            .login-header { text-align: center; animation: fadeIn 0.8s ease-out; margin-bottom: 2rem; }
            .login-header h1 { background: linear-gradient(135deg, var(--accent-1), #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; }
            .login-subtitle { color: var(--muted); font-size: 1.2rem; margin-bottom: 1rem; }
            .feature-card { background: linear-gradient(135deg, rgba(102,126,234,0.09), rgba(118,75,162,0.06)); border-radius: 10px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid var(--accent-1); animation: slideIn 0.6s ease-out; }
            .google-btn { background: linear-gradient(135deg, #4285f4 0%, #357ae8 100%); color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; display: inline-block; width: 100%; text-align: center; font-weight: 600; margin-top: 10px; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3); }
            .google-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4); }
            .info-card { background: var(--card); padding: 10px; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
    # Hero section with dark-mode toggle
    col1, col2, col3 = st.columns([1, 3, 1])

    # Right column: dark mode toggle and small status
    with col3:
        # Persist preference when toggled via on_change callback
        from ui.prefs import save_dark_mode_from_session
        dm = st.checkbox("🌙 Dark Mode", value=dark_mode, key="dark_mode", on_change=save_dark_mode_from_session, kwargs={"username": st.session_state.get('username')})

    with col2:
        st.markdown('<div class="login-header"><h1>🚀 Antigravity AI</h1><div class="login-subtitle">Your intelligent multi-model AI companion</div></div>', unsafe_allow_html=True)
        
        # Feature highlights
        st.markdown(
            '<div class="feature-card" style="box-shadow:0 2px 12px rgba(0,0,0,0.07); border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.5rem; background: #fff;">✨ <strong>25+ AI Models</strong> from Google, OpenAI, Anthropic, Meta & more</div>'
            '<div class="feature-card" style="box-shadow:0 2px 12px rgba(0,0,0,0.07); border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.5rem; background: #fff;">🧠 <strong>AI Brain Mode</strong> - Combines multiple models for enhanced responses</div>'
            '<div class="feature-card" style="box-shadow:0 2px 12px rgba(0,0,0,0.07); border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.5rem; background: #fff;">🌐 <strong>Internet Search</strong> - Real-time information from the web</div>'
            '<div class="feature-card" style="box-shadow:0 2px 12px rgba(0,0,0,0.07); border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.5rem; background: #fff;">📎 <strong>Multimodal</strong> - Images, PDFs, Audio & Video support</div>',
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
                help="Paste the token from Google OAuth redirect here if not auto-filled."
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
                placeholder="Enter email or username",
                help="Enter your registered email address or username."
            )
            password = st.text_input(
                "Password", 
                type="password", 
                key="login_password", 
                placeholder="Enter password",
                help="Enter your account password."
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
                        st.warning("⚠️ Please enter both email/username and password.")
            
            with col_info:
                with st.popover("ℹ️ Info"):
                    st.markdown("<div style='box-shadow:0 2px 12px rgba(0,0,0,0.07); border-radius:12px; padding:1rem 1.2rem; background:#f9fafb;'>", unsafe_allow_html=True)
                    st.markdown("**Default Credentials:**")
                    st.code("Email: admin@example.com\nUsername: admin\nPassword: admin123")
                    st.markdown("---")
                    st.markdown("**Login with email or username**")
                    st.caption("You can use either your email address or username to login")
                    if google_client_id:
                        st.markdown("---")
                        st.markdown("**Google OAuth Setup:**")
                        st.caption("Set GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI in environment variables")
                    st.markdown("</div>", unsafe_allow_html=True)
        
        with tab_register:
            st.markdown("#### Create New Account")
            reg_name = st.text_input("Full Name", key="reg_name", placeholder="Enter your full name", help="Enter your real name for your profile.")
            reg_email = st.text_input("Email Address", key="reg_email", placeholder="Enter your email", help="Enter a valid email address for account recovery.")
            reg_username = st.text_input("Username", key="reg_username", placeholder="Choose a username", help="Pick a unique username for login.")
            reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Choose a password", help="Password must be at least 6 characters.")
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm", placeholder="Confirm password", help="Re-enter your password to confirm.")
            
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
