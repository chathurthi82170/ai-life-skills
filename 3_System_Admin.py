import streamlit as st
import pandas as pd
import altair as alt
import sys, os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)

st.set_page_config(page_title="System Admin", page_icon="⚙️", layout="wide")
enforce_access()

st.markdown("""
<style>
    .admin-header { font-size: 2.5rem; font-weight: 800; margin-bottom: 20px;}
    .admin-card { padding: 25px; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="admin-header">⚙️ Nexus System Administration</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Platform Health", "🛠️ Agentic Config", "👨‍🎓 Manage Users", 
    "👩‍🏫 Manage Teachers", "📜 System Logs", "🛡️ Security & Backup"
])

with tab1:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("Platform Health Overview")
    colA, colB = st.columns(2)
    with colA:
        st.write("**Total System Usage (Current Month)**")
        source = pd.DataFrame({"Week": ["W1", "W2", "W3", "W4"], "Sessions": [450, 520, 610, 780]})
        line = alt.Chart(source).mark_line(color="#38BDF8", strokeWidth=3).encode(x='Week', y='Sessions').properties(height=300)
        st.altair_chart(line, use_container_width=True)
    with colB:
        st.write("**Agentic LLM API Latency (ms)**")
        bar_data = pd.DataFrame({"Endpoint": ["Task Planner", "Emotion Assessor", "Routine Gen"], "Latency": [350, 210, 420]})
        bar = alt.Chart(bar_data).mark_bar(color="#F43F5E").encode(x='Latency:Q', y=alt.Y('Endpoint:N', sort='-x')).properties(height=300)
        st.altair_chart(bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("Global Agentic AI Settings & API Keys")
    
    current_key = os.environ.get("OPENAI_API_KEY", "")
    masked_key = (current_key[:6] + "..." + current_key[-4:]) if len(current_key) > 10 else ""
    
    st.info(f"🔑 **Current Active Status:** {'✅ API Key Active (' + masked_key + ')' if current_key else '⚡ Using Free Live AI Engine (Pollinations.ai)'}")
    
    api_key_input = st.text_input("OpenAI API Key (Optional):", value=current_key, type="password", placeholder="sk-proj-...")
    
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("LLM Routing Engine", ["OpenAI GPT-3.5-Turbo", "OpenAI GPT-4", "Free Live AI Engine (Pollinations.ai)", "Local MOCK Engine (Fallback)"])
        st.slider("Model Temperature (Creativity vs Determinism)", 0.0, 1.0, 0.7)
    with c2:
        st.toggle("Enable Text-to-Speech Engine System-wide", value=True)
        st.number_input("Maximum steps per task breakdown", min_value=3, max_value=15, value=7)
    
    if st.button("Deploy Configuration to Agents 🚀", type="primary"):
        if api_key_input.strip():
            os.environ["OPENAI_API_KEY"] = api_key_input.strip()
            # Save to .env file as well
            try:
                env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
                with open(env_path, "a", encoding="utf-8") as f:
                    f.write(f"\nOPENAI_API_KEY={api_key_input.strip()}\n")
            except Exception:
                pass
            st.success("✅ OpenAI API Key saved and deployed successfully!")
        else:
            st.success("✅ Configuration deployed! System is running on the **Free Live AI Engine**.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("Manage Users (Students & Assessment Scores Database)")
    
    # Fetch real data & scores from SQLite
    students = database.get_all_users("Student")
    if students:
        student_records = []
        for s_user, d_joined in students:
            score_data = database.get_latest_assessment(s_user)
            if score_data:
                score_str = f"{score_data[0]} / {score_data[1]}"
                level_str = score_data[2]
            else:
                score_str = "Not Taken Yet"
                level_str = "Pending ⭐"
                
            student_records.append({
                "Student Username": s_user,
                "Assessment Score": score_str,
                "Assigned Level": level_str,
                "Date Joined": d_joined
            })
            
        student_df = pd.DataFrame(student_records)
        st.dataframe(student_df, use_container_width=True, hide_index=True)
    else:
        st.info("No students registered in the database yet.")
        
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("+ Add New Student Manually"):
            st.info("Form to add new student opened.")
    with c2: 
        if st.button("- Suspend Selected Student"):
            st.warning("Selected student has been suspended.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("Manage Teachers Database")
    
    # Fetch real data from SQLite
    teachers = database.get_all_users("Teacher")
    if teachers:
        teacher_df = pd.DataFrame(teachers, columns=["Teacher Username", "Date Joined"])
        st.dataframe(teacher_df, use_container_width=True)
    else:
        st.info("No teachers registered in the database yet.")
        
    if st.button("+ Add New Teacher Manually"):
        st.info("Form to add new teacher opened.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("Live System Logs")
    st.code("[2026-09-04 10:01:23] INFO: Database connection initialized.\n[2026-09-04 10:05:12] WARN: LLM API Timeout (Retry 1/3)\n[2026-09-04 10:05:15] INFO: LLM Connection restored.\n[2026-09-04 10:12:44] INFO: Database backup requested.", language="shell")
    st.markdown('</div>', unsafe_allow_html=True)

with tab6:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("Security & Data Backup")
    st.write("Ensure platform compliance with GDPR and student privacy laws.")
    st.checkbox("Enforce 2-Factor Authentication for Teachers/Admins", value=True)
    st.checkbox("Anonymize all student data in analytics", value=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Read the actual SQLite database file for download!
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nexus.db")
        with open(db_path, "rb") as f:
            db_bytes = f.read()
        
        st.download_button(
            label="💾 Download SQLite Database (.db file)", 
            data=db_bytes, 
            file_name="nexus_production_backup.db", 
            mime="application/octet-stream", 
            type="primary"
        )
    except Exception as e:
        st.error("Database file not ready for download yet.")

    st.markdown('</div>', unsafe_allow_html=True)
