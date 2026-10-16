import streamlit as st
import os
from dotenv import load_dotenv
import database
import importlib
importlib.reload(database)

# Initialize the SQLite Database
database.init_db()

# Inject master CSS from style.css globally
try:
    with open(os.path.join(os.path.dirname(__file__), 'style.css'), 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception:
    pass

load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "admin123")
TEACHER_USER = os.getenv("TEACHER_USERNAME", "teacher")
TEACHER_PASS = os.getenv("TEACHER_PASSWORD", "teacher123")

# Ensure default admin, teacher, and student vv exist in the DB
database.add_user(ADMIN_USER, ADMIN_PASS, "Admin")
database.add_user(TEACHER_USER, TEACHER_PASS, "Teacher")
database.add_user("vv", "123456", "Student")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

    if not st.session_state.logged_in:
        # Hide sidebar entirely on the login page
        st.markdown('<style>[data-testid="stSidebar"] { display: none; }</style>', unsafe_allow_html=True)
        
        # 2-Column Layout for a professional landing page
        col1, padding, col2 = st.columns([1.2, 0.1, 1])
        
        with col1:
            st.markdown('<br><br>', unsafe_allow_html=True)
            st.markdown('<p class="hero-text">Empowering Every<br>Child to Learn.</p>', unsafe_allow_html=True)
            st.markdown('<p class="sub-hero">An Agentic AI Platform that adapts daily life skills into personalized, interactive learning modules for children of all learning styles.</p>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box"><b>🧠 Adaptive AI Generation</b><br>Dynamically scales task complexity based on each child's learning pace.</div>
            <div class="feature-box"><b>📊 Comprehensive Analytics</b><br>Real-time progress tracking for parents, educators, and admins.</div>
            <div class="feature-box"><b>🎮 Multi-modal Learning</b><br>Visual, auditory, and gamified interaction modes for children.</div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown('<br><br>', unsafe_allow_html=True)
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.subheader("Welcome Back 👋")
            st.write("Please select your portal to sign in or register.")
            
            # Separate Logins using Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🎒 Student", "👩‍🏫 Teacher", "👨‍👩‍👧 Parent", "⚙️ Admin"])
            
            with tab1:
                student_user = st.text_input("Student Username", key="stu_user", placeholder="Enter username (e.g. vv)")
                student_pass = st.text_input("Password", type="password", key="stu_pass", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Student Login / Register 🚀", key="btn_stu", use_container_width=True, type="primary"):
                    if student_user and student_pass:
                        # Automatically save student to SQLite DB so they appear in Admin & Teacher dashboards
                        database.add_user(student_user, student_pass, "Student")
                        st.session_state.logged_in = True
                        st.session_state.username = student_user
                        st.session_state.role = "Student"
                        st.switch_page("pages/11_Student_Profile.py")
                    else:
                        st.error("Please enter both username and password.")
                        
            with tab2:
                teacher_user = st.text_input("Teacher ID", key="teach_user", placeholder="Enter Teacher ID")
                teacher_pass = st.text_input("Password", type="password", key="teach_pass", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Teacher Login / Register 👩‍🏫", key="btn_teach", use_container_width=True, type="primary"):
                    if teacher_user and teacher_pass:
                        database.add_user(teacher_user, teacher_pass, "Teacher")
                        st.session_state.logged_in = True
                        st.session_state.username = teacher_user
                        st.session_state.role = "Teacher"
                        st.rerun()
                    else:
                        st.error("Please enter credentials.")
                        
            with tab3:
                parent_user = st.text_input("Parent Email / Name", key="par_user", placeholder="Enter Parent Email")
                parent_pass = st.text_input("Password", type="password", key="par_pass", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Parent Login / Register 👨‍👩‍👧", key="btn_par", use_container_width=True, type="primary"):
                    if parent_user and parent_pass:
                        database.add_user(parent_user, parent_pass, "Parent")
                        st.session_state.logged_in = True
                        st.session_state.username = parent_user
                        st.session_state.role = "Parent"
                        st.rerun()
                    else:
                        st.error("Please enter credentials.")
                        
            with tab4:
                st.info("Admins are pre-configured by the system.")
                admin_user = st.text_input("Admin ID", key="adm_user", placeholder="Enter Admin ID")
                admin_pass = st.text_input("Password", type="password", key="adm_pass", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Secure Admin Login ⚙️", key="btn_adm", use_container_width=True, type="primary"):
                    if database.verify_user(admin_user, admin_pass, "Admin") or (admin_user == ADMIN_USER and admin_pass == ADMIN_PASS):
                        st.session_state.logged_in = True
                        st.session_state.username = admin_user
                        st.session_state.role = "Admin"
                        st.rerun()
                    else:
                        st.error("❌ Invalid Admin credentials.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        from rbac import inject_sidebar_css
        inject_sidebar_css()
        
        st.success(f"Welcome back, **{st.session_state.username}**! (Role: **{st.session_state.role}**)")
        
        if st.session_state.role == "Student":
            st.switch_page("pages/11_Student_Profile.py")
        else:
            st.info("Use the sidebar on the left to navigate to your authorized modules.")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

if __name__ == "__main__":
    main()
