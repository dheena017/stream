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
from multimodal_voice_integration import MultimodalVoiceIntegrator
import pandas as pd

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

# --- COST TRACKING ---

# Pricing per 1M tokens (input, output) - Updated Jan 2026 estimates
MODEL_PRICING = {
    # Google Gemini
    "gemini-3-flash-preview": (0.075, 0.30),
    "gemini-2.0-flash-exp": (0.075, 0.30),
    "gemini-2.0-flash-latest": (0.075, 0.30),
    "gemini-1.5-flash": (0.075, 0.30),
    "gemini-1.5-pro": (1.25, 5.00),
    "gemini-1.0-pro-vision-latest": (0.50, 1.50),
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4-turbo": (10.00, 30.00),
    "o1-preview": (15.00, 60.00),
    "o1-mini": (3.00, 12.00),
    # Anthropic Claude
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.25, 1.25),
    "claude-3-opus-20240229": (15.00, 75.00),
    # Together AI (Llama)
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": (0.88, 0.88),
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": (3.50, 3.50),
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": (0.88, 0.88),
    # xAI Grok
    "grok-beta": (5.00, 15.00),
    # DeepSeek
    "deepseek-chat": (0.14, 0.28),
    "deepseek-coder": (0.14, 0.28),
}

def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English"""
    return len(text) // 4

def calculate_cost(model: str, input_text: str, output_text: str) -> float:
    """Calculate estimated cost for a request"""
    pricing = MODEL_PRICING.get(model, (1.0, 1.0))  # Default fallback
    input_tokens = estimate_tokens(input_text)
    output_tokens = estimate_tokens(output_text)
    
    input_cost = (input_tokens / 1_000_000) * pricing[0]
    output_cost = (output_tokens / 1_000_000) * pricing[1]
    
    return input_cost + output_cost

def get_session_cost() -> Dict[str, Any]:
    """Calculate total session cost from messages"""
    total_cost = 0.0
    cost_by_provider = {}
    
    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages):
        if msg["role"] == "assistant":
            model = msg.get("model", "unknown")
            provider = msg.get("provider", "unknown")
            
            # Get previous user message for input estimation
            input_text = messages[i-1]["content"] if i > 0 else ""
            output_text = msg["content"]
            
            cost = calculate_cost(model, input_text, output_text)
            total_cost += cost
            
            if provider not in cost_by_provider:
                cost_by_provider[provider] = 0.0
            cost_by_provider[provider] += cost
    
    return {
        "total": total_cost,
        "by_provider": cost_by_provider,
        "message_count": len([m for m in messages if m["role"] == "assistant"])
    }

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

@st.cache_resource
def get_google_client(api_key: str):
    """Cached Google Gemini client initialization"""
    return genai.Client(api_key=api_key)

@st.cache_data(ttl=3600)
def get_model_pricing():
    """Cached model pricing data"""
    return MODEL_PRICING.copy()

@st.cache_data(ttl=60)
def get_cached_learning_stats(_learning_brain):
    """Cached learning stats - refreshes every minute"""
    return _learning_brain.get_learning_stats()

@st.cache_data(ttl=300)
def get_cached_model_strengths(_learning_brain):
    """Cached model strengths summary"""
    return _learning_brain.summarize_model_strengths()

def build_conversation_history(messages: List[Dict], exclude_last: bool = True, max_messages: int = 20, max_chars: int = 50000) -> List[Dict]:
    """Build conversation history from messages with smart summarization for long chats.
    
    Args:
        messages: List of message dictionaries
        exclude_last: Whether to exclude the last message
        max_messages: Maximum number of recent messages to include in full
        max_chars: Maximum total characters before summarizing older messages
    """
    history = messages[:-1] if exclude_last and len(messages) > 0 else messages
    
    if not history:
        return []
    
    # Convert to simple format
    formatted = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    
    # Check if summarization is needed
    total_chars = sum(len(m["content"]) for m in formatted)
    
    if len(formatted) > max_messages or total_chars > max_chars:
        # Split into older and recent messages
        older = formatted[:-max_messages] if len(formatted) > max_messages else []
        recent = formatted[-max_messages:]
        
        if older:
            # Create a summary of older messages
            older_summary_parts = []
            for msg in older[-10:]:  # Summarize last 10 of older messages
                content_preview = msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"]
                older_summary_parts.append(f"{msg['role'].upper()}: {content_preview}")
            
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
            
            # Return summary + recent messages
            return [{"role": "system", "content": summary_text}] + recent
        else:
            return recent
    
    return formatted

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
    
    # Additional quick action shortcuts (enhanced)
    st.markdown("---")
    st.markdown("### ⚡ Additional Actions")

    # Custom CSS for action cards
    st.markdown("""
    <style>
    .action-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        border: 1px solid #667eea30;
        transition: transform 0.2s;
    }
    .action-card:hover { transform: translateY(-2px); }
    .action-icon { font-size: 1.5rem; }
    .action-label { font-size: 0.85rem; color: #555; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

    # Row 1: Primary actions
    st.markdown("#### Primary")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

    with quick_col1:
        if st.button("🔄 Clear Chat", use_container_width=True, key="clear_chat_quick"):
            st.session_state.messages = []
            st.success("✅ Chat cleared!")
            st.rerun()
        st.caption("Reset conversation")

    with quick_col2:
        if st.button("🧠 Reset Brain", use_container_width=True, key="reset_brain_quick"):
            learning_brain = st.session_state.learning_brain
            learning_brain.reset_learning()
            st.success("✅ Brain reset!")
            st.rerun()
        st.caption("Clear learning data")

    with quick_col3:
        if st.button("💾 Save Brain", use_container_width=True, key="save_brain_quick"):
            learning_brain = st.session_state.learning_brain
            path = st.session_state.get("brain_state_path", "learning_brain_state.json")
            if learning_brain.save_to_file(path):
                st.success("✅ Brain saved!")
            else:
                st.error("❌ Save failed")
        st.caption("Persist to disk")

    with quick_col4:
        if st.button("📂 Load Brain", use_container_width=True, key="load_brain_quick"):
            learning_brain = st.session_state.learning_brain
            path = st.session_state.get("brain_state_path", "learning_brain_state.json")
            if learning_brain.load_from_file(path):
                st.success("✅ Brain loaded!")
                st.rerun()
            else:
                st.warning("⚠️ File not found")
        st.caption("Restore from disk")

    # Row 2: Secondary actions
    st.markdown("#### Secondary")
    sec_col1, sec_col2, sec_col3, sec_col4 = st.columns(4)

    with sec_col1:
        if st.button("📊 Refresh Stats", use_container_width=True, key="refresh_stats_quick"):
            st.rerun()
        st.caption("Update UI")

    with sec_col2:
        if st.button("📥 Export Chat", use_container_width=True, key="export_chat_quick"):
            messages = st.session_state.get("messages", [])
            if messages:
                chat_blob = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
                st.download_button("Download", chat_blob, "chat_export.txt", "text/plain", key="dl_chat_quick")
            else:
                st.info("No messages to export")
        st.caption("Save conversation")

    with sec_col3:
        if st.button("📄 Download Report", use_container_width=True, key="dl_report_quick"):
            learning_brain = st.session_state.learning_brain
            report = learning_brain.format_learning_report()
            st.download_button("Download", report, "learning_report.md", "text/markdown", key="dl_rpt_quick2")
        st.caption("Brain insights")

    with sec_col4:
        if st.button("🔗 Copy Session ID", use_container_width=True, key="copy_session_quick"):
            session_id = st.session_state.get("session_id", "N/A")
            st.code(session_id)
        st.caption("For debugging")

    # Row 3: Toggles & info
    st.markdown("#### Toggles")
    tog_col1, tog_col2, tog_col3, tog_col4 = st.columns(4)

    with tog_col1:
        show_brain_stats = st.checkbox("📈 Show Brain Stats", value=st.session_state.get('show_brain_stats', False), key="toggle_brain_stats")
        st.session_state.show_brain_stats = show_brain_stats

    with tog_col2:
        dark_mode = st.checkbox("🌙 Dark Hints", value=st.session_state.get('dark_hints', False), key="toggle_dark_hints")
        st.session_state.dark_hints = dark_mode

    with tog_col3:
        auto_save = st.checkbox("💾 Auto-save Brain", value=st.session_state.get('auto_save_brain', False), key="toggle_auto_save")
        st.session_state.auto_save_brain = auto_save

    with tog_col4:
        compact_ui = st.checkbox("📐 Compact UI", value=st.session_state.get('compact_ui', False), key="toggle_compact_ui")
        st.session_state.compact_ui = compact_ui
    
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

# Initialize theme state early
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Apply theme CSS
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    /* Dark mode theme - comprehensive text styling */
    .stApp { background-color: #1a1a2e; color: #eaeaea; }
    .stSidebar { background-color: #16213e !important; }
    .stSidebar [data-testid="stSidebarContent"] { background-color: #16213e; }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar p, .stSidebar span, .stSidebar label { color: #eaeaea !important; }
    .stChatMessage { background-color: #1f2940 !important; border-color: #2d3a4f !important; }
    .stChatMessage p, .stChatMessage span, .stChatMessage div { color: #eaeaea !important; }
    .stTextInput > div > div > input { background-color: #1f2940; color: #eaeaea !important; border-color: #3d4f6f; }
    .stTextInput label { color: #eaeaea !important; }
    .stTextArea textarea { background-color: #1f2940 !important; color: #eaeaea !important; border-color: #3d4f6f !important; }
    .stTextArea label { color: #eaeaea !important; }
    .stSelectbox > div > div { background-color: #1f2940; color: #eaeaea !important; }
    .stSelectbox label { color: #eaeaea !important; }
    .stSelectbox [data-baseweb="select"] { background-color: #1f2940; }
    .stSelectbox [data-baseweb="select"] span { color: #eaeaea !important; }
    .stMultiSelect label { color: #eaeaea !important; }
    .stSlider label { color: #eaeaea !important; }
    .stSlider p { color: #eaeaea !important; }
    .stCheckbox label { color: #eaeaea !important; }
    .stCheckbox span { color: #eaeaea !important; }
    .stRadio label { color: #eaeaea !important; }
    .stExpander { background-color: #1f2940; border-color: #3d4f6f; }
    .stExpander summary { color: #eaeaea !important; }
    .stExpander p, .stExpander span, .stExpander div { color: #eaeaea !important; }
    div[data-testid="stExpander"] details summary span { color: #eaeaea !important; }
    .stMarkdown, .stText { color: #eaeaea !important; }
    .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 { color: #eaeaea !important; }
    .stMarkdown a { color: #7c9eff !important; }
    .stMarkdown code { background-color: #2d3a4f !important; color: #a8d4ff !important; }
    .stMarkdown pre { background-color: #2d3a4f !important; }
    .stMarkdown pre code { color: #a8d4ff !important; }
    p, span, label, div { color: #eaeaea; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    .stButton > button { background-color: #3d4f6f; color: white !important; border: none; }
    .stButton > button:hover { background-color: #4a5f8f; }
    .stMetric { background-color: #1f2940; border-radius: 8px; padding: 10px; }
    .stMetric label { color: #aaaaaa !important; }
    .stMetric [data-testid="stMetricValue"] { color: #ffffff !important; }
    .stMetric [data-testid="stMetricDelta"] { color: #88cc88 !important; }
    .stDataFrame { background-color: #1f2940; }
    .stDataFrame th { color: #eaeaea !important; background-color: #2d3a4f !important; }
    .stDataFrame td { color: #eaeaea !important; }
    .stProgress > div > div { background-color: #667eea; }
    .stCaption { color: #aaaaaa !important; }
    small { color: #aaaaaa !important; }
    .stAlert { color: #eaeaea !important; }
    .stInfo { background-color: #1e3a5f !important; color: #eaeaea !important; }
    .stSuccess { background-color: #1e3a2e !important; color: #88cc88 !important; }
    .stWarning { background-color: #3a3a1e !important; color: #cccc88 !important; }
    .stError { background-color: #3a1e1e !important; color: #cc8888 !important; }
    .chat-bubble-assistant { background: linear-gradient(135deg, #1f2940 0%, #2d3a4f 100%) !important; color: #eaeaea !important; border-color: #3d4f6f !important; }
    div[data-testid="stExpander"] { background-color: #1f2940; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1f2940; }
    .stTabs [data-baseweb="tab"] { color: #eaeaea !important; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; }
    [data-testid="stHeader"] { background-color: #1a1a2e !important; }
    .stCodeBlock { background-color: #2d3a4f !important; }
    .stCodeBlock code { color: #a8d4ff !important; }
    /* Table styling */
    table { background-color: #1f2940 !important; }
    table th { color: #eaeaea !important; background-color: #2d3a4f !important; }
    table td { color: #eaeaea !important; }
    /* Chat input */
    [data-testid="stChatInput"] { background-color: #1f2940 !important; }
    [data-testid="stChatInput"] textarea { background-color: #1f2940 !important; color: #eaeaea !important; }
    /* File uploader */
    .stFileUploader label { color: #eaeaea !important; }
    .stFileUploader section { background-color: #1f2940 !important; border-color: #3d4f6f !important; }
    .stFileUploader section div { color: #eaeaea !important; }
    /* Download button */
    .stDownloadButton button { background-color: #3d4f6f !important; color: white !important; }
    /* Tooltip */
    [data-testid="stTooltipIcon"] { color: #aaaaaa !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    /* Light mode theme - ensure dark text for readability */
    .stApp { background-color: #f8f9fa; color: #1a1a1a; }
    .stSidebar { background-color: #ffffff !important; }
    .stSidebar [data-testid="stSidebarContent"] { background-color: #ffffff; }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar p, .stSidebar span, .stSidebar label { color: #1a1a1a !important; }
    .stChatMessage { border-radius: 12px; background-color: #ffffff !important; }
    .stChatMessage p, .stChatMessage span, .stChatMessage div { color: #1a1a1a !important; }
    .stTextInput > div > div > input { background-color: #ffffff; color: #1a1a1a !important; border-color: #d0d0d0; }
    .stTextInput label { color: #1a1a1a !important; }
    .stTextArea textarea { background-color: #ffffff !important; color: #1a1a1a !important; border-color: #d0d0d0 !important; }
    .stTextArea label { color: #1a1a1a !important; }
    .stSelectbox > div > div { background-color: #ffffff; color: #1a1a1a !important; }
    .stSelectbox label { color: #1a1a1a !important; }
    .stSelectbox [data-baseweb="select"] { background-color: #ffffff; }
    .stSelectbox [data-baseweb="select"] span { color: #1a1a1a !important; }
    .stMultiSelect label { color: #1a1a1a !important; }
    .stSlider label { color: #1a1a1a !important; }
    .stSlider p { color: #1a1a1a !important; }
    .stCheckbox label { color: #1a1a1a !important; }
    .stCheckbox span { color: #1a1a1a !important; }
    .stRadio label { color: #1a1a1a !important; }
    .stExpander { background-color: #ffffff; border-color: #e0e0e0; }
    .stExpander summary { color: #1a1a1a !important; }
    .stExpander p, .stExpander span, .stExpander div { color: #1a1a1a !important; }
    div[data-testid="stExpander"] details summary span { color: #1a1a1a !important; }
    .stMarkdown, .stText { color: #1a1a1a !important; }
    .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 { color: #1a1a1a !important; }
    .stMarkdown a { color: #667eea !important; }
    .stMarkdown code { background-color: #f0f0f0 !important; color: #333333 !important; }
    .stMarkdown pre { background-color: #f0f0f0 !important; }
    .stMarkdown pre code { color: #333333 !important; }
    p, span, label, div { color: #1a1a1a; }
    h1, h2, h3, h4, h5, h6 { color: #1a1a1a !important; }
    .stButton > button { background-color: #667eea; color: white !important; border: none; }
    .stButton > button:hover { background-color: #5a6fd6; }
    .stMetric { background-color: #ffffff; border-radius: 8px; padding: 10px; }
    .stMetric label { color: #666666 !important; }
    .stMetric [data-testid="stMetricValue"] { color: #1a1a1a !important; }
    .stMetric [data-testid="stMetricDelta"] { color: #28a745 !important; }
    .stDataFrame { background-color: #ffffff; }
    .stDataFrame th { color: #1a1a1a !important; background-color: #f0f0f0 !important; }
    .stDataFrame td { color: #1a1a1a !important; }
    .stProgress > div > div { background-color: #667eea; }
    .stCaption { color: #666666 !important; }
    small { color: #666666 !important; }
    .stAlert { color: #1a1a1a !important; }
    .chat-bubble-assistant { background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%) !important; color: #1a1a1a !important; border-color: #e0e0e0 !important; }
    div[data-testid="stExpander"] { background-color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { background-color: #ffffff; }
    .stTabs [data-baseweb="tab"] { color: #1a1a1a !important; }
    .stTabs [aria-selected="true"] { color: #667eea !important; }
    [data-testid="stHeader"] { background-color: #f8f9fa !important; }
    .stCodeBlock { background-color: #f0f0f0 !important; }
    .stCodeBlock code { color: #333333 !important; }
    /* Table styling */
    table { background-color: #ffffff !important; }
    table th { color: #1a1a1a !important; background-color: #f0f0f0 !important; }
    table td { color: #1a1a1a !important; }
    /* Chat input */
    [data-testid="stChatInput"] { background-color: #ffffff !important; }
    [data-testid="stChatInput"] textarea { background-color: #ffffff !important; color: #1a1a1a !important; }
    /* File uploader */
    .stFileUploader label { color: #1a1a1a !important; }
    .stFileUploader section { background-color: #ffffff !important; border-color: #d0d0d0 !important; }
    .stFileUploader section div { color: #1a1a1a !important; }
    /* Download button */
    .stDownloadButton button { background-color: #667eea !important; color: white !important; }
    /* Tooltip */
    [data-testid="stTooltipIcon"] { color: #666666 !important; }
    </style>
    """, unsafe_allow_html=True)

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

# Initialize chat history and session state early (BEFORE dashboard)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False
if "multimodal_options" not in st.session_state:
    st.session_state.multimodal_options = []
if "auto_speak" not in st.session_state:
    st.session_state.auto_speak = True

# Show dashboard if on dashboard page
if st.session_state.current_page == "dashboard":
    show_dashboard()
    st.stop()
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
    
    # Theme toggle (Dark/Light mode)
    theme_col1, theme_col2 = st.columns([1, 1])
    with theme_col1:
        st.markdown("**🎨 Theme**")
    with theme_col2:
        dark_mode = st.toggle("🌙", value=st.session_state.dark_mode, key="dark_mode_toggle", help="Toggle dark mode")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
    
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
    
    # Model selection with search (enhanced)
    st.markdown("### 🤖 AI Model Selection")

    # Provider icons & colors
    provider_icons = {
        "google": "🔵", "openai": "🟢", "anthropic": "🟣",
        "together": "🔴", "xai": "⚫", "deepseek": "🟠"
    }
    provider_labels = {
        "google": "Google Gemini", "openai": "OpenAI GPT", "anthropic": "Anthropic Claude",
        "together": "Meta Llama", "xai": "xAI Grok", "deepseek": "DeepSeek"
    }

    # Model capability tags (static metadata)
    model_capabilities = {
        "gemini-3-flash-preview": ["⚡ Fast", "🖼️ Vision", "🆕 Preview"],
        "gemini-2.0-flash-exp": ["⚡ Fast", "🖼️ Vision", "🧪 Experimental"],
        "gemini-2.0-flash-latest": ["⚡ Fast", "🖼️ Vision"],
        "gemini-1.5-flash": ["⚡ Fast", "📄 Long Context"],
        "gemini-1.5-pro": ["🧠 Smart", "📄 Long Context"],
        "gemini-1.0-pro-vision-latest": ["🖼️ Vision"],
        "gpt-4o": ["🧠 Smart", "🖼️ Vision", "⚡ Fast"],
        "gpt-4o-mini": ["⚡ Fast", "💰 Cheap"],
        "gpt-4-turbo": ["🧠 Smart", "🖼️ Vision"],
        "o1-preview": ["🧠 Reasoning", "🆕 Preview"],
        "o1-mini": ["🧠 Reasoning", "⚡ Fast"],
        "claude-3-5-sonnet-20241022": ["🧠 Smart", "📝 Writing"],
        "claude-3-5-haiku-20241022": ["⚡ Fast", "💰 Cheap"],
        "claude-3-opus-20240229": ["🧠 Flagship", "📝 Writing"],
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": ["🦙 Open", "⚡ Fast"],
        "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": ["🦙 Open", "🧠 Flagship"],
        "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": ["🦙 Open"],
        "grok-beta": ["🆕 Beta", "💬 Chat"],
        "deepseek-chat": ["💬 Chat", "💰 Cheap"],
        "deepseek-coder": ["💻 Code", "💰 Cheap"],
    }

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

    # Build display labels with provider icon
    display_labels = [f"{provider_icons.get(m[2], '⚪')} {m[0]}" for m in filtered_models]
    model_choice_idx = st.selectbox(
        "Select Model",
        range(len(filtered_models)),
        format_func=lambda i: display_labels[i],
        index=0,
    )
    selected_model = filtered_models[model_choice_idx]
    model_choice_label = selected_model[0]
    model_name = selected_model[1]
    provider = selected_model[2]

    # Model info card
    caps = model_capabilities.get(model_name, [])
    caps_str = " ".join(caps) if caps else "—"
    st.markdown(
        f'<div style="background:linear-gradient(90deg,#667eea15,#764ba210);'
        f'border-left:4px solid #667eea;padding:12px;border-radius:8px;margin:8px 0;">'
        f'<b>{provider_icons.get(provider, "⚪")} {model_choice_label}</b><br/>'
        f'<span style="font-size:0.85rem;color:#555;">Provider: {provider_labels.get(provider, provider.upper())}</span><br/>'
        f'<span style="font-size:0.8rem;">{caps_str}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Brain recommendation (if learning data exists)
    learning_brain = st.session_state.get("learning_brain")
    if learning_brain and learning_brain.model_performance:
        available = [m[2] for m in MODEL_OPTIONS]
        recommended = learning_brain.recommend_models("", available)[:3]
        if recommended:
            rec_chips = " ".join([f"`{provider_icons.get(r, '⚪')} {r}`" for r in recommended])
            st.caption(f"🧠 Brain recommends: {rec_chips}")

    # Quick model comparison (top 3 by success rate from brain)
    if learning_brain and learning_brain.model_performance:
        with st.expander("📊 Quick Model Comparison", expanded=False):
            strengths = learning_brain.summarize_model_strengths()[:5]
            if strengths:
                cmp_df = pd.DataFrame(strengths)[['model', 'success_rate', 'total']]
                cmp_df = cmp_df.rename(columns={'model': 'Model', 'success_rate': 'Success %', 'total': 'Queries'})
                st.dataframe(cmp_df, use_container_width=True)
            else:
                st.info("No performance data yet.")
    
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
            
            # Auto-select mode
            auto_select_model = st.checkbox(
                "🤖 Auto-Select Best Model",
                value=True,
                help="Let the brain automatically choose the best model based on query type and past performance"
            )
            
            if auto_select_model:
                st.caption("Brain will analyze your query and pick the optimal model(s)")
                
                # Query type detection hints
                st.markdown("**Query Type Detection:**")
                type_hints = {
                    "💻 Code": ["code", "function", "debug", "error", "programming", "python", "javascript"],
                    "📝 Writing": ["write", "essay", "article", "email", "summarize", "translate"],
                    "🔬 Analysis": ["analyze", "compare", "explain", "why", "how does"],
                    "💡 Creative": ["brainstorm", "ideas", "creative", "story", "imagine"],
                    "📊 Data": ["data", "chart", "statistics", "calculate", "math"],
                }
                hint_cols = st.columns(5)
                for i, (hint_type, _) in enumerate(type_hints.items()):
                    with hint_cols[i]:
                        st.caption(hint_type)
            
            st.markdown("---")
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
            
            # Store auto-select preference
            st.session_state.brain_auto_select = auto_select_model
        else:
            enable_internet = False
            brain_use_google = brain_use_openai = brain_use_anthropic = brain_use_together = False
            st.session_state.brain_auto_select = False
    
    st.divider()
    
    # Enhanced Multimodal & Voice sections (wired to advanced modules)
    with st.expander("📎 Multimodal & Voice Features", expanded=False):
        if "multimodal_voice_integrator" not in st.session_state:
            st.session_state.multimodal_voice_integrator = MultimodalVoiceIntegrator()

        integrator: MultimodalVoiceIntegrator = st.session_state.multimodal_voice_integrator

        st.markdown("#### 📎 Multimodal Control Center")
        upload_results = integrator.create_multimodal_uploader()

        st.markdown("#### 🎤 Voice Control Center")
        voice_preferences = integrator.create_voice_settings()
        integrator.create_text_to_speech_interface(voice_preferences)
        integrator.create_speech_to_text_interface(voice_preferences)

        st.markdown("#### 📊 Processing Statistics")
        integrator.display_multimodal_statistics()

        st.markdown("#### 🔊 Voice Mode Toggle (app-wide)")
        st.session_state.voice_mode = st.toggle(
            "Enable voice input/output",
            value=st.session_state.voice_mode,
            help="Controls app-level voice behaviors like auto-speaking responses where supported."
        )

        st.session_state.auto_speak = st.checkbox(
            "Auto-speak responses",
            value=st.session_state.get("auto_speak", True),
            help="When enabled, responses will be read aloud in sections that support audio playback."
        )
    
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
        # --- Added: Visualizations, model table, feedback, topic viewer, report download
        st.markdown("#### Visualizations & Insights")
        vis_col1, vis_col2 = st.columns([2, 3])
        with vis_col1:
            # Overall success metric (average of model strengths)
            model_strengths = stats.get('model_strengths', [])
            overall_success = 0.0
            if model_strengths:
                overall_success = sum([m.get('success_rate', 0.0) for m in model_strengths]) / len(model_strengths)
            st.metric("Overall Success", f"{overall_success:.1f}%")

            # Conversation trend
            if learning_brain.conversation_history:
                dates = [r.timestamp.split('T')[0] for r in learning_brain.conversation_history]
                counts = pd.Series(dates).value_counts().sort_index()
                counts.index = pd.to_datetime(counts.index)
                st.line_chart(counts)
            else:
                st.caption("No conversation history to chart yet.")

        with vis_col2:
            top_topics = stats.get('top_topics', [])
            if top_topics:
                df_topics = pd.DataFrame(top_topics).set_index('topic')
                st.bar_chart(df_topics['count'])
                st.table(df_topics.reset_index().rename(columns={'topic': 'Topic', 'count': 'Count'}))
            else:
                st.info("No top topics yet")

        # Model performance table + quick feedback
        st.markdown("#### Model Performance Table & Feedback")
        if stats.get('model_performance'):
            df_perf = pd.DataFrame.from_dict(stats['model_performance'], orient='index')
            df_perf = df_perf.rename_axis('model').reset_index()
            st.dataframe(df_perf)
            model_list = df_perf['model'].tolist()
            sel_model = st.selectbox("Select model to give feedback", model_list, key="select_feedback_model")
            fb_col1, fb_col2 = st.columns(2)
            with fb_col1:
                if st.button("👍 Mark Success", key="fb_success"):
                    learning_brain.register_feedback(sel_model, True)
                    st.success("Feedback recorded — marked success")
            with fb_col2:
                if st.button("👎 Mark Failure", key="fb_fail"):
                    learning_brain.register_feedback(sel_model, False)
                    st.warning("Feedback recorded — marked failure")
        else:
            st.info("No model performance data yet. Use Brain Mode to start learning!")

        # Topic viewer and export
        st.markdown("#### Topic Browser")
        topics = list(learning_brain.knowledge_base.keys())
        if topics:
            sel_topic = st.selectbox("Browse topic", topics, key="select_topic")
            entries = learning_brain.knowledge_base.get(sel_topic, [])
            if entries:
                for e in entries[-5:][::-1]:
                    st.caption(f"{e.timestamp} • {e.query}")
                    for ans in e.answers:
                        st.write(ans)
                    st.caption(f"Models: {', '.join(e.models_used)}")
                    st.divider()
                # Export selected topic
                topic_blob = json.dumps([{ 'query': e.query, 'answers': e.answers, 'timestamp': e.timestamp, 'models_used': e.models_used } for e in entries], indent=2)
                st.download_button("Export topic JSON", topic_blob, f"{sel_topic}_kb.json", "application/json", key="download_topic")
            else:
                st.info("No entries for this topic yet.")
        else:
            st.info("No topics learned yet.")

        # Download formatted learning report
        report_md = learning_brain.format_learning_report()
        st.download_button("📄 Download Learning Report", report_md, "learning_report.md", "text/markdown", key="download_report")
    
    # Model Performance Dashboard (enhanced)
    with st.expander("📊 Model Performance", expanded=True):
        strengths = stats.get("model_strengths", [])
        model_perf = stats.get("model_performance", {})
        provider_icons = {
            "google": "🔵", "openai": "🟢", "anthropic": "🟣",
            "together": "🔴", "xai": "⚫", "deepseek": "🟠"
        }
        if strengths:
            # Summary metrics row
            total_queries = sum(m.get("total", 0) for m in strengths)
            total_success = sum(m.get("success", 0) for m in strengths)
            avg_success = (total_success / total_queries * 100) if total_queries else 0
            sum_col1, sum_col2, sum_col3 = st.columns(3)
            with sum_col1:
                st.metric("Total Queries", total_queries)
            with sum_col2:
                st.metric("Total Successes", total_success)
            with sum_col3:
                st.metric("Avg Success Rate", f"{avg_success:.1f}%")
            st.markdown("---")

            # Detailed cards per model
            for rank, model_data in enumerate(strengths, start=1):
                model_name_display = model_data['model']
                success_rate = model_data['success_rate']
                total = model_data['total']
                success = model_data['success']
                perf_info = model_perf.get(model_name_display, {})
                avg_len = perf_info.get('avg_response_length', 0)

                # Rank badge & color tier
                if rank == 1:
                    badge = "🥇"
                elif rank == 2:
                    badge = "🥈"
                elif rank == 3:
                    badge = "🥉"
                else:
                    badge = f"#{rank}"

                if success_rate >= 80:
                    tier_color = "#28a745"
                elif success_rate >= 50:
                    tier_color = "#ffc107"
                else:
                    tier_color = "#dc3545"

                icon = provider_icons.get(model_name_display.lower(), "🤖")

                st.markdown(
                    f'<div style="background:linear-gradient(90deg,{tier_color}22,{tier_color}08);'
                    f'border-left:4px solid {tier_color};padding:10px;border-radius:6px;margin-bottom:8px;">'
                    f'<span style="font-size:1.3rem;">{badge} {icon} <b>{model_name_display}</b></span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                col_bar, col_stats, col_len = st.columns([4, 2, 2])
                with col_bar:
                    st.progress(success_rate / 100.0, text=f"{success_rate}% success")
                with col_stats:
                    st.caption(f"✔ {success}/{total} queries")
                with col_len:
                    st.caption(f"📏 ~{int(avg_len)} chars")

                # Top topics
                if model_data.get('top_topics'):
                    st.caption(f"🏆 Top topics: {', '.join(model_data['top_topics'][:5])}")

            # Comparison table
            st.markdown("#### Comparison Table")
            df_cmp = pd.DataFrame(strengths)
            df_cmp = df_cmp[['model', 'success_rate', 'success', 'total']]
            df_cmp = df_cmp.rename(columns={'model': 'Model', 'success_rate': 'Success %', 'success': 'Successes', 'total': 'Queries'})
            st.dataframe(df_cmp, use_container_width=True)

            # Success rate bar chart
            st.markdown("#### Success Rate by Model")
            chart_df = pd.DataFrame(strengths).set_index('model')[['success_rate']]
            st.bar_chart(chart_df)
        else:
            st.info("No model performance data yet. Use Brain Mode to start learning!")
    
    # Topic Expertise Dashboard (enhanced)
    with st.expander("🎯 Topic Expertise", expanded=False):
        top_topics = stats.get("top_topics", [])
        topic_expertise = learning_brain.topic_expertise  # {topic: {model: count}}

        if top_topics:
            # Summary metrics
            total_topics = len(top_topics)
            total_entries = sum(t['count'] for t in top_topics)
            top_topic_name = top_topics[0]['topic'] if top_topics else "—"
            te_col1, te_col2, te_col3 = st.columns(3)
            with te_col1:
                st.metric("Total Topics", total_topics)
            with te_col2:
                st.metric("Total Entries", total_entries)
            with te_col3:
                st.metric("Top Topic", top_topic_name)

            st.markdown("---")

            # Horizontal bar chart of top 10 topics
            st.markdown("#### Top Topics by Conversations")
            df_topics = pd.DataFrame(top_topics[:10])
            if not df_topics.empty:
                df_topics = df_topics.set_index('topic')
                st.bar_chart(df_topics['count'])

            # Detailed topic cards with model breakdown
            st.markdown("#### Topic Details")
            for idx, topic_info in enumerate(top_topics[:10], start=1):
                topic_name = topic_info['topic']
                count = topic_info['count']

                # Badge for rank
                if idx == 1:
                    badge = "🥇"
                elif idx == 2:
                    badge = "🥈"
                elif idx == 3:
                    badge = "🥉"
                else:
                    badge = f"#{idx}"

                st.markdown(
                    f'<div style="background:linear-gradient(90deg,#667eea22,#764ba208);'
                    f'border-left:4px solid #667eea;padding:10px;border-radius:6px;margin-bottom:8px;">'
                    f'<span style="font-size:1.1rem;">{badge} <b>{topic_name}</b></span>'
                    f' &nbsp;—&nbsp; {count} conversation{"s" if count != 1 else ""}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Model breakdown for this topic
                models_for_topic = topic_expertise.get(topic_name, {})
                if models_for_topic:
                    sorted_models = sorted(models_for_topic.items(), key=lambda x: x[1], reverse=True)
                    chips = " ".join([f"`{m}` ({c})" for m, c in sorted_models[:5]])
                    st.caption(f"Models: {chips}")

            # Search / filter topics
            st.markdown("#### Search Topics")
            search_q = st.text_input("Filter topics", "", key="topic_search")
            if search_q:
                filtered = [t for t in top_topics if search_q.lower() in t['topic'].lower()]
                if filtered:
                    for t in filtered[:20]:
                        st.write(f"• **{t['topic']}**: {t['count']}")
                else:
                    st.info("No matching topics found.")
        else:
            st.info("No topics learned yet. Ask questions to build the knowledge base!")
    
    # Recent Learning Activity (enhanced)
    with st.expander("📜 Recent Learning Activity", expanded=False):
        history = learning_brain.conversation_history
        if history:
            # Summary metrics
            total_sessions = len(history)
            total_success = sum(r.success_count for r in history)
            total_models_used = sum(len(r.models) for r in history)
            avg_success_rate = (total_success / total_models_used * 100) if total_models_used else 0

            la_col1, la_col2, la_col3 = st.columns(3)
            with la_col1:
                st.metric("Total Sessions", total_sessions)
            with la_col2:
                st.metric("Total Successes", total_success)
            with la_col3:
                st.metric("Avg Success", f"{avg_success_rate:.1f}%")

            st.markdown("---")

            # Activity trend chart (sessions per day)
            st.markdown("#### Activity Trend")
            dates = [r.timestamp.split('T')[0] for r in history]
            counts = pd.Series(dates).value_counts().sort_index()
            counts.index = pd.to_datetime(counts.index)
            st.line_chart(counts)

            # Configurable number of recent sessions
            st.markdown("#### Recent Sessions")
            num_sessions = st.slider("Show last N sessions", 3, min(30, total_sessions), 10, key="la_slider")
            recent = history[-num_sessions:][::-1]

            for idx, record in enumerate(recent, start=1):
                query_preview = record.query[:100] + "..." if len(record.query) > 100 else record.query
                success_pct = (record.success_count / len(record.models) * 100) if record.models else 0

                # Color tier
                if success_pct >= 80:
                    tier_color = "#28a745"
                elif success_pct >= 50:
                    tier_color = "#ffc107"
                else:
                    tier_color = "#dc3545"

                st.markdown(
                    f'<div style="background:linear-gradient(90deg,{tier_color}22,{tier_color}08);'
                    f'border-left:4px solid {tier_color};padding:10px;border-radius:6px;margin-bottom:8px;">'
                    f'<b>#{idx}</b> &nbsp; {query_preview}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                detail_cols = st.columns([3, 2, 2])
                with detail_cols[0]:
                    st.caption(f"🕒 {record.timestamp}")
                with detail_cols[1]:
                    st.caption(f"🤖 {', '.join(record.models)}")
                with detail_cols[2]:
                    st.caption(f"✔ {record.success_count}/{len(record.models)} ({success_pct:.0f}%)")

            # Export history as JSON
            st.markdown("---")
            history_blob = json.dumps(
                [{'query': r.query, 'timestamp': r.timestamp, 'models': r.models, 'success_count': r.success_count} for r in history],
                indent=2
            )
            st.download_button("📥 Export History JSON", history_blob, "learning_history.json", "application/json", key="download_history")
        else:
            st.info("No learning history yet.")

    st.divider()
    
    # Cost tracking display
    with st.expander("💰 Cost Tracking", expanded=False):
        session_cost = get_session_cost()
        
        cost_col1, cost_col2 = st.columns(2)
        with cost_col1:
            st.metric("Session Cost", f"${session_cost['total']:.6f}")
        with cost_col2:
            st.metric("API Calls", session_cost['message_count'])
        
        if session_cost['by_provider']:
            st.markdown("**Cost by Provider:**")
            for provider_name, cost in session_cost['by_provider'].items():
                st.caption(f"• {provider_name}: ${cost:.6f}")
        
        st.markdown("---")
        st.markdown("**Pricing Reference (per 1M tokens):**")
        pricing_df = pd.DataFrame([
            {"Model": k, "Input": f"${v[0]:.2f}", "Output": f"${v[1]:.2f}"}
            for k, v in list(MODEL_PRICING.items())[:8]
        ])
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)
    
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

# Keyboard shortcuts
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    // Ctrl+K or Cmd+K: Focus chat input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const chatInput = document.querySelector('textarea[data-testid="stChatInput"]');
        if (chatInput) chatInput.focus();
    }
    // Ctrl+Shift+C: Clear chat (trigger button click)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
        e.preventDefault();
        const clearBtn = document.querySelector('button[kind="secondary"]');
        if (clearBtn && clearBtn.innerText.includes('Clear')) clearBtn.click();
    }
    // Escape: Blur current input
    if (e.key === 'Escape') {
        document.activeElement.blur();
    }
});
</script>
<style>
/* Keyboard shortcut hints */
.shortcut-hint {
    font-size: 0.7rem;
    color: #888;
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 4px;
    margin-left: 4px;
}
</style>
""", unsafe_allow_html=True)

# Show keyboard shortcut hints
with st.expander("⌨️ Keyboard Shortcuts", expanded=False):
    st.markdown("""
    | Shortcut | Action |
    |----------|--------|
    | `Ctrl/Cmd + K` | Focus chat input |
    | `Ctrl/Cmd + Shift + C` | Clear chat |
    | `Escape` | Blur input |
    | `Enter` | Send message (in chat input) |
    """)

# Chat interface styling
st.markdown("""
<style>
.chat-bubble-user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    max-width: 85%;
    margin-left: auto;
}
.chat-bubble-assistant {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    color: #333;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    max-width: 85%;
    border: 1px solid #e0e0e0;
}
.chat-meta {
    font-size: 0.75rem;
    color: #888;
    margin-top: 4px;
}
.copy-btn {
    background: transparent;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.75rem;
    cursor: pointer;
    margin-left: 8px;
}
.copy-btn:hover { background: #f0f0f0; }
.favorite-star { cursor: pointer; font-size: 1rem; }
.response-time { font-size: 0.7rem; color: #888; margin-left: 8px; }
</style>
""", unsafe_allow_html=True)

# Conversation search
search_col1, search_col2 = st.columns([4, 1])
with search_col1:
    chat_search = st.text_input("🔍 Search conversation", "", key="chat_search", label_visibility="collapsed", placeholder="Search messages...")
with search_col2:
    clear_search = st.button("Clear", key="clear_search", use_container_width=True)
    if clear_search:
        st.session_state.chat_search = ""
        st.rerun()

# Filter messages based on search
messages_to_display = st.session_state.messages
if chat_search:
    messages_to_display = [m for m in st.session_state.messages if chat_search.lower() in m.get("content", "").lower()]
    st.caption(f"Found {len(messages_to_display)} message(s) matching '{chat_search}'")

# Display previous messages with enhanced UI
for idx, message in enumerate(messages_to_display):
    with st.chat_message(message["role"]):
        # Display images if present
        if "images" in message and message["images"]:
            cols = st.columns(min(len(message["images"]), 3))
            for img_idx, img_data in enumerate(message["images"]):
                with cols[img_idx % 3]:
                    st.image(img_data, use_container_width=True)
        
        # Display file info if present
        if "files" in message and message["files"]:
            for file_info in message["files"]:
                st.caption(f"📎 {file_info['name']} ({file_info['type']})")
        
        # Message content
        st.markdown(message["content"])
        
        # Message metadata row
        meta_col1, meta_col2, meta_col3 = st.columns([2, 1, 1])
        with meta_col1:
            # Timestamp
            timestamp = message.get("timestamp", "")
            if timestamp:
                st.caption(f"🕒 {timestamp}")
            # Response time for assistant messages
            if message["role"] == "assistant" and message.get("response_time"):
                st.caption(f"⚡ {message['response_time']:.2f}s")
        
        with meta_col2:
            # Copy button
            if st.button("📋 Copy", key=f"copy_{idx}", use_container_width=True):
                st.code(message["content"], language=None)
                st.success("Copied to clipboard area above!")
        
        with meta_col3:
            # Favorite/bookmark toggle
            fav_key = f"fav_{idx}"
            is_fav = st.session_state.get(fav_key, message.get("favorite", False))
            if st.button("⭐" if is_fav else "☆", key=f"fav_btn_{idx}", use_container_width=True):
                st.session_state[fav_key] = not is_fav
                if idx < len(st.session_state.messages):
                    st.session_state.messages[idx]["favorite"] = not is_fav
                st.rerun()

# --- 4. HANDLE USER INPUT ---
prompt = None
uploaded_images = []
uploaded_file_info = []
extra_context = ""

# Multimodal file upload
multimodal_options = st.session_state.get('multimodal_options', [])
if multimodal_options:
    with st.container():
        st.markdown(
            f'<div style="padding: 10px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); '
            f'border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;">'
            f'📎 <strong>Multimodal Mode Active</strong> • {', '.join(multimodal_options)}</div>',
            unsafe_allow_html=True
        )
    
    # Determine allowed file types
    allowed_types = []
    if "Images" in multimodal_options:
        allowed_types.extend(["jpg", "jpeg", "png", "gif", "webp", "bmp"])
    if "Documents (PDF/TXT)" in multimodal_options:
        allowed_types.extend(["pdf", "txt", "md", "docx"])
    if "Audio Files" in multimodal_options:
        allowed_types.extend(["mp3", "wav", "m4a", "ogg", "flac"])
    if "Video Frames" in multimodal_options:
        allowed_types.extend(["mp4", "avi", "mov", "mkv", "webm"])
    
    uploaded_files = st.file_uploader(
        "🎯 Drag & drop files here or click to browse",
        type=allowed_types,
        accept_multiple_files=True,
        help=f"Supported: {', '.join(allowed_types[:10])}{'...' if len(allowed_types) > 10 else ''}"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            file_ext = file.name.split('.')[-1].lower()
            
            # Handle images
            if file_ext in ["jpg", "jpeg", "png", "gif", "webp", "bmp"]:
                img = Image.open(file)
                
                # Auto-resize if enabled
                if st.session_state.get('image_resize', True):
                    max_size = (1024, 1024)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                uploaded_images.append(img)
                
                # Enhanced preview with metadata
                img_col1, img_col2 = st.columns([1, 3])
                with img_col1:
                    st.image(img, caption=file.name, width=150)
                with img_col2:
                    st.success(f"✅ **{file.name}**")
                    st.caption(f"📐 Size: {img.size[0]}×{img.size[1]}px • Format: {img.format}")
                
                uploaded_file_info.append({"name": file.name, "type": "Image"})
            
            # Handle PDFs
            elif file_ext == "pdf":
                try:
                    import PyPDF2  # type: ignore
                    pdf_reader = PyPDF2.PdfReader(file)
                    page_limit = st.session_state.get('pdf_page_limit', 10)
                    text = ""
                    pages_to_read = min(len(pdf_reader.pages), page_limit)
                    
                    with st.spinner(f"📄 Extracting text from {file.name}..."):
                        for i, page in enumerate(pdf_reader.pages[:pages_to_read]):
                            text += page.extract_text() + "\n"
                    
                    extra_context += f"\n\n--- Content from {file.name} (pages 1-{pages_to_read}) ---\n{text[:3000]}..." if len(text) > 3000 else f"\n\n--- Content from {file.name} ---\n{text}"
                    
                    st.success(f"✅ **{file.name}** • Extracted {pages_to_read}/{len(pdf_reader.pages)} pages")
                    with st.expander("📄 Preview extracted text"):
                        st.text(text[:500] + "..." if len(text) > 500 else text)
                    
                    uploaded_file_info.append({"name": file.name, "type": "PDF Document"})
                except ImportError:
                    st.warning("⚠️ PDF support requires PyPDF2: `pip install PyPDF2`")
                except Exception as e:
                    st.error(f"❌ Failed to read PDF: {e}")
            
            # Handle text files
            elif file_ext in ["txt", "md"]:
                text = file.read().decode('utf-8')
                extra_context += f"\n\n--- Content from {file.name} ---\n{text}"
                st.success(f"✅ Loaded {file.name}")
                uploaded_file_info.append({"name": file.name, "type": "Text Document"})
            
            # Handle audio files
            elif file_ext in ["mp3", "wav", "m4a", "ogg", "flac"]:
                try:
                    import speech_recognition as sr  # type: ignore
                    
                    # Save to temp file for processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name
                    
                    recognizer = sr.Recognizer()
                    
                    with st.spinner(f"🎵 Transcribing {file.name}..."):
                        with sr.AudioFile(tmp_path) as source:
                            # Adjust for ambient noise
                            recognizer.adjust_for_ambient_noise(source, duration=0.5)
                            audio = recognizer.record(source)
                            transcription = recognizer.recognize_google(audio)
                            extra_context += f"\n\n--- Transcription from {file.name} ---\n{transcription}"
                            
                            st.success(f"✅ **{file.name}** transcribed successfully")
                            with st.expander("🎧 View transcription"):
                                st.write(transcription)
                            
                            uploaded_file_info.append({"name": file.name, "type": "Audio"})
                    
                    os.unlink(tmp_path)
                except ImportError:
                    st.warning("⚠️ Audio transcription requires SpeechRecognition: `pip install SpeechRecognition`")
                except Exception as e:
                    st.error(f"❌ Audio processing failed: {e}")
            
            # Handle video files (extract frames)
            elif file_ext in ["mp4", "avi", "mov", "mkv", "webm"]:
                try:
                    from moviepy.editor import VideoFileClip  # type: ignore
                    
                    # Save to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name
                    
                    with st.spinner(f"🎬 Processing video {file.name}..."):
                        clip = VideoFileClip(tmp_path)
                        duration = clip.duration
                        fps = clip.fps
                        
                        # Extract frames at intervals
                        num_frames = st.session_state.get('frame_count', 5)
                        num_frames = min(num_frames, int(duration))
                        
                        st.info(f"🎬 **{file.name}** • Duration: {duration:.1f}s • FPS: {fps:.0f}")
                        
                        frame_cols = st.columns(min(num_frames, 5))
                        for i in range(num_frames):
                            t = (i * duration) / num_frames if num_frames > 1 else 0
                            frame = clip.get_frame(t)
                            img = Image.fromarray(frame)
                            uploaded_images.append(img)
                            
                            with frame_cols[i % 5]:
                                st.image(img, caption=f"@{t:.1f}s", use_container_width=True)
                        
                        clip.close()
                        st.success(f"✅ Extracted {num_frames} frame{'s' if num_frames != 1 else ''} from {file.name}")
                        uploaded_file_info.append({"name": file.name, "type": "Video"})
                    
                    os.unlink(tmp_path)
                except ImportError:
                    st.warning("⚠️ Video support requires moviepy: `pip install moviepy`")
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
    # Text input mode with prompt templates
    
    # Prompt templates library
    PROMPT_TEMPLATES = {
        "None": "",
        "💻 Code Review": "Please review the following code for bugs, best practices, and potential improvements:\n\n",
        "💻 Explain Code": "Please explain what this code does step by step:\n\n",
        "💻 Debug Help": "I'm getting an error with this code. Please help me debug it:\n\nCode:\n\nError:\n",
        "💻 Write Function": "Write a function that does the following:\n\n",
        "💻 Convert Code": "Convert the following code from [source language] to [target language]:\n\n",
        "📝 Summarize": "Please summarize the following text in a concise manner:\n\n",
        "📝 Improve Writing": "Please improve the following text for clarity and readability:\n\n",
        "📝 Fix Grammar": "Please fix any grammar and spelling errors in the following text:\n\n",
        "📝 Translate": "Translate the following text to [target language]:\n\n",
        "🔬 Explain Concept": "Explain the following concept in simple terms:\n\n",
        "🔬 Compare & Contrast": "Compare and contrast the following:\n\n",
        "🔬 Pros and Cons": "List the pros and cons of:\n\n",
        "🎯 Step-by-Step Guide": "Provide a step-by-step guide for:\n\n",
        "🎯 Best Practices": "What are the best practices for:\n\n",
        "📊 Analyze Data": "Analyze the following data and provide insights:\n\n",
        "💡 Brainstorm Ideas": "Brainstorm creative ideas for:\n\n",
        "📧 Write Email": "Write a professional email about:\n\n",
        "📄 Create Outline": "Create a detailed outline for:\n\n",
    }
    
    # Template selector
    template_col1, template_col2 = st.columns([1, 3])
    with template_col1:
        selected_template = st.selectbox(
            "📋 Templates",
            list(PROMPT_TEMPLATES.keys()),
            index=0,
            key="prompt_template",
            label_visibility="collapsed"
        )
    with template_col2:
        if selected_template != "None":
            st.caption(f"Template: {selected_template}")
    
    # Apply template to session state if changed
    if selected_template != "None":
        template_text = PROMPT_TEMPLATES[selected_template]
        if st.session_state.get("last_template") != selected_template:
            st.session_state.template_prefix = template_text
            st.session_state.last_template = selected_template
    else:
        st.session_state.template_prefix = ""
    
    prompt = st.chat_input("Ask me anything...")

if prompt:
    # Apply template prefix if set
    template_prefix = st.session_state.get("template_prefix", "")
    if template_prefix:
        prompt = template_prefix + prompt
        st.session_state.template_prefix = ""  # Clear after use
        st.session_state.last_template = "None"
    
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
        
        # Auto-select logic: detect query type and recommend models
        auto_select = st.session_state.get("brain_auto_select", False)
        detected_type = "general"
        
        if auto_select:
            query_lower = prompt.lower()
            # Detect query type
            code_keywords = ["code", "function", "debug", "error", "programming", "python", "javascript", "api", "script", "class", "method"]
            writing_keywords = ["write", "essay", "article", "email", "summarize", "translate", "draft", "blog"]
            analysis_keywords = ["analyze", "compare", "explain", "why", "how does", "difference", "pros and cons"]
            creative_keywords = ["brainstorm", "ideas", "creative", "story", "imagine", "generate", "invent"]
            
            if any(kw in query_lower for kw in code_keywords):
                detected_type = "code"
            elif any(kw in query_lower for kw in writing_keywords):
                detected_type = "writing"
            elif any(kw in query_lower for kw in analysis_keywords):
                detected_type = "analysis"
            elif any(kw in query_lower for kw in creative_keywords):
                detected_type = "creative"
            
            st.caption(f"🎯 Detected query type: **{detected_type.title()}**")
        
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

        # Reorder models based on learned recommendations + query type
        recommended_order = learning_brain.recommend_models(
            prompt,
            [m["provider"] for m in models_to_query]
        )
        
        # Boost certain providers based on detected type
        type_provider_boost = {
            "code": ["openai", "anthropic"],  # GPT and Claude excel at code
            "writing": ["anthropic", "openai"],  # Claude excels at writing
            "analysis": ["google", "openai"],  # Gemini good at analysis
            "creative": ["anthropic", "google"],
            "general": []
        }
        boosted = type_provider_boost.get(detected_type, [])
        
        if recommended_order or boosted:
            def sort_key(m):
                provider = m["provider"]
                base_score = recommended_order.index(provider) if provider in recommended_order else 10
                boost = -5 if provider in boosted else 0
                return base_score + boost
            models_to_query.sort(key=sort_key)
        
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
        
        # Response Comparison View - Show individual model responses side-by-side
        if len(model_responses) > 1:
            with st.expander("🔀 Compare Model Responses", expanded=False):
                st.markdown("#### Side-by-Side Comparison")
                
                # Create columns for each model
                num_models = len(model_responses)
                cols = st.columns(min(num_models, 3))
                
                for idx, response in enumerate(model_responses):
                    with cols[idx % 3]:
                        provider = response.get('provider', 'Unknown')
                        provider_icons = {"google": "🔵", "openai": "🟢", "anthropic": "🟣", "together": "🔴"}
                        icon = provider_icons.get(provider, "⚪")
                        
                        # Response card header
                        success = response.get('success', False)
                        status_icon = "✅" if success else "❌"
                        st.markdown(f"**{icon} {provider.upper()}** {status_icon}")
                        
                        # Response content
                        text = response.get('response', response.get('error', 'No response'))
                        if len(text) > 500:
                            text = text[:500] + "..."
                        st.markdown(text)
                        
                        # Response time if available
                        if response.get('response_time'):
                            st.caption(f"⚡ {response['response_time']:.2f}s")
                
                # Summary table
                st.markdown("---")
                st.markdown("#### Response Summary")
                summary_data = []
                for r in model_responses:
                    summary_data.append({
                        "Provider": r.get('provider', 'Unknown').upper(),
                        "Status": "✅ Success" if r.get('success') else "❌ Failed",
                        "Length": len(r.get('response', '')),
                    })
                st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
        
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
        user_message = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        st.session_state.messages.append(user_message)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display synthesized response
        with st.chat_message("assistant"):
            st.markdown(synthesized_response)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": synthesized_response,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model": "brain-mode",
            "provider": "multi"
        })
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
        
        user_message = {
            "role": "user",
            "content": final_prompt,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
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
        response_start_time = time.time()  # Track response time
        with st.chat_message("assistant"):
            # Loading skeleton placeholder
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown("""
                <div style="animation: pulse 1.5s infinite; background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%); 
                background-size: 200% 100%; padding: 20px; border-radius: 10px; margin: 10px 0;">
                    <div style="height: 16px; background: #d0d0d0; border-radius: 4px; margin-bottom: 8px; width: 80%;"></div>
                    <div style="height: 16px; background: #d0d0d0; border-radius: 4px; margin-bottom: 8px; width: 60%;"></div>
                    <div style="height: 16px; background: #d0d0d0; border-radius: 4px; width: 70%;"></div>
                </div>
                <style>
                @keyframes pulse {
                    0% { background-position: 200% 0; }
                    100% { background-position: -200% 0; }
                }
                </style>
                """, unsafe_allow_html=True)
                st.caption(f"🔄 Generating response with {model_choice_label}...")
            
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
                    loading_placeholder.empty()  # Clear loading skeleton
                    st.markdown(response_text)
                        
                elif provider == "openai":
                    # OpenAI GPT
                    loading_placeholder.empty()  # Clear loading skeleton
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
                
                # Store error info for retry
                st.session_state.last_error = {
                    "message": error_msg,
                    "provider": provider,
                    "model": model_name,
                    "prompt": final_prompt,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Categorized error messages with retry option
                error_container = st.container()
                with error_container:
                    if "404" in error_msg:
                        st.error(f"❌ Model not available: {model_name}. Try a different model from the sidebar.")
                        st.caption("💡 Tip: Some models may be deprecated or region-restricted.")
                    elif "DNS" in error_msg or "timeout" in error_msg.lower():
                        st.error("❌ Network error. Check your internet connection or VPN settings.")
                        st.caption("💡 Tip: Try again in a few seconds. Network issues are usually temporary.")
                    elif "API key" in error_msg or "authentication" in error_msg.lower():
                        st.error(f"❌ Invalid API key for {provider}. Please check your API key in the sidebar.")
                        st.caption("💡 Tip: Regenerate your API key from the provider's console.")
                    elif "rate" in error_msg.lower() or "quota" in error_msg.lower():
                        st.error("❌ Rate limit exceeded. Please wait a moment before trying again.")
                        st.caption("💡 Tip: Consider upgrading your API plan or using a different model.")
                    elif "context" in error_msg.lower() or "token" in error_msg.lower():
                        st.error("❌ Message too long. Try shortening your prompt or clearing chat history.")
                        st.caption("💡 Tip: Use the Clear Chat button to reset context.")
                    else:
                        st.error(f"❌ Request failed: {error_msg}")
                    
                    # Retry button
                    retry_col1, retry_col2 = st.columns([1, 3])
                    with retry_col1:
                        if st.button("🔄 Retry", key="retry_request", use_container_width=True):
                            st.rerun()
                    with retry_col2:
                        st.caption("Click to try again with the same prompt")
        
        # Save assistant response to history
        if response_text:
            response_time = time.time() - response_start_time
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "response_time": response_time,
                "model": model_name,
                "provider": provider
            })
            
            # Text-to-speech in voice mode
            if st.session_state.voice_mode and st.session_state.get("auto_speak", False) and response_text:
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
                    