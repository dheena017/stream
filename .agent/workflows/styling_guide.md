---
description: Guide to the centralized styling system
---

# Styling System Guide

This project uses a centralized styling system located in `ui/styles.py`. All CSS is injected via `st.markdown(unsafe_allow_html=True)`.

## 1. Core Variables
We use CSS variables for theming. These change dynamically based on the theme (Dark/Light).
- `--bg-primary`, `--bg-secondary`: Backgrounds
- `--text-primary`, `--text-secondary`: Typography
- `--accent-primary`: Main brand color (Indigo/Purple)
- `--gradient-primary`: Standard brand gradient

## 2. Common Classes
Do NOT use inline styles (e.g., `style="..."`). Use these classes instead:

### Layout
- `.main-header`: The top banner on pages (Chat, Dashboard).
- `.glass-panel`: A semi-transparent container for highlighted content.

### Components
- `.dashboard-card`: Standard card for metrics/content in dashboard.
- `.action-card`: Interactive card for quick actions.
- `.status-badge`: Small pill-shaped indicators (used in Chat).
- `.sidebar-header`: The top branding in the sidebar.
- `.sidebar-user-card`: The user profile summary in the sidebar.

## 3. Adding New Styles
1. Edit `ui/styles.py`.
2. Add your CSS class in **BOTH** the Dark Mode block and Light Mode block.
3. Use CSS variables to ensure it adapts to themes.
4. Use the class in your Python file: `st.markdown('<div class="my-new-class">...</div>', unsafe_allow_html=True)`.

## 4. Theme Toggling
Theme state is managed by `st.session_state['dark_mode']`.
Changing this boolean and calling `st.rerun()` will automatically apply the correct CSS block from `ui/styles.py`.
