
import streamlit as st

def load_css():
    """Load all custom CSS styles for the application"""
    
    # Premium Dark Mode Theme - Enforced
    return """
    <style>
    /* Premium Dark Mode Theme - Deep Space & Neon Accents */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        /* Color Palette */
        --bg-primary: #0B0F19;       /* Deepest blue/black */
        --bg-secondary: #151B2B;     /* Slightly lighter panel bg */
        --bg-tertiary: #1E293B;      /* Card/Input bg */
        --bg-secondary-rgb: 21, 27, 43; /* Added for RGB usage */
        
        --text-primary: #F8FAFC;     /* Bright white text */
        --text-secondary: #94A3B8;   /* Muted text */
        --text-accent: #38BDF8;      /* Light blue accent text */
        
        --accent-primary: #6366F1;   /* Indigo */
        --accent-secondary: #8B5CF6; /* Violet */
        --accent-glow: rgba(99, 102, 241, 0.4);
        --accent-subtle: rgba(99, 102, 241, 0.1); 
        
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

    /* --- Layout & Utility Classes --- */
    .main-header {
        background: var(--gradient-primary);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-card);
        color: white;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .glass-panel {
        background: rgba(var(--bg-secondary-rgb), 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow-card);
    }

    /* --- Sidebar Specific --- */
    .sidebar-header {
        background: var(--gradient-primary); 
        padding: 1.25rem 1rem; 
        border-radius: 14px; 
        text-align: center; 
        margin-bottom: 1.5rem; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .sidebar-user-card {
        background: var(--bg-tertiary);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid var(--accent-primary);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* --- Dashboard Cards --- */
    .dashboard-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .dashboard-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-card);
        border-color: var(--accent-primary);
    }
    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; bottom: 0; width: 4px;
        background: var(--gradient-primary);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* --- Quick Actions --- */
    .action-card {
        background: var(--bg-tertiary);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-subtle);
        transition: all 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .action-card:hover {
        border-color: var(--accent-primary);
        transform: translateY(-2px);
    }
    .action-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .action-desc {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
        line-height: 1.5;
    }

    /* --- Status Indicators (Chat) --- */
    .status-badge {
        background: var(--bg-tertiary);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-subtle);
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    .status-badge.active {
        border-color: var(--accent-primary);
        color: var(--accent-primary);
        background: rgba(99, 102, 241, 0.1);
    }

    /* --- Welcome Screen --- */
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .welcome-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* Custom Scrollbars & Utilities */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { 
        background: var(--text-secondary); 
        border-radius: 4px; 
        opacity: 0.5;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-primary); }

    /* --- Accessibility Enhancements --- */
    /* Strong focus indicators for keyboard navigation */
    :focus-visible, [tabindex="0"]:focus, button:focus, input:focus, select:focus, textarea:focus {
        outline: 3px solid var(--accent-primary) !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 0 4px var(--accent-subtle) !important;
    }

    /* Ensure text visibility */
    .stMarkdown, p, span, div {
        text-rendering: optimizeLegibility;
    }
    </style>
    """
