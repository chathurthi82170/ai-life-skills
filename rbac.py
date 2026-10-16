import streamlit as st
import os

ROLE_ACCESS = {
    "Student": ["Learn_Skill", "Student_Dash", "Interactive_Stories", "Focus_Timer", "Daily_Routines", "Emotion_Explorer", "Sensory_Sandbox", "Reward_Shop", "Student_Profile", "AI_Assessment", "AI_Companion", "Visual_Schedule", "Safety_Skills", "Money_Manager"],
    "Teacher": ["Teacher_Dash"],
    "Parent": ["Parent_Dash"],
    "Admin": ["System_Admin"]
}

ALL_PAGES = [
    "Learn_Skill", "Student_Dash", "System_Admin", "Teacher_Dash", 
    "Interactive_Stories", "Focus_Timer", "Daily_Routines", "Emotion_Explorer",
    "Sensory_Sandbox", "Reward_Shop", "Student_Profile", "AI_Assessment", "Parent_Dash",
    "AI_Companion", "Visual_Schedule", "Safety_Skills", "Money_Manager"
]

def inject_sidebar_css():
    current_role = st.session_state.get('role', '')
    if not current_role or current_role not in ROLE_ACCESS:
        return
        
    allowed = ROLE_ACCESS[current_role]
    css_rules = []
    for p in ALL_PAGES:
        if p not in allowed:
            p_hyphen = p.replace('_', '-')
            # Streamlit URLs can vary (case and hyphens vs underscores), cover all bases
            css_rules.append(f'a[href*="{p}" i] {{ display: none !important; }}')
            css_rules.append(f'a[href*="{p_hyphen}" i] {{ display: none !important; }}')
    
    css_rules.append('''
        [data-testid="stSidebar"] a, [data-testid="stSidebar"] span, [data-testid="stSidebarNav"] span, [data-testid="stSidebarNavLink"] span {
            color: #ffffff !important;
            font-weight: 600 !important;
            opacity: 1 !important;
        }
    ''')
    if css_rules:
        st.markdown(f'<style>{" ".join(css_rules)}</style>', unsafe_allow_html=True)

def apply_classic_background():
    # 100% RELIABLE CSS INJECTION FROM MASTER FILE FOR ALL ROLES
    try:
        css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load theme: {e}")

def enforce_access():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("🔒 Please log in from the main page first.")
        st.stop()
        
    current_role = st.session_state.get('role', '')
    if not current_role or current_role not in ROLE_ACCESS:
        st.error("Invalid role detected. Please log in again.")
        st.stop()
        
    inject_sidebar_css()
    apply_classic_background()

    with st.sidebar:
        st.markdown("---")
        st.write(f"👤 **{st.session_state.get('username', '')}** ({current_role})")
        if st.button("🚪 Logout", key="universal_logout_sidebar_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.switch_page("main.py")
