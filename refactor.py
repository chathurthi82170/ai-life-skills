import os

# 1. Update .env
with open(".env", "r") as f:
    env_content = f.read()
if "TEACHER_USERNAME" not in env_content:
    with open(".env", "a") as f:
        f.write("\nTEACHER_USERNAME=teacher\nTEACHER_PASSWORD=teacher123\n")

# 2. rbac.py
rbac_code = """import streamlit as st

ROLE_ACCESS = {
    "Student": ["Learn_Skill", "Student_Dash", "Interactive_Stories", "Focus_Timer", "Daily_Routines", "Emotion_Explorer"],
    "Teacher": ["Teacher_Dash", "Student_Dash", "Learn_Skill", "Interactive_Stories", "Focus_Timer", "Daily_Routines", "Emotion_Explorer"],
    "Admin": ["System_Admin"]
}
ALL_PAGES = ["Learn_Skill", "Student_Dash", "System_Admin", "Teacher_Dash", "Interactive_Stories", "Focus_Timer", "Daily_Routines", "Emotion_Explorer"]

def enforce_access():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("🔒 Please log in from the main page first.")
        st.stop()
        
    current_role = st.session_state.get('role', '')
    if not current_role or current_role not in ROLE_ACCESS:
        st.error("Invalid role detected. Please log in again.")
        st.stop()
        
    allowed = ROLE_ACCESS[current_role]
    css_rules = [f'a[href$="{p}"] {{ display: none !important; }}' for p in ALL_PAGES if p not in allowed]
    
    if css_rules:
        st.markdown(f'<style>{" ".join(css_rules)}</style>', unsafe_allow_html=True)
"""
with open("rbac.py", "w", encoding="utf-8") as f:
    f.write(rbac_code)

# 3. Rename
renames = {
    "pages/2_Dashboard.py": "pages/2_Student_Dash.py",
    "pages/3_Admin.py": "pages/3_System_Admin.py",
    "pages/4_Interactive_Stories.py": "pages/5_Interactive_Stories.py",
    "pages/5_Focus_Timer.py": "pages/6_Focus_Timer.py",
    "pages/6_Daily_Routines.py": "pages/7_Daily_Routines.py",
    "pages/7_Emotion_Explorer.py": "pages/8_Emotion_Explorer.py"
}
for old, new in renames.items():
    if os.path.exists(old):
        os.rename(old, new)

# 4. Patch Pages
old_admin_auth = """if 'logged_in' not in st.session_state or not st.session_state.logged_in or st.session_state.get('role') != "Admin/Teacher":
    st.error("🔒 Access Denied. Please log in as Admin/Teacher from the main page.")
    st.stop()"""

old_auth = """if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please log in from the main page first.")
    st.stop()"""

old_hide = """if st.session_state.get('role') != 'Admin/Teacher':
    st.markdown('<style>a[href*="Admin"] {display: none !important;}</style>', unsafe_allow_html=True)"""

for file in os.listdir("pages"):
    if file.endswith(".py"):
        path = os.path.join("pages", file)
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        
        c = c.replace(old_admin_auth, "")
        c = c.replace(old_auth, "")
        c = c.replace(old_hide, "")
        
        injection = "\nimport sys, os\nsys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nfrom rbac import enforce_access\nenforce_access()\n"
        
        if "enforce_access()" not in c:
            if 'layout="wide")' in c:
                c = c.replace('layout="wide")', 'layout="wide")' + injection)
            elif 'layout="centered")' in c:
                c = c.replace('layout="centered")', 'layout="centered")' + injection)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
