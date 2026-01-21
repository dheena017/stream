
import streamlit as st

def load_css():
    """Load all custom CSS styles for the application"""
    
    # Premium Dark Mode Theme
    if st.session_state.get('dark_mode', False):
        return """
        <style>
        /* Premium Dark Mode Theme - Glassmorphism & Vibrant Gradients */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --text-primary: #ffffff;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: rgba(30, 41, 59, 0.7);
            --border-color: rgba(255, 255, 255, 0.1);
            --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --accent-color: #8b5cf6;
            --glass-border: 1px solid rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: var(--bg-primary);
            background-image: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.1) 0%, transparent 40%),
                              radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.1) 0%, transparent 40%);
            color: var(--text-primary);
        }

        /* Sidebar Styling */
        .stSidebar {
            background-color: rgba(15, 23, 42, 0.95) !important;
            border-right: var(--glass-border);
        }
        .stSidebar [data-testid="stSidebarContent"] {
            background-color: transparent;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }
        p, span, div, label {
            color: var(--text-secondary);
        }

        /* Inputs */
        .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
            background-color: rgba(30, 41, 59, 0.6) !important;
            color: #ffffff !important;
            border: var(--glass-border) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px);
        }
        .stTextInput > div > div > input:focus {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
        }

        /* Buttons */
        .stButton > button {
            background: var(--accent-gradient) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
        }
        .stButton > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: none;
        }

        /* Cards & Containers */
        div[data-testid="stExpander"], .quick-action-card, .feature-card {
            background: var(--bg-card) !important;
            border: var(--glass-border) !important;
            border-radius: 16px !important;
            box-shadow: var(--glass-shadow);
            backdrop-filter: blur(12px);
        }

        /* Chat Messages */
        .stChatMessage {
            background-color: rgba(30, 41, 59, 0.6) !important;
            border: var(--glass-border) !important;
            border-radius: 16px !important;
        }
        .stChatMessage[data-testid="chatAvatarIcon-assistant"] {
            background: var(--accent-gradient) !important;
        }

        /* Code Blocks */
        .stCodeBlock {
            background-color: #0f172a !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Metrics */
        .stMetric {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px !important;
            backdrop-filter: blur(8px);
        }
        .stMetric label { color: var(--text-muted) !important; }
        .stMetric [data-testid="stMetricValue"] { color: #f8fafc !important; font-weight: 700; }

        /* Tables */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            overflow: hidden;
        }
        
        /* Text overrides */
        .stMarkdown, .stText, p { color: var(--text-secondary) !important; }
        .stMarkdown strong { color: #ffffff !important; }
        
        /* Inline Styles Overrides */
        div[style*="background: linear-gradient"] {
            border: none !important;
        }
        
        /* Scrollbars */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }
        </style>
        """
    else:
        # Premium Light Mode Theme
        return """
        <style>
        /* Premium Light Mode Theme - Clean, Minimal, Modern */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --border-color: #e2e8f0;
            --accent-gradient: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            --accent-color: #6366f1;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
        }

        .stApp {
            background-color: var(--bg-primary);
        }

        /* Sidebar */
        .stSidebar {
            background-color: #ffffff !important;
            border-right: 1px solid var(--border-color);
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #0f172a !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }
        p, span, div, label {
            color: var(--text-secondary);
        }

        /* Inputs */
        .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
            background-color: #ffffff !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            box-shadow: var(--shadow-sm);
        }
        .stTextInput > div > div > input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
        }

        /* Buttons */
        .stButton > button {
            background: var(--accent-gradient) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 8px rgba(79, 70, 229, 0.3);
        }

        /* Cards */
        div[data-testid="stExpander"], .quick-action-card, .feature-card, .stMetric {
            background: #ffffff !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-sm);
        }

        /* Chat Messages */
        .stChatMessage {
            background-color: #ffffff !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 16px !important;
            box-shadow: var(--shadow-sm);
        }
        .stChatMessage[data-testid="chatAvatarIcon-assistant"] {
            background: var(--accent-gradient) !important;
        }

        /* Code Blocks */
        .stCodeBlock {
            background-color: #f1f5f9 !important;
            border-radius: 12px !important;
        }

        /* Tables */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
        }

        /* Metric Values */
        .stMetric [data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-weight: 700;
        }
        
        /* Utility Overrides */
        .stMarkdown, .stText { color: var(--text-secondary) !important; }
        
        /* Scrollbars */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        </style>
        """
