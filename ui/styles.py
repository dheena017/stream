
import streamlit as st

def load_css():
    """Load all custom CSS styles for the application"""
    
    # Premium Dark Mode Theme
    if st.session_state.get('dark_mode', False):
        return """
        <style>
        /* Premium Dark Mode Theme - Deep Space & Neon Accents */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            /* Color Palette */
            --bg-primary: #0B0F19;       /* Deepest blue/black */
            --bg-secondary: #151B2B;     /* Slightly lighter panel bg */
            --bg-tertiary: #1E293B;      /* Card/Input bg */
            
            --text-primary: #F8FAFC;     /* Bright white text */
            --text-secondary: #94A3B8;   /* Muted text */
            --text-accent: #38BDF8;      /* Light blue accent text */
            
            --accent-primary: #6366F1;   /* Indigo */
            --accent-secondary: #8B5CF6; /* Violet */
            --accent-glow: rgba(99, 102, 241, 0.4);
            
            --border-subtle: rgba(148, 163, 184, 0.1);
            --border-focus: rgba(99, 102, 241, 0.5);
            
            --gradient-primary: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
            --gradient-surface: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
            
            --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.4);
            --glass-blur: blur(12px);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }

        /* --- Main Layout & Background --- */
        .stApp {
            background-color: var(--bg-primary);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.08) 0%, transparent 45%);
            background-attachment: fixed;
        }

        /* --- Sidebar --- */
        [data-testid="stSidebar"] {
            background-color: var(--bg-secondary) !important;
            border-right: 1px solid var(--border-subtle);
            box-shadow: 4px 0 24px rgba(0,0,0,0.2);
        }
        
        /* Sidebar Navigation Buttons */
        [data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            border: 1px solid var(--border-subtle) !important;
            color: var(--text-secondary) !important;
            justify-content: flex-start;
            padding-left: 1rem;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: var(--accent-primary) !important;
            color: var(--text-primary) !important;
            background: rgba(99, 102, 241, 0.1) !important;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: var(--gradient-primary) !important;
            border: none !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        /* --- Typography --- */
        h1, h2, h3 {
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
        }
        p, .stMarkdown {
            color: var(--text-secondary) !important;
            line-height: 1.6;
        }
        code, .stCodeBlock {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* --- Inputs & Interactive Elements --- */
        .stTextInput > div > div > input, 
        .stTextArea textarea, 
        .stSelectbox > div > div {
            background-color: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 8px !important;
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus, 
        .stTextArea textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 2px var(--accent-glow) !important;
            background-color: #1e293b !important;
        }

        /* --- Cards & Containers --- */
        div[data-testid="stExpander"], .stCard {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Metric Cards */
        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(30, 41, 59, 1) 0%, rgba(20, 27, 45, 1) 100%) !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            border-radius: 12px;
            padding: 16px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 0.9rem; }
        [data-testid="stMetricValue"] { 
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important; 
        }

        /* --- Chat Interface --- */
        .stChatMessage {
            background-color: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
        }
        [data-testid="chatAvatarIcon-user"] {
            background-color: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
        }
        [data-testid="chatAvatarIcon-assistant"] {
            background: var(--gradient-primary) !important;
            color: white !important;
        }

        /* --- Buttons --- */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button[kind="secondary"] {
            background-color: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-subtle) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton > button[kind="secondary"]:hover {
            border-color: var(--text-secondary) !important;
            transform: translateY(-1px);
        }
        .stButton > button[kind="primary"] {
            background: var(--gradient-primary) !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }
        
        /* --- Scrollbars --- */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { 
            background: #334155; 
            border-radius: 5px; 
            border: 2px solid var(--bg-primary);
        }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }

        /* Custom Classes */
        .highlight-text { color: var(--accent-primary); font-weight: 600; }
        .subtle-text { color: var(--text-secondary); font-size: 0.9rem; }
        </style>
        """
    else:
        # Premium Light Mode Theme
        return """
        <style>
        /* Premium Light Mode Theme - Clean, Airy & Professional */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            /* Color Palette */
            --bg-primary: #FFFFFF;      /* Pure white */
            --bg-secondary: #F8FAFC;    /* Very light gray/blue */
            --bg-tertiary: #F1F5F9;     /* Input bg */
            
            --text-primary: #0F172A;    /* Dark slate */
            --text-secondary: #475569;  /* Slate */
            --text-muted: #94A3B8;      /* Lighter slate */
            
            --accent-primary: #4F46E5;  /* Indigo */
            --accent-secondary: #7C3AED; /* Violet */
            --accent-subtle: #EEF2FF;   /* Very light indigo bg */
            
            --border-subtle: #E2E8F0;
            --border-focus: #4F46E5;
            
            --gradient-primary: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }
        
        .stApp {
            background-color: var(--bg-primary);
            background-image: radial-gradient(circle at top right, #f1f5f9 0%, transparent 40%);
        }

        /* --- Sidebar --- */
        [data-testid="stSidebar"] {
            background-color: #FAFAFA !important;
            border-right: 1px solid var(--border-subtle);
        }
        
        /* Sidebar Navigation */
        [data-testid="stSidebar"] .stButton > button {
            background: white !important;
            border: 1px solid var(--border-subtle) !important;
            color: var(--text-secondary) !important;
            justify-content: flex-start;
            padding-left: 1rem;
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: var(--accent-primary) !important;
            color: var(--accent-primary) !important;
            background: var(--accent-subtle) !important;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: var(--gradient-primary) !important;
            border: none !important;
            color: white !important;
        }

        /* --- Typography --- */
        h1, h2, h3, h4 {
            color: var(--text-primary) !important;
            letter-spacing: -0.01em;
            font-weight: 700 !important;
        }
        p, .stMarkdown {
            color: var(--text-secondary) !important;
            line-height: 1.6;
        }
        code, .stCodeBlock {
            font-family: 'JetBrains Mono', monospace !important;
            background-color: var(--bg-secondary) !important;
        }

        /* --- Inputs --- */
        .stTextInput > div > div > input, 
        .stTextArea textarea, 
        .stSelectbox > div > div {
            background-color: white !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 8px !important;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }

        /* --- Cards & Containers --- */
        div[data-testid="stExpander"], .stCard {
            background: white !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
            box-shadow: var(--shadow-sm);
        }
        
        /* Metrics */
        [data-testid="stMetric"] {
            background: white !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px;
            padding: 16px !important;
            box-shadow: var(--shadow-sm);
            transition: transform 0.2s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-weight: 500; }
        [data-testid="stMetricValue"] { color: var(--accent-primary) !important; font-weight: 700; }

        /* --- Chat Interface --- */
        .stChatMessage {
            background-color: white !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-sm);
        }
        .stChatMessage.user-message {
            background-color: #F8FAFC !important;
        }
        [data-testid="chatAvatarIcon-assistant"] {
            background: var(--gradient-primary) !important;
        }

        /* --- Buttons --- */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s;
        }
        .stButton > button[kind="primary"] {
            background: var(--gradient-primary) !important;
            border: none !important;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);
        }
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 8px -1px rgba(79, 70, 229, 0.4);
            transform: translateY(-1px);
        }
        .stButton > button[kind="secondary"] {
            background: white !important;
            border: 1px solid var(--border-subtle) !important;
            color: var(--text-secondary) !important;
            box-shadow: var(--shadow-sm);
        }
        .stButton > button[kind="secondary"]:hover {
            border-color: var(--text-secondary) !important;
            background: var(--bg-secondary) !important;
        }
        
        /* --- Scrollbars --- */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { 
            background: #CBD5E1; 
            border-radius: 5px; 
            border: 2px solid white;
        }
        ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
        </style>
        """
